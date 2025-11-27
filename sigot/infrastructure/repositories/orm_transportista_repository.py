"""
Repositorio ORM para Transportistas
Implementa TransportistaRepositoryPort usando el ORM de Django/GeoDjango
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
import logging
import math

from django.db.models import Q
from django.utils import timezone
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError

from sigot.core.ports import (
    TransportistaRepositoryPort,
    TransportistaData,
    Point,
)
from sigot.infrastructure.db.models import Transportista, User

logger = logging.getLogger(__name__)


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calcula la distancia en kilómetros entre dos puntos usando la fórmula de Haversine.
    """
    R = 6371  # Radio de la Tierra en km
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = math.sin(delta_lat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c


class TransportistaRepositoryORM(TransportistaRepositoryPort):
    """
    Implementación ORM del TransportistaRepositoryPort.
    Usa los modelos de Django para persistir datos y consultas geoespaciales.
    """

    def find_by_id(self, transportista_id: int) -> Optional[Dict[str, Any]]:
        """Busca un transportista por su ID."""
        try:
            transportista = (
                Transportista.objects.select_related('user')
                .prefetch_related('categorias')
                .get(user_id=transportista_id)
            )
            return self._to_dict(transportista, include_distance=False)
        except Transportista.DoesNotExist:
            return None

    def find_by_user_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Busca un transportista por el ID de su usuario asociado."""
        try:
            transportista = (
                Transportista.objects.select_related('user')
                .prefetch_related('categorias')
                .get(user_id=user_id)
            )
            return self._to_dict(transportista, include_distance=False)
        except Transportista.DoesNotExist:
            return None

    def _geocodificar_consulta(self, query_location_str: str) -> Optional[Point]:
        """
        Geocodifica una consulta de búsqueda (ej: "Madrid", "CP: 28001") en un Point.
        Retorna None si no se puede geocodificar.
        """
        try:
            geolocator = Nominatim(user_agent="sigot")
            # Si es solo un número (código postal), añadir ", España"
            query = query_location_str.strip()
            if query.isdigit() and len(query) == 5:
                query = f"{query}, España"
            location = geolocator.geocode(query, timeout=10)
            if location:
                return Point(latitude=location.latitude, longitude=location.longitude)
            return None
        except (GeocoderTimedOut, GeocoderServiceError) as e:
            logger.error(f"Error geocodificando '{query_location_str}': {e}")
            return None
        except Exception as e:
            logger.error(f"Error inesperado geocodificando '{query_location_str}': {e}")
            return None

    def find_transportistas_por_zona(
        self,
        query_location_str: str,
        category_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Busca transportistas disponibles según su zona de actuación.
        
        Args:
            query_location_str: Consulta de búsqueda (ej: "Madrid", "CP: 28001")
            category_id: ID de categoría opcional para filtrar
            
        Returns:
            Lista de dicts con los datos de los transportistas encontrados
        """
        # Geocodificar la consulta del usuario
        cliente_point = self._geocodificar_consulta(query_location_str)
        if not cliente_point:
            logger.warning(f"No se pudo geocodificar la consulta: {query_location_str}")
            return []
        
        logger.info(f"Consulta geocodificada: {query_location_str} -> {cliente_point}")

        # Extraer provincia/ciudad de la consulta (simplificado para MVP)
        # En producción, esto debería usar un servicio más robusto
        provincia_cliente = None
        ciudad_cliente = None
        try:
            geolocator = Nominatim(user_agent="sigot")
            location = geolocator.geocode(query_location_str, timeout=10, addressdetails=True)
            if location and location.raw.get('address'):
                provincia_cliente = location.raw['address'].get('state') or location.raw['address'].get('province')
                ciudad_cliente = location.raw['address'].get('city') or location.raw['address'].get('town')
        except Exception as e:
            logger.warning(f"No se pudo extraer provincia/ciudad de '{query_location_str}': {e}")

        # Construir la consulta
        queryset = Transportista.objects.filter(disponible=True).select_related('user').prefetch_related(
            'categorias', 'transportistacategoria_set', 'transportistacategoria_set__categoria'
        )

        resultados = []
        
        # Si hay filtro por categoría, obtener todas las categorías descendientes una sola vez
        categoria_ids_validas = None
        if category_id:
            from sigot.infrastructure.db.models import Categoria
            categoria_buscada = Categoria.objects.filter(id=category_id).prefetch_related('children').first()
            
            if categoria_buscada:
                def get_all_descendants(cat):
                    descendants = [cat.id]
                    children = list(cat.children.all())
                    for child in children:
                        descendants.extend(get_all_descendants(child))
                    return descendants
                
                categoria_ids_validas = set(get_all_descendants(categoria_buscada))
                logger.info(f"Categorías válidas para búsqueda: {categoria_ids_validas}")
        
        # Caso 1: Transportistas con RADIO
        radio_filter = Q(
            tipo_zona_actuacion='RADIO',
            base_latitud__isnull=False,
            base_longitud__isnull=False,
        ) & (
            Q(radio_km_general__isnull=False) | 
            Q(transportistacategoria_set__radio_km_especifico__isnull=False)
        )
        queryset_radio = queryset.filter(radio_filter).distinct()
        
        logger.info(f"Transportistas después del filtro RADIO: {queryset_radio.count()}")
        
        # Filtrar en Python usando Haversine
        for transportista in queryset_radio:
            # Calcular distancia usando Haversine
            distancia_km = haversine_distance(
                cliente_point.latitude, cliente_point.longitude,
                transportista.base_latitud, transportista.base_longitud
            )
            transportista._distancia_km = distancia_km  # Guardar para uso posterior
            
            # Si hay filtro por categoría, verificar si el transportista tiene esa categoría
            if category_id and categoria_ids_validas is not None:
                categorias_transportista = list(transportista.transportistacategoria_set.all())
                
                tiene_categoria = False
                transportista_categoria_match = None
                
                for tc in categorias_transportista:
                    if tc.categoria.id in categoria_ids_validas:
                        tiene_categoria = True
                        transportista_categoria_match = tc
                        break
                
                if not tiene_categoria:
                    continue
                
                radio_efectivo = transportista_categoria_match.radio_km_especifico if transportista_categoria_match else None
                radio_efectivo = radio_efectivo or transportista.radio_km_general
            else:
                radio_efectivo = transportista.radio_km_general
            
            if not radio_efectivo:
                continue
            
            if distancia_km <= radio_efectivo:
                resultados.append(transportista)

        # Caso 2: Transportistas con ZONAS
        queryset_zonas = queryset.filter(
            tipo_zona_actuacion='ZONAS',
            zonas_definidas__isnull=False
        )
        
        # Filtrar manualmente en Python (simplificado para MVP)
        # En producción, usar Func() o extra() para hacer esto en SQL
        for transportista in queryset_zonas:
            zonas = transportista.zonas_definidas or {}
            if zonas.get('nacional'):
                resultados.append(transportista)
                continue
            
            provincias = zonas.get('provincias', [])
            if not provincias:
                continue
            
            # Buscar coincidencia con provincia o ciudad
            encontrado = False
            if provincia_cliente:
                for provincia in provincias:
                    if provincia_cliente.lower() in str(provincia).lower():
                        encontrado = True
                        break
            if not encontrado and ciudad_cliente:
                for provincia in provincias:
                    if ciudad_cliente.lower() in str(provincia).lower():
                        encontrado = True
                        break
            
            if encontrado:
                resultados.append(transportista)

        # El filtro por categoría ya se hizo arriba (incluyendo descendientes)
        # No necesitamos filtrar de nuevo aquí

        # Ordenar por distancia (si aplica) o por ID
        resultados_con_distancia = [t for t in resultados if hasattr(t, '_distancia_km')]
        resultados_sin_distancia = [t for t in resultados if not hasattr(t, '_distancia_km')]
        
        resultados_con_distancia.sort(key=lambda x: x._distancia_km)
        resultados_sin_distancia.sort(key=lambda x: x.user_id)
        
        resultados = resultados_con_distancia + resultados_sin_distancia

        return [
            self._to_dict(transportista, include_distance=hasattr(transportista, '_distancia_km'))
            for transportista in resultados
        ]

    def find_near_location_by_category(
        self,
        point: Point,
        radius_km: float,
        category_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        MÉTODO OBSOLETO: Usar find_transportistas_por_zona en su lugar.
        Mantenido por compatibilidad temporal.
        """
        logger.warning("find_near_location_by_category está obsoleto. Usar find_transportistas_por_zona.")
        return []

    def save(self, transportista_data: TransportistaData) -> Dict[str, Any]:
        """
        Guarda o actualiza un transportista.
        Si el transportista ya existe (por user_id), lo actualiza.
        Si no existe, lo crea.
        """
        user = User.objects.get(id=transportista_data.user_id)

        lat = None
        lon = None
        if transportista_data.ubicacion:
            lat = transportista_data.ubicacion.latitude
            lon = transportista_data.ubicacion.longitude

        transportista, created = Transportista.objects.get_or_create(
            user=user,
            defaults={
                'disponible': transportista_data.disponible,
                'base_latitud': lat,
                'base_longitud': lon,
                'trial_end': transportista_data.trial_end,
            },
        )

        if not created:
            transportista.disponible = transportista_data.disponible
            transportista.base_latitud = lat
            transportista.base_longitud = lon
            transportista.trial_end = transportista_data.trial_end
            transportista.save()

        if transportista_data.categoria_ids:
            transportista.categorias.set(transportista_data.categoria_ids)

        return self._to_dict(transportista, include_distance=False)

    def update_disponibilidad(self, user_id: int, is_disponible: bool) -> bool:
        """Actualiza el estado de disponibilidad de un transportista."""
        try:
            transportista = Transportista.objects.get(user_id=user_id)
            transportista.disponible = is_disponible
            transportista.save()
            return True
        except Transportista.DoesNotExist:
            return False

    def update_ubicacion(self, user_id: int, point: Point) -> bool:
        """Actualiza la ubicación de un transportista."""
        try:
            transportista = Transportista.objects.get(user_id=user_id)
            transportista.base_latitud = point.latitude
            transportista.base_longitud = point.longitude
            transportista.save()
            return True
        except Transportista.DoesNotExist:
            return False

    def create_user_and_transportista(
        self,
        username: str,
        email: str,
        password: str,
        phone: Optional[str] = None,
        is_transportista: bool = False,
        trial_end: Optional[datetime] = None,
    ) -> Dict[str, Any]:
        """
        Crea un usuario y opcionalmente su perfil de transportista.
        """
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            phone=phone,
        )

        if is_transportista:
            if trial_end and timezone.is_naive(trial_end):
                trial_end = timezone.make_aware(trial_end)

            transportista = Transportista.objects.create(
                user=user,
                disponible=False,
                trial_end=trial_end,
            )
            return self._to_dict(transportista, include_distance=False)

        return {
            'id': user.id,
            'user_id': user.id,
            'disponible': False,
            'base_latitud': None,
            'base_longitud': None,
            'trial_end': None,
            'categoria_ids': [],
            'categorias': [],
            'distancia_km': None,
        }

    def _to_dict(
        self,
        transportista: Transportista,
        include_distance: bool = False,
    ) -> Dict[str, Any]:
        """Convierte un modelo Transportista a un diccionario."""
        base_geocodificada_dict = None
        if transportista.base_latitud and transportista.base_longitud:
            base_geocodificada_dict = {
                'lat': transportista.base_latitud,
                'lon': transportista.base_longitud,
            }

        distancia_km: Optional[float] = None
        if include_distance and hasattr(transportista, '_distancia_km') and transportista._distancia_km is not None:
            distancia_km = round(transportista._distancia_km, 3)

        categorias = [
            {
                'id': categoria.id,
                'nombre': categoria.nombre,
                'descripcion': categoria.descripcion,
                'parent': categoria.parent_id,
            }
            for categoria in transportista.categorias.all()
        ]

        # Obtener maquinaria (TransportistaCategoria)
        from sigot.infrastructure.db.models import TransportistaCategoria
        maquinaria = []
        for tc in transportista.transportistacategoria_set.all():
            maquinaria.append({
                'categoria': {
                    'id': tc.categoria.id,
                    'nombre': tc.categoria.nombre,
                    'descripcion': tc.categoria.descripcion,
                    'parent': tc.categoria.parent_id,
                },
                'radio_km_especifico': tc.radio_km_especifico,
                'nombre_vehiculo': tc.nombre_vehiculo,
                'marca': tc.marca,
                'tonelaje': float(tc.tonelaje) if tc.tonelaje else None,
                'caracteristicas': tc.caracteristicas,
                'imagen_maquina_url': tc.imagen_maquina.url if tc.imagen_maquina else None,
            })

        return {
            'id': transportista.user_id,
            'user_id': transportista.user_id,
            'user': {
                'id': transportista.user_id,
                'username': transportista.user.username,
                'email': transportista.user.email,
                'is_transportista': True,
            },
            'disponible': transportista.disponible,
            'codigo_postal': transportista.codigo_postal,
            'base_geocodificada': base_geocodificada_dict,
            'tipo_zona_actuacion': transportista.tipo_zona_actuacion,
            'radio_km_general': transportista.radio_km_general,
            'zonas_definidas': transportista.zonas_definidas,
            'foto_de_perfil_url': transportista.foto_de_perfil.url if transportista.foto_de_perfil else None,
            'trial_end': transportista.trial_end.isoformat() if transportista.trial_end else None,
            'categoria_ids': [categoria['id'] for categoria in categorias],
            'categorias': categorias,
            'maquinaria': maquinaria,
            'distancia_km': distancia_km,
        }


