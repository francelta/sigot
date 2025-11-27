"""
Vistas de API para Transportistas
"""

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from sigot.infrastructure.api.serializers.transportistas import (
    TransportistaListSerializer,
)
from sigot.infrastructure.repositories.orm_transportista_repository import (
    TransportistaRepositoryORM,
)
from sigot.infrastructure.db.models import Transportista


class TransportistasCercanosView(APIView):
    """
    Endpoint: GET /api/transportistas/cercanos/
    Busca transportistas por zona de actuación.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = TransportistaListSerializer

    def get(self, request):
        query_param = request.query_params.get('q')
        categoria_param = request.query_params.get('categoria')

        if query_param is None or query_param.strip() == '':
            return Response(
                {
                    'error': 'VALIDATION_ERROR',
                    'message': 'El parámetro q (consulta de búsqueda) es obligatorio',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        category_id = None
        if categoria_param is not None:
            try:
                category_id = int(categoria_param)
            except (TypeError, ValueError):
                return Response(
                    {
                        'error': 'VALIDATION_ERROR',
                        'message': 'El parámetro categoria debe ser entero',
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        repository = TransportistaRepositoryORM()
        transportistas_dicts = repository.find_transportistas_por_zona(
            query_location_str=query_param.strip(),
            category_id=category_id,
        )

        # El repositorio retorna diccionarios, pero el serializer espera instancias
        # Necesitamos obtener las instancias reales para serializar correctamente
        transportista_ids = [t['id'] for t in transportistas_dicts]
        transportistas_instances = Transportista.objects.filter(
            user_id__in=transportista_ids
        ).select_related('user').prefetch_related(
            'categorias', 'transportistacategoria_set', 'transportistacategoria_set__categoria'
        )
        
        # Mantener el orden original
        transportistas_ordered = []
        for t_dict in transportistas_dicts:
            for t_instance in transportistas_instances:
                if t_instance.user_id == t_dict['id']:
                    # Añadir distancia si existe
                    if 'distancia_km' in t_dict and t_dict['distancia_km']:
                        t_instance.distancia_km = t_dict['distancia_km']
                    transportistas_ordered.append(t_instance)
                    break

        serializer = self.serializer_class(
            transportistas_ordered, 
            many=True,
            context={'request': request}
        )
        data = {
            'count': len(serializer.data),
            'results': serializer.data,
        }
        return Response(data, status=status.HTTP_200_OK)


class MiPerfilView(APIView):
    """
    Endpoint: GET /api/transportistas/mi-perfil/ - Obtiene el perfil del transportista
    Endpoint: PATCH /api/transportistas/mi-perfil/ - Actualiza el perfil del transportista (categorías).
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Obtiene el perfil del transportista autenticado.
        """
        try:
            transportista = Transportista.objects.get(user=request.user)
        except Transportista.DoesNotExist:
            return Response(
                {
                    'error': 'NOT_FOUND',
                    'message': 'No se encontró el perfil de transportista',
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = TransportistaListSerializer([transportista], many=True)
        return Response(serializer.data[0], status=status.HTTP_200_OK)

    def patch(self, request):
        categoria_ids = request.data.get('categoria_ids', [])

        if not isinstance(categoria_ids, list):
            return Response(
                {
                    'error': 'VALIDATION_ERROR',
                    'message': 'categoria_ids debe ser una lista',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            transportista = Transportista.objects.get(user=request.user)
        except Transportista.DoesNotExist:
            return Response(
                {
                    'error': 'NOT_FOUND',
                    'message': 'No se encontró el perfil de transportista',
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        # Validar que todas las categorías existen
        from sigot.infrastructure.db.models import Categoria
        categorias_validas = Categoria.objects.filter(id__in=categoria_ids)
        if categorias_validas.count() != len(categoria_ids):
            return Response(
                {
                    'error': 'VALIDATION_ERROR',
                    'message': 'Una o más categorías no existen',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Actualizar categorías
        transportista.categorias.set(categoria_ids)
        transportista.save()

        return Response(
            {'message': 'Perfil actualizado correctamente'},
            status=status.HTTP_200_OK,
        )
