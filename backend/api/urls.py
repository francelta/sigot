"""
API URL Configuration for ConnecMaq.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    ConstructorProfileViewSet,
    ProviderProfileViewSet,
    MachineViewSet,
    ChatRoomViewSet,
    MessageViewSet
)

# Router for ViewSets
router = DefaultRouter()

# Register all ViewSets
router.register(r'users', UserViewSet, basename='user')
router.register(r'constructor-profiles', ConstructorProfileViewSet, basename='constructor-profile')
router.register(r'providers', ProviderProfileViewSet, basename='provider')
router.register(r'machines', MachineViewSet, basename='machine')
router.register(r'chat-rooms', ChatRoomViewSet, basename='chat-room')
router.register(r'messages', MessageViewSet, basename='message')

# URL patterns
urlpatterns = [
    # Include router URLs
    path('', include(router.urls)),
]

