from django.urls import path

from sigot.infrastructure.websockets.consumers import ChatConsumer

websocket_urlpatterns = [
    path('ws/chat/<int:room_id>/', ChatConsumer.as_asgi(), name='ws-chat-room'),
]

