"""
Tests de API para Búsqueda por Zona de Actuación (E2E)
Valida el contrato definido en openapi.yml para búsqueda por zona

Estas pruebas deben FALLAR (ROJO) hasta que el Agente de Backend implemente los endpoints.
"""

import pytest
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.gis.geos import Point
from django.contrib.auth import get_user_model

from sigot.infrastructure.db.models import Transportista, Categoria

User = get_user_model()


@pytest.mark.api
class TestBusquedaPorZonaAPI:
    """
    Suite de pruebas para el endpoint de búsqueda por zona de actuación.
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

    @pytest.mark.django_db
    def test_transportista_con_radio_km_aparece_en_busqueda(
        self,
        authenticated_client
    ):
        """
        Test que valida que un transportista con radio_km aparece en búsquedas
        dentro de su radio de actuación.
        
        Escenario:
        - Transportista en Zaragoza con radio_km=100
        - Búsqueda en Huesca (a ~70km de Zaragoza)
        - Debe aparecer en los resultados
        """
        # Crear transportista en Zaragoza (aprox. 41.6488, -0.8891)
        user_t1 = User.objects.create_user(
            username='transportista_zaragoza',
            email='zaragoza@example.com',
            password='password123'
        )
        transportista = Transportista.objects.create(
            user=user_t1,
            disponible=True,
            direccion_empresarial='Zaragoza, España',
            base_geocodificada=Point(-0.8891, 41.6488, srid=4326),  # Zaragoza
            tipo_zona_actuacion='RADIO',
            radio_km=100,
            trial_end=None
        )

        # Hacemos la petición GET buscando en Huesca (a ~70km de Zaragoza)
        # Huesca está aproximadamente en -0.4087, 42.1361
        response = authenticated_client.get(
            '/api/transportistas/cercanos/',
            {'q': 'Huesca'}
        )

        # VALIDACIÓN DEL CONTRATO:
        # Según openapi.yml, debe devolver 200 OK
        assert response.status_code == status.HTTP_200_OK, (
            f"El endpoint /transportistas/cercanos/ debe devolver 200 OK, "
            f"pero devolvió {response.status_code}. "
            f"Respuesta: {response.data if hasattr(response, 'data') else response.content}"
        )

        # VALIDACIÓN DE LA LÓGICA DE NEGOCIO:
        # Debe devolver el transportista de Zaragoza (está dentro del radio de 100km)
        if 'results' in response.data:
            results = response.data['results']
        else:
            results = response.data if isinstance(response.data, list) else []

        transportista_ids = [t.get('id') or t.get('user_id') for t in results]
        assert user_t1.id in transportista_ids or transportista.user_id in transportista_ids, (
            f"El transportista de Zaragoza (ID: {user_t1.id}) debe aparecer en la búsqueda de Huesca, "
            f"ya que está dentro del radio de 100km. IDs encontrados: {transportista_ids}"
        )

    @pytest.mark.django_db
    def test_transportista_fuera_de_radio_no_aparece(
        self,
        authenticated_client
    ):
        """
        Test que valida que un transportista NO aparece si la búsqueda está fuera de su radio.
        
        Escenario:
        - Transportista en Zaragoza con radio_km=100
        - Búsqueda en Marsella (a ~600km de Zaragoza)
        - NO debe aparecer en los resultados
        """
        # Crear transportista en Zaragoza
        user_t1 = User.objects.create_user(
            username='transportista_zaragoza',
            email='zaragoza@example.com',
            password='password123'
        )
        transportista = Transportista.objects.create(
            user=user_t1,
            disponible=True,
            direccion_empresarial='Zaragoza, España',
            base_geocodificada=Point(-0.8891, 41.6488, srid=4326),  # Zaragoza
            tipo_zona_actuacion='RADIO',
            radio_km=100,
            trial_end=None
        )

        # Hacemos la petición GET buscando en Marsella (a ~600km de Zaragoza)
        response = authenticated_client.get(
            '/api/transportistas/cercanos/',
            {'q': 'Marsella'}
        )

        # VALIDACIÓN DEL CONTRATO:
        assert response.status_code == status.HTTP_200_OK, (
            f"El endpoint debe devolver 200 OK, pero devolvió {response.status_code}"
        )

        # VALIDACIÓN DE LA LÓGICA DE NEGOCIO:
        # NO debe devolver el transportista de Zaragoza (está fuera del radio de 100km)
        if 'results' in response.data:
            results = response.data['results']
        else:
            results = response.data if isinstance(response.data, list) else []

        transportista_ids = [t.get('id') or t.get('user_id') for t in results]
        assert user_t1.id not in transportista_ids and transportista.user_id not in transportista_ids, (
            f"El transportista de Zaragoza (ID: {user_t1.id}) NO debe aparecer en la búsqueda de Marsella, "
            f"ya que está fuera del radio de 100km. IDs encontrados: {transportista_ids}"
        )

    @pytest.mark.django_db
    def test_transportista_con_zona_provincia_aparece(
        self,
        authenticated_client
    ):
        """
        Test que valida que un transportista con zonas definidas aparece
        cuando la búsqueda coincide con una de sus provincias.
        
        Escenario:
        - Transportista con zonas_definidas={"provincias": ["Madrid"]}
        - Búsqueda en "Madrid"
        - Debe aparecer en los resultados
        """
        # Crear transportista con zona de actuación por provincias
        user_t1 = User.objects.create_user(
            username='transportista_madrid',
            email='madrid@example.com',
            password='password123'
        )
        transportista = Transportista.objects.create(
            user=user_t1,
            disponible=True,
            direccion_empresarial='Madrid, España',
            base_geocodificada=Point(-3.7038, 40.4168, srid=4326),  # Madrid
            tipo_zona_actuacion='ZONAS',
            zonas_definidas={'provincias': ['Madrid']},
            trial_end=None
        )

        # Hacemos la petición GET buscando en Madrid
        response = authenticated_client.get(
            '/api/transportistas/cercanos/',
            {'q': 'Madrid'}
        )

        # VALIDACIÓN DEL CONTRATO:
        assert response.status_code == status.HTTP_200_OK, (
            f"El endpoint debe devolver 200 OK, pero devolvió {response.status_code}"
        )

        # VALIDACIÓN DE LA LÓGICA DE NEGOCIO:
        # Debe devolver el transportista con zona Madrid
        if 'results' in response.data:
            results = response.data['results']
        else:
            results = response.data if isinstance(response.data, list) else []

        transportista_ids = [t.get('id') or t.get('user_id') for t in results]
        assert user_t1.id in transportista_ids or transportista.user_id in transportista_ids, (
            f"El transportista con zona Madrid (ID: {user_t1.id}) debe aparecer en la búsqueda de Madrid. "
            f"IDs encontrados: {transportista_ids}"
        )

    @pytest.mark.django_db
    def test_get_transportistas_cercanos_falla_sin_autenticacion(
        self,
        api_client
    ):
        """
        Test que valida que el endpoint requiere autenticación.
        
        Según openapi.yml:
        - El endpoint requiere autenticación (security: bearerAuth)
        - Debe devolver 401 Unauthorized cuando no hay token
        """
        # Hacemos la petición GET sin autenticación
        response = api_client.get(
            '/api/transportistas/cercanos/',
            {'q': 'Madrid'}
        )

        # VALIDACIÓN DEL CONTRATO:
        # Según openapi.yml, debe devolver 401 Unauthorized
        assert response.status_code == status.HTTP_401_UNAUTHORIZED, (
            f"El endpoint debe devolver 401 Unauthorized sin autenticación, "
            f"pero devolvió {response.status_code}"
        )


