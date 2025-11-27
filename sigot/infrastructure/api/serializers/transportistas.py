"""
Serializers para Transportistas
"""

from rest_framework import serializers

from sigot.infrastructure.api.serializers.auth import UserSerializer


class UbicacionField(serializers.Field):
    """
    Campo personalizado para representar el Point del dominio.
    """

    def to_representation(self, value):
        if value is None:
            return None

        lat = getattr(value, 'latitude', None)
        lon = getattr(value, 'longitude', None)

        if lat is None or lon is None:
            return None

        return {
            'lat': float(lat),
            'lon': float(lon),
        }

    def to_internal_value(self, data):
        raise NotImplementedError('UbicacionField es de solo lectura')


class CategoriaSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nombre = serializers.CharField()
    descripcion = serializers.CharField(allow_null=True)
    parent = serializers.IntegerField(allow_null=True)


class TransportistaCategoriaSerializer(serializers.Serializer):
    """
    Serializer para TransportistaCategoria (máquina del transportista).
    """
    categoria = CategoriaSerializer()
    radio_km_especifico = serializers.IntegerField(allow_null=True)
    nombre_vehiculo = serializers.CharField(allow_null=True, allow_blank=True)
    marca = serializers.CharField(allow_null=True, allow_blank=True)
    tonelaje = serializers.DecimalField(max_digits=10, decimal_places=2, allow_null=True)
    caracteristicas = serializers.CharField(allow_null=True, allow_blank=True)
    imagen_maquina = serializers.ImageField(allow_null=True, read_only=True)
    imagen_maquina_url = serializers.SerializerMethodField()

    def get_imagen_maquina_url(self, obj):
        """Retorna la URL de la imagen de la máquina si existe."""
        if obj.imagen_maquina:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.imagen_maquina.url)
            return obj.imagen_maquina.url
        return None


class TransportistaListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    user = UserSerializer()
    disponible = serializers.BooleanField()
    codigo_postal = serializers.CharField(allow_null=True, required=False)
    base_geocodificada = serializers.DictField(allow_null=True, required=False)
    tipo_zona_actuacion = serializers.CharField(required=False)
    radio_km_general = serializers.IntegerField(allow_null=True, required=False)
    zonas_definidas = serializers.DictField(allow_null=True, required=False)
    foto_de_perfil = serializers.ImageField(allow_null=True, read_only=True)
    foto_de_perfil_url = serializers.SerializerMethodField()
    ubicacion = UbicacionField(required=False, allow_null=True)
    trial_end = serializers.DateTimeField(allow_null=True)
    categorias = CategoriaSerializer(many=True)
    maquinaria = TransportistaCategoriaSerializer(many=True, required=False)
    distancia_km = serializers.FloatField(allow_null=True, required=False)

    def get_foto_de_perfil_url(self, obj):
        """Retorna la URL de la foto de perfil si existe."""
        if obj.foto_de_perfil:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.foto_de_perfil.url)
            return obj.foto_de_perfil.url
        return None

    def to_representation(self, instance):
        """
        Serializa una instancia de Transportista a dict.
        """
        data = {
            'id': instance.user_id,  # Transportista usa user_id como primary_key
            'user_id': instance.user_id,
            'user': UserSerializer(instance.user).data,
            'disponible': instance.disponible,
            'codigo_postal': instance.codigo_postal,
            'tipo_zona_actuacion': instance.tipo_zona_actuacion,
            'radio_km_general': instance.radio_km_general,
            'zonas_definidas': instance.zonas_definidas,
            'trial_end': instance.trial_end,
            'categorias': [
                {
                    'id': cat.id,
                    'nombre': cat.nombre,
                    'descripcion': cat.descripcion,
                    'parent': cat.parent_id
                }
                for cat in instance.categorias.all()
            ],
            'maquinaria': [
                {
                    'categoria': {
                        'id': tc.categoria.id,
                        'nombre': tc.categoria.nombre,
                        'descripcion': tc.categoria.descripcion,
                        'parent': tc.categoria.parent_id
                    },
                    'radio_km_especifico': tc.radio_km_especifico,
                    'nombre_vehiculo': tc.nombre_vehiculo,
                    'marca': tc.marca,
                    'tonelaje': float(tc.tonelaje) if tc.tonelaje else None,
                    'caracteristicas': tc.caracteristicas,
                    'imagen_maquina_url': (
                        self.context['request'].build_absolute_uri(tc.imagen_maquina.url)
                        if tc.imagen_maquina and self.context.get('request')
                        else (tc.imagen_maquina.url if tc.imagen_maquina else None)
                    )
                }
                for tc in instance.transportistacategoria_set.all()
            ],
        }

        # Añadir base_geocodificada si existe
        if instance.base_geocodificada:
            data['base_geocodificada'] = {
                'lat': instance.base_geocodificada.y,
                'lon': instance.base_geocodificada.x
            }
        else:
            data['base_geocodificada'] = None

        # Añadir ubicacion (alias de base_geocodificada) para compatibilidad
        if instance.base_geocodificada:
            data['ubicacion'] = {
                'lat': instance.base_geocodificada.y,
                'lon': instance.base_geocodificada.x
            }
        else:
            data['ubicacion'] = None

        # Añadir foto_de_perfil_url
        if instance.foto_de_perfil:
            request = self.context.get('request')
            if request:
                data['foto_de_perfil_url'] = request.build_absolute_uri(instance.foto_de_perfil.url)
            else:
                data['foto_de_perfil_url'] = instance.foto_de_perfil.url
        else:
            data['foto_de_perfil_url'] = None

        return data

