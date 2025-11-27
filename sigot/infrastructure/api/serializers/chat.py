"""
Serializers para la API de Chat
"""

from rest_framework import serializers


class ChatParticipantSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    username = serializers.CharField()
    email = serializers.EmailField(allow_blank=True, allow_null=True)
    is_transportista = serializers.BooleanField()
    photo_url = serializers.CharField(allow_null=True, required=False)


class ChatRoomSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    participants = ChatParticipantSerializer(many=True)
    created_at = serializers.CharField(allow_null=True)
    updated_at = serializers.CharField(allow_null=True)

    def to_representation(self, instance):
        """
        Permite serializar dicts emitidos por el repositorio sin transformación adicional.
        """
        return instance



