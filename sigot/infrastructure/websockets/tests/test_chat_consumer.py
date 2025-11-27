"""
Tests de integración para el ChatConsumer de Channels
Estas pruebas deben FALLAR (ROJO) hasta que el Agente de Backend
implemente el consumer WebSocket.
"""

import json
import pytest
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model
from django.utils import timezone

from sigot.infrastructure.db.models import ChatRoom, Transportista, Message
from sigot.boot.asgi import application

User = get_user_model()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_connect_falla_sin_autenticacion():
    """La conexión debe ser rechazada si no hay usuario autenticado."""
    communicator = WebsocketCommunicator(application, "/ws/chat/1/")

    connected, _ = await communicator.connect()

    assert connected is False, (
        "La conexión WebSocket debe ser rechazada cuando no hay usuario autenticado"
    )
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_connect_falla_si_usuario_no_es_participante():
    """La conexión debe fallar si el usuario no pertenece a la sala."""
    usuario_a = User.objects.create_user(
        username="usuario_a",
        email="usuario_a@example.com",
        password="password123",
    )
    user_t1 = User.objects.create_user(
        username="transportista_1",
        email="t1@example.com",
        password="password123",
    )
    transportista_1 = Transportista.objects.create(
        user=user_t1,
        disponible=True,
        ubicacion=None,
        trial_end=timezone.now(),
    )
    malicious_user = User.objects.create_user(
        username="malicioso",
        email="mal@example.com",
        password="password123",
    )

    sala = ChatRoom.objects.create()
    sala.participants.add(usuario_a, transportista_1.user)

    communicator = WebsocketCommunicator(application, f"/ws/chat/{sala.id}/")
    communicator.scope["user"] = malicious_user

    connected, _ = await communicator.connect()

    assert connected is False, (
        "La conexión debe ser rechazada para usuarios que no son participantes de la sala"
    )
    await communicator.disconnect()


@pytest.mark.asyncio
@pytest.mark.django_db(transaction=True)
async def test_envio_de_mensaje_se_guarda_en_bd_y_se_emite():
    """El consumer debe persistir y retransmitir los mensajes enviados."""
    usuario_a = User.objects.create_user(
        username="usuario_a",
        email="usuario_a@example.com",
        password="password123",
    )
    user_t1 = User.objects.create_user(
        username="transportista_1",
        email="t1@example.com",
        password="password123",
    )
    transportista_1 = Transportista.objects.create(
        user=user_t1,
        disponible=True,
        ubicacion=None,
        trial_end=timezone.now(),
    )

    sala = ChatRoom.objects.create()
    sala.participants.add(usuario_a, transportista_1.user)

    communicator = WebsocketCommunicator(application, f"/ws/chat/{sala.id}/")
    communicator.scope["user"] = usuario_a

    connected, _ = await communicator.connect()
    assert connected is True, "La conexión debe ser aceptada para participantes válidos"

    initial_messages = Message.objects.count()

    payload = {
        "type": "chat.message",
        "message": "Hola desde el test",
    }

    await communicator.send_json_to(payload)

    response = await communicator.receive_json_from()

    assert response == payload, (
        "El consumer debe emitir el mismo payload enviado por el cliente",
    )

    final_messages = Message.objects.count()
    assert final_messages == initial_messages + 1, (
        "El mensaje enviado debe persistirse en la base de datos"
    )

    await communicator.disconnect()

