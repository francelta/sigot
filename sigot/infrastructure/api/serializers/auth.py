"""
Serializers para Autenticación
Basados en el contrato OpenAPI definido en openapi.yml
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    """
    Serializer para registro de usuarios.
    Valida los datos según el esquema RegisterRequest de openapi.yml
    """
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        style={'input_type': 'password'}
    )
    is_transportista = serializers.BooleanField(
        required=True,
        help_text='Si es true, se crea un perfil de transportista con período de prueba de 3 meses'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'phone', 'is_transportista')
        extra_kwargs = {
            'username': {'min_length': 3, 'max_length': 150},
            'email': {'required': True},
            'phone': {'required': False, 'allow_blank': True, 'allow_null': True},
        }

    def validate_email(self, value):
        """Valida que el email sea único."""
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Este email ya está registrado.")
        return value

    def validate_username(self, value):
        """Valida que el username sea único."""
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Este nombre de usuario ya está registrado.")
        return value


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer para representar un usuario.
    Usado en las respuestas de autenticación según el esquema User de openapi.yml
    """
    is_transportista = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'phone', 'is_transportista', 'created_at')
        read_only_fields = ('id', 'created_at')

    def get_is_transportista(self, obj):
        """Determina si el usuario es transportista."""
        return hasattr(obj, 'transportista')


class AuthResponseSerializer(serializers.Serializer):
    """
    Serializer para la respuesta de autenticación.
    Según el esquema AuthResponse de openapi.yml
    """
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True, required=False)
    user = UserSerializer(read_only=True)


