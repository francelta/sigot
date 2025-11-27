"""
Vista para el proceso de onboarding transaccional de transportistas
"""

import json
import logging

from django.db import transaction
from geopy.exc import GeocoderServiceError, GeocoderTimedOut
from geopy.geocoders import Nominatim
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from sigot.infrastructure.api.permissions import IsTransportista
from sigot.infrastructure.api.serializers.auth import UserSerializer
from sigot.infrastructure.api.serializers.onboarding import OnboardingPayloadSerializer
from sigot.infrastructure.api.serializers.transportistas import TransportistaListSerializer
from sigot.infrastructure.db.models import Categoria, Transportista, TransportistaCategoria

logger = logging.getLogger(__name__)


class OnboardingCompleteView(APIView):
    """
    Endpoint: POST /api/onboarding/complete/
    
    Completa el proceso de onboarding del transportista v3.0 en una única transacción.
    Actualiza todos los datos del wizard (código postal, maquinaria, radios, imágenes).
    
    Requisitos:
    - Usuario autenticado
    - Usuario debe ser transportista
    - Todas las operaciones se ejecutan en una transacción atómica
    """

    permission_classes = [IsAuthenticated, IsTransportista]

    def _geocode_postal_code(self, codigo_postal: str) -> tuple[float, float] | None:
        """
        Geocodifica un código postal español y retorna (latitud, longitud).
        Usa Nominatim (OpenStreetMap) para geocodificar.
        """
        try:
            # Formato para España: "28001, España" o solo el código postal
            query = f"{codigo_postal}, España"
            geolocator = Nominatim(user_agent="sigot")
            location = geolocator.geocode(query, timeout=10)
            
            if location:
                # Retorna (latitud, longitud)
                return (location.latitude, location.longitude)
            return None
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            logger.error(f"Error geocodificando código postal '{codigo_postal}': {e}")
            return None
        except Exception as e:
            logger.error(f"Error inesperado geocodificando código postal '{codigo_postal}': {e}")
            return None

    def _parse_request_data(self, request):
        """
        Parsea los datos de la request, manejando tanto JSON como FormData.
        Si viene FormData, parsea el campo 'maquinaria' que viene como JSON string.
        """
        # Para FormData, no podemos hacer copy() directamente porque contiene archivos
        # En su lugar, construimos un dict manualmente
        if request.content_type and 'multipart/form-data' in request.content_type:
            # Es FormData - construir dict manualmente
            data = {}
            
            # Copiar campos simples (no archivos)
            for key, value in request.data.items():
                if key not in request.FILES:
                    data[key] = value
            
            # Si 'maquinaria' viene como string (FormData), parsearlo
            if 'maquinaria' in data and isinstance(data['maquinaria'], str):
                try:
                    data['maquinaria'] = json.loads(data['maquinaria'])
                except json.JSONDecodeError:
                    logger.error(f"Error parsing maquinaria JSON: {data['maquinaria']}")
                    raise ValueError("El campo 'maquinaria' no es un JSON válido")
            
            # Manejar imágenes de maquinaria que vienen como archivos separados
            # Formato: maquinaria_0_imagen, maquinaria_1_imagen, etc.
            if 'maquinaria' in data and isinstance(data['maquinaria'], list):
                for index, maquina_item in enumerate(data['maquinaria']):
                    imagen_key = f'maquinaria_{index}_imagen'
                    if imagen_key in request.FILES:
                        maquina_item['imagen'] = request.FILES[imagen_key]
            
            # Añadir foto_de_perfil si existe
            if 'foto_de_perfil' in request.FILES:
                data['foto_de_perfil'] = request.FILES['foto_de_perfil']
        else:
            # Es JSON - podemos usar copy() normalmente
            data = request.data.copy()
        
        return data

    @transaction.atomic
    def post(self, request):
        """
        Procesa el payload completo del wizard v3.0 y actualiza el perfil del transportista.
        
        Request body (OnboardingPayloadSerializer):
        - codigo_postal: str
        - maquinaria: [
            { categoria_id: int, radio_km_especifico: int | null, imagen: File | null }
          ]
        - radio_km_general: int | null
        - foto_de_perfil: File | null
        
        Response (200 OK):
        - message: str
        - transportista: Transportista object
        - user: User object
        """
        # Parsear datos de la request (maneja JSON y FormData)
        try:
            parsed_data = self._parse_request_data(request)
        except ValueError as e:
            return Response(
                {
                    'error': 'VALIDATION_ERROR',
                    'message': str(e)
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validar el payload
        serializer = OnboardingPayloadSerializer(data=parsed_data)
        
        if not serializer.is_valid():
            return Response(
                {
                    'error': 'VALIDATION_ERROR',
                    'message': 'Los datos proporcionados no son válidos',
                    'details': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        validated_data = serializer.validated_data

        # Obtener el transportista del usuario autenticado
        try:
            transportista = Transportista.objects.get(user=request.user)
        except Transportista.DoesNotExist:
            return Response(
                {
                    'error': 'NOT_FOUND',
                    'message': 'No se encontró el perfil de transportista'
                },
                status=status.HTTP_404_NOT_FOUND
            )

        # Validar que todas las categorías existen
        categoria_ids = [item['categoria_id'] for item in validated_data['maquinaria']]
        categorias_validas = Categoria.objects.filter(id__in=categoria_ids)
        
        if categorias_validas.count() != len(categoria_ids):
            # IDs de categorías que no existen
            ids_validos = set(categorias_validas.values_list('id', flat=True))
            ids_invalidos = set(categoria_ids) - ids_validos
            return Response(
                {
                    'error': 'VALIDATION_ERROR',
                    'message': 'Una o más categorías no existen',
                    'details': {
                        'maquinaria': [
                            f'La categoría con ID {cat_id} no existe'
                            for cat_id in ids_invalidos
                        ]
                    }
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # TRANSACCIÓN ATÓMICA: Todas las operaciones se ejecutan dentro de @transaction.atomic
        # Si cualquier operación falla, se hace rollback completo

        # 1. Geocodificar código postal y actualizar Transportista
        codigo_postal = validated_data['codigo_postal']
        coords = self._geocode_postal_code(codigo_postal)
        
        transportista.codigo_postal = codigo_postal
        if coords:
            transportista.base_latitud = coords[0]
            transportista.base_longitud = coords[1]
        transportista.radio_km_general = validated_data.get('radio_km_general')
        transportista.tipo_zona_actuacion = 'RADIO'  # Siempre RADIO en v3.0
        
        # Actualizar foto_de_perfil si se proporciona
        if 'foto_de_perfil' in validated_data and validated_data['foto_de_perfil']:
            transportista.foto_de_perfil = validated_data['foto_de_perfil']
        
        transportista.save()

        # 2. Eliminar todas las relaciones TransportistaCategoria existentes
        TransportistaCategoria.objects.filter(transportista=transportista).delete()

        # 3. Crear nuevos objetos TransportistaCategoria para cada máquina
        for maquina_item in validated_data['maquinaria']:
            TransportistaCategoria.objects.create(
                transportista=transportista,
                categoria_id=maquina_item['categoria_id'],
                radio_km_especifico=maquina_item.get('radio_km_especifico'),
                nombre_vehiculo=maquina_item.get('nombre_vehiculo'),
                marca=maquina_item.get('marca'),
                tonelaje=maquina_item.get('tonelaje'),
                caracteristicas=maquina_item.get('caracteristicas'),
                imagen_maquina=maquina_item.get('imagen')  # Puede ser None o un archivo
            )

        # Preparar respuesta según WizardSubmissionResponse
        transportista_serializer = TransportistaListSerializer([transportista], many=True)
        user_serializer = UserSerializer(request.user)

        response_data = {
            'message': 'Onboarding completado exitosamente',
            'transportista': transportista_serializer.data[0],
            'user': user_serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)

