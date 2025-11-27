"""
Vistas de API para Chat
"""

from typing import List

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from sigot.core.ports import MessageData
from sigot.infrastructure.api.serializers.chat import ChatRoomSerializer
from sigot.infrastructure.repositories.orm_chat_repository import ChatRepositoryORM

User = get_user_model()


class ChatRoomView(APIView):
    """Gestiona la creación y listado de salas de chat."""

    permission_classes = [IsAuthenticated]
    serializer_class = ChatRoomSerializer

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repository = ChatRepositoryORM()

    def get(self, request):
        rooms = self.repository.get_rooms_for_user(request.user.id)
        serializer = self.serializer_class(rooms, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        participant_ids = request.data.get('participant_ids')

        if not isinstance(participant_ids, list) or len(participant_ids) == 0:
            return Response(
                {
                    'error': 'VALIDATION_ERROR',
                    'message': 'El campo participant_ids debe ser una lista de IDs de usuarios',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            typed_participants: List[int] = [int(pid) for pid in participant_ids]
        except (TypeError, ValueError):
            return Response(
                {
                    'error': 'VALIDATION_ERROR',
                    'message': 'Todos los participant_ids deben ser enteros',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        typed_participants.append(request.user.id)
        typed_participants = sorted(set(typed_participants))

        if len(typed_participants) < 2:
            return Response(
                {
                    'error': 'VALIDATION_ERROR',
                    'message': 'Se requiere al menos otro participante además del usuario autenticado',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        participants_qs = User.objects.filter(id__in=typed_participants)
        if participants_qs.count() != len(typed_participants):
            return Response(
                {
                    'error': 'PARTICIPANT_NOT_FOUND',
                    'message': 'Uno o más participantes no existen',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        existing_room = self.repository.find_room_with_participants(typed_participants)
        if existing_room:
            serializer = self.serializer_class(existing_room)
            return Response(serializer.data, status=status.HTTP_200_OK)

        new_room = self.repository.create_room(typed_participants)
        serializer = self.serializer_class(new_room)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ChatMessagesView(APIView):
    """Gestiona la obtención de mensajes de una sala de chat."""

    permission_classes = [IsAuthenticated]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repository = ChatRepositoryORM()

    def get(self, request, room_id: int):
        """
        Obtiene los mensajes de una sala de chat.
        
        Query params:
        - limit: Número máximo de mensajes a retornar (default: 50)
        - offset: Número de mensajes a saltar (default: 0)
        """
        # Verificar que el usuario es participante de la sala
        room = self.repository.get_room_by_id(room_id)
        if not room:
            return Response(
                {
                    'error': 'NOT_FOUND',
                    'message': 'La sala de chat no existe',
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        
        # Verificar que el usuario es participante
        participant_ids = [p['id'] for p in room.get('participants', [])]
        if request.user.id not in participant_ids:
            return Response(
                {
                    'error': 'FORBIDDEN',
                    'message': 'No tienes acceso a esta sala de chat',
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        
        # Obtener parámetros de paginación
        limit = request.query_params.get('limit', 50)
        offset = request.query_params.get('offset', 0)
        
        try:
            limit = int(limit) if limit else 50
            offset = int(offset) if offset else 0
        except (TypeError, ValueError):
            return Response(
                {
                    'error': 'VALIDATION_ERROR',
                    'message': 'Los parámetros limit y offset deben ser enteros',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        # Obtener mensajes
        messages = self.repository.get_messages_for_room(
            room_id=room_id,
            limit=limit,
            offset=offset,
        )
        
        return Response(
            {
                'count': len(messages),
                'results': messages,
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request, room_id: int):
        """
        Envía un mensaje a una sala de chat (soporta archivos).
        
        Body (multipart/form-data):
        - message: Texto del mensaje (opcional si hay archivo)
        - attachment: Archivo adjunto (opcional)
        """
        # Verificar que el usuario es participante de la sala
        room = self.repository.get_room_by_id(room_id)
        if not room:
            return Response(
                {
                    'error': 'NOT_FOUND',
                    'message': 'La sala de chat no existe',
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        
        # Verificar que el usuario es participante
        participant_ids = [p['id'] for p in room.get('participants', [])]
        if request.user.id not in participant_ids:
            return Response(
                {
                    'error': 'FORBIDDEN',
                    'message': 'No tienes acceso a esta sala de chat',
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        message_body = request.data.get('message', '')
        attachment = request.FILES.get('attachment')

        if not message_body and not attachment:
            return Response(
                {
                    'error': 'VALIDATION_ERROR',
                    'message': 'El mensaje debe tener texto o un archivo adjunto',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Guardar mensaje usando el repositorio
        message_data = MessageData(
            chatroom_id=room_id,
            author_id=request.user.id,
            body=message_body,
            attachment_path=attachment,  # Django ORM maneja el archivo directamente
        )
        
        saved_message = self.repository.save_message(message_data)

        # Broadcast a través de WebSocket
        channel_layer = get_channel_layer()
        group_name = f'chat_room_{room_id}'
        
        message_payload = {
            'type': 'chat.message',
            'id': saved_message.get('id'),
            'chatroom_id': room_id,
            'author': saved_message.get('author'),
            'body': saved_message.get('body'),
            'attachment': saved_message.get('attachment'),
            'created_at': saved_message.get('created_at'),
        }
        
        async_to_sync(channel_layer.group_send)(
            group_name,
            message_payload,
        )

        return Response(saved_message, status=status.HTTP_201_CREATED)


class ChatRoomMarkReadView(APIView):
    """
    API View para marcar una sala como leída.
    """
    permission_classes = [IsAuthenticated]
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.repository = ChatRepositoryORM()
    
    def post(self, request, room_id: int):
        """
        Marca la sala como leída actualizando last_read_at.
        """
        # Verificar que el usuario es participante de la sala
        room = self.repository.get_room_by_id(room_id)
        if not room:
            return Response(
                {
                    'error': 'NOT_FOUND',
                    'message': 'La sala de chat no existe',
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        
        # Verificar que el usuario es participante
        participant_ids = [p['id'] for p in room.get('participants', [])]
        if request.user.id not in participant_ids:
            return Response(
                {
                    'error': 'FORBIDDEN',
                    'message': 'No tienes acceso a esta sala de chat',
                },
                status=status.HTTP_403_FORBIDDEN,
            )
        
        # Actualizar last_read_at
        success = self.repository.mark_room_as_read(room_id, request.user.id)
        
        if not success:
            return Response(
                {
                    'error': 'SERVER_ERROR',
                    'message': 'Error al marcar la sala como leída',
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        
        # Broadcast a través de WebSocket
        channel_layer = get_channel_layer()
        group_name = f'chat_room_{room_id}'
        
        mark_read_payload = {
            'type': 'chat.mark_read',
            'room_id': room_id,
            'user_id': request.user.id,
            'marked_at': timezone.now().isoformat(),
        }
        
        async_to_sync(channel_layer.group_send)(
            group_name,
            mark_read_payload,
        )
        
        return Response({'success': True}, status=status.HTTP_200_OK)
