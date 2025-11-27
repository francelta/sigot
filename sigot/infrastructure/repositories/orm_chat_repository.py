"""
Repositorio ORM para Chat
Implementa ChatRepositoryPort usando Django ORM
"""

from typing import List, Dict, Any, Optional

from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Count

from sigot.core.ports import ChatRepositoryPort, MessageData
from sigot.infrastructure.db.models import ChatRoom, Message


User = get_user_model()


class ChatRepositoryORM(ChatRepositoryPort):
    """
    Implementación ORM del ChatRepositoryPort.
    """

    def get_room_by_id(self, room_id: int) -> Optional[Dict[str, Any]]:
        try:
            room = (
                self._base_queryset()
                .filter(id=room_id)
                .first()
            )
            if room is None:
                return None
            return self._to_dict(room, include_last_message=True)
        except ChatRoom.DoesNotExist:
            return None

    def get_rooms_for_user(self, user_id: int) -> List[Dict[str, Any]]:
        rooms = (
            self._base_queryset()
            .filter(participants__id=user_id)
            .distinct()
        )
        return [self._to_dict(room, include_last_message=True) for room in rooms]

    def create_room(self, participant_ids: List[int]) -> Dict[str, Any]:
        participant_ids = sorted(set(participant_ids))

        with transaction.atomic():
            participants = list(User.objects.filter(id__in=participant_ids))
            if len(participants) != len(participant_ids):
                raise ValueError("Uno o más participantes no existen")

            room = ChatRoom.objects.create()
            room.participants.add(*participants)

        room = self._base_queryset().get(id=room.id)
        return self._to_dict(room)

    # Métodos adicionales (no definidos en el puerto) pero útiles para la API
    def find_room_with_participants(
        self,
        participant_ids: List[int],
    ) -> Optional[Dict[str, Any]]:
        participant_ids = sorted(set(participant_ids))
        participant_count = len(participant_ids)

        if participant_count == 0:
            return None

        rooms = (
            self._base_queryset()
            .annotate(num_participants=Count('participants'))
            .filter(num_participants=participant_count)
        )

        for participant_id in participant_ids:
            rooms = rooms.filter(participants__id=participant_id)

        room = rooms.distinct().first()
        if room is None:
            return None
        return self._to_dict(room)

    # Métodos aún no implementados (no requeridos por las pruebas actuales)
    def save_message(self, message_data: MessageData) -> Dict[str, Any]:
        chatroom = ChatRoom.objects.get(id=message_data.chatroom_id)
        author = User.objects.get(id=message_data.author_id)

        message = Message.objects.create(
            chatroom=chatroom,
            author=author,
            body=message_data.body,
            attachment=message_data.attachment_path,  # Django FileField handles path or file object
        )

        return self._message_to_dict(message)

    def get_messages_for_room(
        self,
        room_id: int,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        # Ordenar por fecha de creación descendente (más recientes primero)
        # Luego invertir para mostrar los más antiguos primero (como en WhatsApp)
        # IMPORTANTE: Usar select_related para cargar el author en una sola query
        queryset = Message.objects.filter(chatroom_id=room_id).select_related('author').order_by('-created_at')

        if limit:
            queryset = queryset[:limit]
        if offset:
            queryset = queryset[offset:]

        # Invertir para mostrar los más antiguos primero
        messages = list(queryset)
        messages.reverse()
        
        result = [self._message_to_dict(message) for message in messages]
        # Debug: Verificar que todos los mensajes tengan author
        for msg_dict in result:
            if not msg_dict.get('author') or not msg_dict['author'].get('id'):
                import logging
                logger = logging.getLogger(__name__)
                logger.warning(f"Message {msg_dict.get('id')} missing author: {msg_dict}")
        
        return result

    # Utilidades internas
    def _base_queryset(self):
        return ChatRoom.objects.prefetch_related('participants').order_by('-updated_at')

    def _to_dict(self, room: ChatRoom, include_last_message: bool = False) -> Dict[str, Any]:
        participants = []
        for participant in room.participants.all():
            participants.append(
                {
                    'id': participant.id,
                    'username': participant.username,
                    'email': participant.email,
                    'is_transportista': hasattr(participant, 'transportista'),
                    'photo_url': self._get_user_photo_url(participant),
                }
            )

        room_dict = {
            'id': room.id,
            'participants': participants,
            'created_at': room.created_at.isoformat() if room.created_at else None,
            'updated_at': room.updated_at.isoformat() if room.updated_at else None,
        }
        
        # Include last message if requested
        if include_last_message:
            last_message = Message.objects.filter(chatroom_id=room.id).order_by('-created_at').first()
            if last_message:
                room_dict['last_message'] = self._message_to_dict(last_message)
            else:
                room_dict['last_message'] = None
        
        return room_dict

    def _message_to_dict(self, message: Message) -> Dict[str, Any]:
        # Ensure author is loaded
        if not hasattr(message, 'author') or message.author is None:
            import logging
            logger = logging.getLogger(__name__)
            logger.error(f"Message {message.id} has no author!")
            return {
                'id': message.id,
                'chatroom_id': message.chatroom_id,
                'author': {
                    'id': 0,
                    'username': 'Unknown',
                    'email': '',
                    'is_transportista': False,
                },
                'body': message.body,
                'attachment': message.attachment.url if message.attachment else None,
                'created_at': message.created_at.isoformat() if message.created_at else None,
                'updated_at': message.updated_at.isoformat() if message.updated_at else None,
            }
        
        return {
            'id': message.id,
            'chatroom_id': message.chatroom_id,
            'author': {
                'id': message.author.id,
                'username': message.author.username,
                'email': message.author.email,
                'is_transportista': hasattr(message.author, 'transportista'),
                'photo_url': self._get_user_photo_url(message.author),
            },
            'body': message.body,
            'attachment': message.attachment.url if message.attachment else None,
            'created_at': message.created_at.isoformat() if message.created_at else None,
            'updated_at': message.updated_at.isoformat() if message.updated_at else None,
        }

    def _get_user_photo_url(self, user) -> Optional[str]:
        if hasattr(user, 'transportista') and user.transportista.foto_de_perfil:
            try:
                return user.transportista.foto_de_perfil.url
            except ValueError:
                # Handle case where file doesn't exist
                return None
        return None



    def mark_room_as_read(self, room_id: int, user_id: int) -> bool:
        """
        Marca una sala como leída actualizando last_read_at.
        Retorna True si se actualizó correctamente.
        """
        from sigot.infrastructure.db.models import UserChatSettings
        from django.utils import timezone
        
        try:
            settings, created = UserChatSettings.objects.get_or_create(
                chatroom_id=room_id,
                user_id=user_id,
                defaults={'last_read_at': timezone.now()}
            )
            
            if not created:
                settings.last_read_at = timezone.now()
                settings.save(update_fields=['last_read_at'])
            
            return True
        except Exception as e:
            print(f"Error marking room as read: {e}")
            return False
