"""
URLs de la API
Define las rutas para los endpoints de la API REST
"""

from django.urls import path

from sigot.infrastructure.api.views.auth import RegisterView, LoginView
from sigot.infrastructure.api.views.transportistas import (
    TransportistasCercanosView,
    MiPerfilView,
)
from sigot.infrastructure.api.views.chat import ChatRoomView, ChatMessagesView, ChatRoomMarkReadView
from sigot.infrastructure.api.views.categorias import CategoriaListView
from sigot.infrastructure.api.views.onboarding import OnboardingCompleteView

app_name = 'api'

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='auth-register'),
    path('auth/login/', LoginView.as_view(), name='auth-login'),
    path(
        'transportistas/cercanos/',
        TransportistasCercanosView.as_view(),
        name='transportistas-cercanos',
    ),
    path(
        'transportistas/mi-perfil/',
        MiPerfilView.as_view(),
        name='transportistas-mi-perfil',
    ),
    path('categorias/', CategoriaListView.as_view(), name='categorias-list'),
    path('chat/rooms/', ChatRoomView.as_view(), name='chat-rooms'),
    path(
        'chat/rooms/<int:room_id>/messages/',
        ChatMessagesView.as_view(),
        name='chat-messages',
    ),
    path(
        'chat/rooms/<int:room_id>/mark_read/',
        ChatRoomMarkReadView.as_view(),
        name='chat-mark-read',
    ),
    path(
        'onboarding/complete/',
        OnboardingCompleteView.as_view(),
        name='onboarding-complete',
    ),
]

