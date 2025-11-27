"""
Tests de API para Chat (E2E)
Valida el contrato definido en openapi.yml para gestión de salas de chat

Estas pruebas deben FALLAR (ROJO) hasta que el Agente de Backend implemente los endpoints.
"""

import pytest
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

from sigot.infrastructure.db.models import ChatRoom, UserChatSettings, Transportista

User = get_user_model()


@pytest.mark.api
class TestChatAPI:
    """
    Suite de pruebas para los endpoints de chat.
    Valida el contrato OpenAPI definido por el Arquitecto.
    """

    @pytest.fixture
    def api_client(self):
        """Cliente API para hacer peticiones HTTP."""
        return APIClient()

    @pytest.fixture
    def authenticated_client(self, api_client):
        """
        Helper para crear un cliente API autenticado.
        Crea un usuario y retorna el cliente con token JWT.
        """
        user = User.objects.create_user(
            username='test_user',
            email='test@example.com',
            password='password123'
        )
        refresh = RefreshToken.for_user(user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        return api_client

    @pytest.fixture
    def usuario_y_transportistas(self, db):
        """
        Fixture que crea un usuario (Usuario A) y 2 transportistas (T1, T2).
        """
        usuario_a = User.objects.create_user(
            username='usuario_a',
            email='usuario_a@example.com',
            password='password123'
        )
        
        # Crear transportistas
        user_t1 = User.objects.create_user(
            username='transportista_1',
            email='t1@example.com',
            password='password123'
        )
        transportista_1 = Transportista.objects.create(
            user=user_t1,
            disponible=True,
            ubicacion=None,
            trial_end=None
        )
        
        user_t2 = User.objects.create_user(
            username='transportista_2',
            email='t2@example.com',
            password='password123'
        )
        transportista_2 = Transportista.objects.create(
            user=user_t2,
            disponible=True,
            ubicacion=None,
            trial_end=None
        )
        
        return {
            'usuario_a': usuario_a,
            'transportista_1': transportista_1,
            'transportista_2': transportista_2,
        }

    @pytest.mark.django_db
    def test_get_chat_rooms_falla_sin_autenticacion(self, api_client):
        """
        Test que valida que el endpoint requiere autenticación.
        
        Según openapi.yml:
        - El endpoint requiere autenticación (security: bearerAuth)
        - Debe devolver 401 Unauthorized cuando no hay token
        """
        # Hacemos la petición GET sin autenticación
        response = api_client.get('/api/chat/rooms/')

        # VALIDACIÓN DEL CONTRATO:
        # Según openapi.yml, debe devolver 401 Unauthorized
        assert response.status_code == status.HTTP_401_UNAUTHORIZED, (
            f"El endpoint debe devolver 401 Unauthorized sin autenticación, "
            f"pero devolvió {response.status_code}"
        )

    @pytest.mark.django_db
    def test_get_chat_rooms_devuelve_lista_de_usuario(
        self,
        api_client,
        usuario_y_transportistas
    ):
        """
        Test que valida que el endpoint GET /chat/rooms/ devuelve las salas del usuario.
        
        Según openapi.yml:
        - Endpoint: GET /chat/rooms/
        - Respuesta esperada: 200 OK con array de ChatRoom
        - Esta prueba FALLARÁ (ROJO) porque el endpoint aún no existe (404)
        """
        usuario_a = usuario_y_transportistas['usuario_a']
        transportista_1 = usuario_y_transportistas['transportista_1']
        transportista_2 = usuario_y_transportistas['transportista_2']

        # Crear 2 ChatRoom en la BBDD: una entre (A y T1), y otra entre (A y T2)
        sala_1 = ChatRoom.objects.create()
        sala_1.participants.add(usuario_a, transportista_1.user)
        
        sala_2 = ChatRoom.objects.create()
        sala_2.participants.add(usuario_a, transportista_2.user)

        # Autenticar como Usuario A
        refresh = RefreshToken.for_user(usuario_a)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        # Hacemos la petición GET al endpoint
        response = api_client.get('/api/chat/rooms/')

        # VALIDACIÓN DEL CONTRATO:
        # Según openapi.yml, debe devolver 200 OK
        assert response.status_code == status.HTTP_200_OK, (
            f"El endpoint /chat/rooms/ debe devolver 200 OK, "
            f"pero devolvió {response.status_code}. "
            f"Respuesta: {response.data if hasattr(response, 'data') else response.content}"
        )

        # VALIDACIÓN DE LA ESTRUCTURA DE RESPUESTA:
        # Según openapi.yml, la respuesta debe ser un array de ChatRoom
        assert isinstance(response.data, list), (
            "La respuesta debe ser una lista según el esquema de OpenAPI"
        )

        # VALIDACIÓN DE LA LÓGICA DE NEGOCIO:
        # Debe devolver 2 salas (las que incluyen al Usuario A)
        assert len(response.data) == 2, (
            f"Debe devolver 2 salas de chat para el usuario A, "
            f"pero devolvió {len(response.data)}"
        )

        # Verificar que las salas retornadas son las correctas
        sala_ids = [sala.get('id') for sala in response.data]
        assert sala_1.id in sala_ids, (
            f"La respuesta debe incluir la sala 1 (ID: {sala_1.id})"
        )
        assert sala_2.id in sala_ids, (
            f"La respuesta debe incluir la sala 2 (ID: {sala_2.id})"
        )

        # VALIDACIÓN DE LA ESTRUCTURA DE CADA ITEM:
        # Según openapi.yml, cada item debe tener el esquema ChatRoom
        if len(response.data) > 0:
            sala = response.data[0]
            assert 'id' in sala, (
                "Cada sala debe tener un campo 'id'"
            )
            assert 'participants' in sala, (
                "Cada sala debe tener el campo 'participants'"
            )
            assert 'created_at' in sala, (
                "Cada sala debe tener el campo 'created_at'"
            )

    @pytest.mark.django_db
    def test_start_chat_room_crea_una_nueva_sala(
        self,
        api_client,
        usuario_y_transportistas
    ):
        """
        Test que valida que el endpoint POST /chat/rooms/ crea una nueva sala.
        
        Según openapi.yml:
        - Endpoint: POST /chat/rooms/
        - Request body: {"participant_ids": [id1, id2, ...]}
        - Respuesta esperada: 201 Created con ChatRoom
        - Esta prueba FALLARÁ (ROJO) porque el endpoint aún no existe (404)
        """
        usuario_a = usuario_y_transportistas['usuario_a']
        transportista_1 = usuario_y_transportistas['transportista_1']

        # Verificar que inicialmente no hay salas
        initial_count = ChatRoom.objects.count()
        assert initial_count == 0, (
            "No debe haber salas de chat al inicio del test"
        )

        # Autenticar como Usuario A
        refresh = RefreshToken.for_user(usuario_a)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        # Hacemos la petición POST al endpoint
        # Según openapi.yml, el payload debe ser {"participant_ids": [id1, id2]}
        # Incluimos al usuario autenticado y al transportista
        payload = {
            'participant_ids': [usuario_a.id, transportista_1.user.id]
        }
        response = api_client.post('/api/chat/rooms/', payload, format='json')

        # VALIDACIÓN DEL CONTRATO:
        # Según openapi.yml, debe devolver 201 Created
        assert response.status_code == status.HTTP_201_CREATED, (
            f"El endpoint /chat/rooms/ debe devolver 201 Created, "
            f"pero devolvió {response.status_code}. "
            f"Respuesta: {response.data if hasattr(response, 'data') else response.content}"
        )

        # VALIDACIÓN DE LA LÓGICA DE NEGOCIO:
        # Debe haberse creado una nueva ChatRoom en la BBDD
        final_count = ChatRoom.objects.count()
        assert final_count == initial_count + 1, (
            f"Debe haberse creado 1 nueva sala de chat. "
            f"Inicial: {initial_count}, Final: {final_count}"
        )

        # Verificar que la sala creada tiene los participantes correctos
        nueva_sala = ChatRoom.objects.latest('created_at')
        participantes = list(nueva_sala.participants.values_list('id', flat=True))
        assert usuario_a.id in participantes, (
            f"La sala debe incluir al Usuario A (ID: {usuario_a.id})"
        )
        assert transportista_1.user.id in participantes, (
            f"La sala debe incluir al Transportista 1 (ID: {transportista_1.user.id})"
        )
        assert len(participantes) == 2, (
            f"La sala debe tener exactamente 2 participantes, "
            f"pero tiene {len(participantes)}"
        )

        # VALIDACIÓN DE LA ESTRUCTURA DE RESPUESTA:
        # Según openapi.yml, la respuesta debe tener el esquema ChatRoom
        assert 'id' in response.data, (
            "La respuesta debe incluir el campo 'id' según ChatRoom"
        )
        assert response.data['id'] == nueva_sala.id, (
            f"El ID de la respuesta debe coincidir con la sala creada"
        )
        assert 'participants' in response.data, (
            "La respuesta debe incluir el campo 'participants' según ChatRoom"
        )

    @pytest.mark.django_db
    def test_start_chat_room_devuelve_sala_existente_si_ya_existe(
        self,
        api_client,
        usuario_y_transportistas
    ):
        """
        Test que valida la idempotencia: si ya existe una sala entre los mismos participantes,
        debe devolver la sala existente en lugar de crear una nueva.
        
        REGLA DE NEGOCIO:
        - No debe crear salas duplicadas entre los mismos participantes
        - Debe devolver 200 OK (no 201) si la sala ya existe
        """
        usuario_a = usuario_y_transportistas['usuario_a']
        transportista_1 = usuario_y_transportistas['transportista_1']

        # Crear manualmente una ChatRoom entre (A y T1)
        sala_existente = ChatRoom.objects.create()
        sala_existente.participants.add(usuario_a, transportista_1.user)

        # Verificar que hay 1 sala
        initial_count = ChatRoom.objects.count()
        assert initial_count == 1, (
            "Debe haber 1 sala de chat antes de la petición"
        )

        # Autenticar como Usuario A
        refresh = RefreshToken.for_user(usuario_a)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        # Hacemos la petición POST al endpoint con los mismos participantes
        payload = {
            'participant_ids': [usuario_a.id, transportista_1.user.id]
        }
        response = api_client.post('/api/chat/rooms/', payload, format='json')

        # VALIDACIÓN DEL CONTRATO:
        # Debe devolver 200 OK (no 201), porque la sala ya existe
        assert response.status_code == status.HTTP_200_OK, (
            f"El endpoint debe devolver 200 OK cuando la sala ya existe, "
            f"pero devolvió {response.status_code}"
        )

        # VALIDACIÓN DE LA LÓGICA DE NEGOCIO (Idempotencia):
        # NO debe haberse creado una nueva sala
        final_count = ChatRoom.objects.count()
        assert final_count == initial_count, (
            f"NO debe haberse creado una nueva sala. "
            f"Inicial: {initial_count}, Final: {final_count}"
        )

        # Verificar que la respuesta contiene la sala existente
        assert 'id' in response.data, (
            "La respuesta debe incluir el campo 'id'"
        )
        assert response.data['id'] == sala_existente.id, (
            f"La respuesta debe contener la sala existente (ID: {sala_existente.id}), "
            f"pero contiene ID: {response.data.get('id')}"
        )


