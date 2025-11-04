"""
WebSocket consumers for real-time chat functionality.
"""

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import ChatRoom, Message

User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    """
    WebSocket consumer for handling real-time chat messages.
    
    When a user connects to a chat room, they join a channel group.
    Messages sent by any user in the room are broadcast to all participants.
    """
    
    async def connect(self):
        """Handle WebSocket connection"""
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'
        
        # Get the user from the scope (authenticated via JWT)
        self.user = self.scope.get('user')
        
        if not self.user or not self.user.is_authenticated:
            await self.close()
            return
        
        # Verify user is a participant in this room
        is_participant = await self.check_room_participant(self.room_id, self.user.id)
        if not is_participant:
            await self.close()
            return
        
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection"""
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        """
        Receive message from WebSocket.
        Expected format: {"message": "text", "type": "chat_message"}
        """
        data = json.loads(text_data)
        message_content = data.get('message', '')
        message_type = data.get('type', 'chat_message')
        
        if message_type == 'chat_message' and message_content:
            # Save message to database
            message = await self.save_message(
                room_id=self.room_id,
                author_id=self.user.id,
                content=message_content
            )
            
            # Broadcast message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': message_content,
                    'message_id': message.id,
                    'author_id': self.user.id,
                    'author_email': self.user.email,
                    'author_name': f"{self.user.first_name} {self.user.last_name}".strip() or self.user.username,
                    'timestamp': message.timestamp.isoformat(),
                }
            )
        
        elif message_type == 'read_receipt':
            # Mark message as read
            message_id = data.get('message_id')
            if message_id:
                await self.mark_message_read(message_id, self.user.id)
                
                # Broadcast read receipt
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'read_receipt',
                        'message_id': message_id,
                        'reader_id': self.user.id,
                    }
                )
    
    async def chat_message(self, event):
        """
        Receive message from room group and send to WebSocket.
        """
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': event['message'],
            'message_id': event['message_id'],
            'author_id': event['author_id'],
            'author_email': event['author_email'],
            'author_name': event['author_name'],
            'timestamp': event['timestamp'],
        }))
    
    async def read_receipt(self, event):
        """
        Receive read receipt from room group and send to WebSocket.
        """
        await self.send(text_data=json.dumps({
            'type': 'read_receipt',
            'message_id': event['message_id'],
            'reader_id': event['reader_id'],
        }))
    
    @database_sync_to_async
    def check_room_participant(self, room_id, user_id):
        """Check if user is a participant in the chat room"""
        try:
            room = ChatRoom.objects.get(id=room_id)
            return room.participants.filter(id=user_id).exists()
        except ChatRoom.DoesNotExist:
            return False
    
    @database_sync_to_async
    def save_message(self, room_id, author_id, content):
        """Save message to database"""
        room = ChatRoom.objects.get(id=room_id)
        author = User.objects.get(id=author_id)
        message = Message.objects.create(
            room=room,
            author=author,
            content=content
        )
        # Update room's updated_at timestamp
        room.save()
        return message
    
    @database_sync_to_async
    def mark_message_read(self, message_id, user_id):
        """Mark a message as read"""
        try:
            message = Message.objects.get(id=message_id)
            # Only mark as read if the current user is not the author
            if message.author.id != user_id:
                message.read = True
                message.save()
        except Message.DoesNotExist:
            pass

