"""
Vistas de API para Categorías
Implementa los endpoints definidos en openapi.yml
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Prefetch
from sigot.infrastructure.db.models import Categoria
from sigot.infrastructure.api.serializers.categorias import CategoriaSerializer


class CategoriaListView(APIView):
    """
    Vista para obtener todas las categorías.
    Endpoint: GET /api/categorias/
    
    Según openapi.yml:
    - Retorna todas las categorías con su estructura jerárquica (árbol de subcategorías)
    - Solo retorna los nodos raíz (parent=None), con todos sus descendientes anidados
    - Soporta jerarquías de N-niveles mediante recursión
    
    NOTA: Endpoint público para permitir que usuarios no autenticados vean las categorías
    disponibles antes de registrarse o iniciar sesión.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        """
        Retorna todas las categorías con su estructura jerárquica.
        
        Solo retorna las categorías raíz (sin parent), que incluyen sus hijos anidados
        de forma recursiva hasta N-niveles.
        
        Optimizado: Carga todas las categorías con prefetch de children para evitar
        consultas N+1. El serializer maneja la recursión de forma eficiente.
        """
        # Obtener solo las categorías raíz (sin parent)
        # Prefetch children para optimizar (evita consultas N+1)
        # Nota: Django no soporta prefetch recursivo directo, pero el serializer
        # manejará la recursión usando los children prefetched cuando estén disponibles
        root_categories = Categoria.objects.filter(
            parent__isnull=True
        ).prefetch_related(
            Prefetch('children', queryset=Categoria.objects.all().prefetch_related('children'))
        ).order_by('nombre')
        
        serializer = CategoriaSerializer(root_categories, many=True)
        return Response(serializer.data)

