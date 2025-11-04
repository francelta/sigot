"""
WebSocket URL routing for Django Channels.
This file defines the WebSocket routes for real-time chat functionality.
"""

from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_id>\d+)/$', consumers.ChatConsumer.as_asgi()),
]

