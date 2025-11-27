"""
Tests de API para Autenticación (E2E)
Valida el contrato definido en openapi.yml

Estas pruebas deben FALLAR (ROJO) hasta que el Agente de Backend implemente los endpoints.
"""

import pytest
from rest_framework.test import APIClient
from rest_framework import status


@pytest.mark.api
class TestAuthAPI:
    """
    Suite de pruebas para los endpoints de autenticación.
    Valida el contrato OpenAPI definido por el Arquitecto.
    """

    @pytest.fixture
    def api_client(self):
        """Cliente API para hacer peticiones HTTP."""
        return APIClient()

    @pytest.mark.django_db
    def test_register_endpoint_exists(self, api_client):
        """
        Test que valida que el endpoint POST /auth/register/ existe y responde.
        
        Según openapi.yml:
        - Endpoint: POST /auth/register/
        - Respuesta esperada: 201 Created con AuthResponse
        - Esta prueba FALLARÁ (ROJO) porque el endpoint aún no existe (404)
        """
        # Datos de registro según el esquema RegisterRequest de openapi.yml
        register_data = {
            "username": "test_user",
            "email": "test@example.com",
            "password": "password123",
            "is_transportista": True
        }

        # Hacemos la petición POST al endpoint
        response = api_client.post('/api/auth/register/', register_data, format='json')

        # VALIDACIÓN DEL CONTRATO:
        # Según openapi.yml, debe devolver 201 Created
        assert response.status_code == status.HTTP_201_CREATED, (
            f"El endpoint /auth/register/ debe devolver 201 Created, "
            f"pero devolvió {response.status_code}. "
            f"Respuesta: {response.data if hasattr(response, 'data') else response.content}"
        )

        # VALIDACIÓN DE LA ESTRUCTURA DE RESPUESTA:
        # Según openapi.yml, la respuesta debe tener el esquema AuthResponse
        assert 'access' in response.data, (
            "La respuesta debe incluir el campo 'access' (token JWT) según AuthResponse"
        )
        assert 'user' in response.data, (
            "La respuesta debe incluir el campo 'user' según AuthResponse"
        )

        # Validar estructura del objeto user
        user_data = response.data['user']
        assert 'id' in user_data, "El objeto user debe tener un campo 'id'"
        assert 'username' in user_data, "El objeto user debe tener un campo 'username'"
        assert 'email' in user_data, "El objeto user debe tener un campo 'email'"
        assert 'is_transportista' in user_data, (
            "El objeto user debe tener un campo 'is_transportista'"
        )

    @pytest.mark.django_db
    def test_register_with_invalid_data_returns_400(self, api_client):
        """
        Test que valida que el endpoint rechaza datos inválidos.
        
        Según openapi.yml:
        - Debe devolver 400 Bad Request cuando los datos no son válidos
        """
        # Datos inválidos: falta el campo requerido 'password'
        invalid_data = {
            "username": "test_user",
            "email": "test@example.com",
            "is_transportista": True
            # Falta 'password' que es requerido según RegisterRequest
        }

        response = api_client.post('/api/auth/register/', invalid_data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST, (
            f"El endpoint debe devolver 400 Bad Request para datos inválidos, "
            f"pero devolvió {response.status_code}"
        )

    @pytest.mark.django_db
    def test_register_with_duplicate_email_returns_409(self, api_client):
        """
        Test que valida que el endpoint rechaza emails duplicados.
        
        Según openapi.yml:
        - Debe devolver 409 Conflict cuando el email ya existe
        """
        # Primero creamos un usuario
        register_data = {
            "username": "first_user",
            "email": "duplicate@example.com",
            "password": "password123",
            "is_transportista": False
        }
        api_client.post('/api/auth/register/', register_data, format='json')

        # Intentamos crear otro usuario con el mismo email
        duplicate_data = {
            "username": "second_user",
            "email": "duplicate@example.com",  # Email duplicado
            "password": "password123",
            "is_transportista": False
        }

        response = api_client.post('/api/auth/register/', duplicate_data, format='json')

        assert response.status_code == status.HTTP_409_CONFLICT, (
            f"El endpoint debe devolver 409 Conflict para emails duplicados, "
            f"pero devolvió {response.status_code}"
        )

