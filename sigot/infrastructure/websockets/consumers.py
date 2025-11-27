"""Consumers de WebSocket para el módulo de chat."""

from typing import Any, Dict

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async

from sigot.infrastructure.repositories.orm_chat_repository import ChatRepositoryORM
from sigot.core.ports import MessageData


class ChatConsumer(AsyncJsonWebsocketConsumer):
    """Consumer de chat en tiempo real."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_id: int | None = None
        self.group_name: str | None = None
        self.repository = ChatRepositoryORM()

    async def connect(self) -> None:
        """Gestiona la conexión entrante."""
        user = self.scope.get('user')
        room_id = self.scope['url_route']['kwargs'].get('room_id')

        # Aceptar la conexión primero para poder enviar mensajes de error si es necesario
        await self.accept()

        if not user or not user.is_authenticated:
            await self.close(code=4001)  # Unauthorized
            return

        if room_id is None:
            await self.close(code=4002)  # Bad request
            return

        self.room_id = int(room_id)
        self.group_name = f'chat_room_{self.room_id}'

        room = await database_sync_to_async(self.repository.get_room_by_id)(self.room_id)
        if room is None:
            await self.close(code=4004)  # Not found
            return

        participant_ids = {participant['id'] for participant in room.get('participants', [])}
        if user.id not in participant_ids:
            await self.close(code=4003)  # Forbidden
            return

        await self.channel_layer.group_add(self.group_name, self.channel_name)

    async def disconnect(self, code: int) -> None:
        """Gestiona la desconexión."""
        if self.group_name:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, content: Dict[str, Any], *, close: bool = False) -> None:
        """Procesa mensajes entrantes."""
        if not self.room_id:
            return

        user = self.scope.get('user')
        if not user or not user.is_authenticated:
            return

        message_body = content.get('message')
        if not message_body:
            return

        message_data = MessageData(
            chatroom_id=self.room_id,
            author_id=user.id,
            body=message_body,
            attachment_path=None,
        )
        saved_message = await database_sync_to_async(self.repository.save_message)(message_data)

        # Send the full message details to all participants
        message_payload = {
            'type': 'chat.message',
            'id': saved_message.get('id'),
            'chatroom_id': self.room_id,
            'author': saved_message.get('author', {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }),
            'body': saved_message.get('body', message_body),
            'attachment': saved_message.get('attachment'),
            'created_at': saved_message.get('created_at'),
        }
        
        await self.channel_layer.group_send(
            self.group_name,
            message_payload,
        )

    async def chat_message(self, event: Dict[str, Any]) -> None:
        """Envía el mensaje al cliente."""
        await self.send_json(event)

    async def chat_mark_read(self, event: Dict[str, Any]) -> None:
        """Envía el evento de marca como leído al cliente."""
        await self.send_json(event)
