"""
Serializers para Categorías
Basados en el contrato OpenAPI definido en openapi.yml

Soporta jerarquías de N-niveles mediante recursión verdadera.
"""

from rest_framework import serializers
from sigot.infrastructure.db.models import Categoria


class CategoriaSerializer(serializers.ModelSerializer):
    """
    Serializer recursivo para categorías con soporte de jerarquías N-niveles.
    
    Este serializer se incluye a sí mismo en el campo 'children', permitiendo
    estructuras de árbol de profundidad arbitraria.
    
    Según el esquema Categoria de openapi.yml:
    - Soporta recursión infinita (N-niveles)
    - Optimizado con prefetch_related para evitar consultas N+1
    """
    parent = serializers.IntegerField(source='parent_id', read_only=True, allow_null=True)
    children = serializers.SerializerMethodField()

    class Meta:
        model = Categoria
        fields = ('id', 'nombre', 'descripcion', 'parent', 'children')
        read_only_fields = ('id',)

    def get_children(self, obj):
        """
        Retorna las subcategorías (hijos) de esta categoría de forma recursiva.
        
        Si el objeto tiene 'children' prefetched (optimización), los usa.
        Si no, hace una consulta. El serializer se llama recursivamente
        para cada nivel de la jerarquía.
        """
        # Intentar usar children prefetched si están disponibles
        if hasattr(obj, '_prefetched_objects_cache') and 'children' in obj._prefetched_objects_cache:
            children = obj._prefetched_objects_cache['children']
        else:
            children = obj.children.all()
        
        if children.exists():
            # Llamada recursiva: el serializer se incluye a sí mismo
            # Esto permite estructuras de N-niveles
            return CategoriaSerializer(children, many=True, context=self.context).data
        return []

