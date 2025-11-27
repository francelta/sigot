"""
Tests de API para Categorías (E2E)
Valida el contrato definido en openapi.yml para la estructura jerárquica N-niveles

Estas pruebas validan que el endpoint devuelve la estructura jerárquica anidada (no plana).
"""

import pytest
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

from sigot.infrastructure.db.models import Categoria

User = get_user_model()


@pytest.mark.api
class TestCategoriasAPI:
    """
    Suite de pruebas para el endpoint de categorías.
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
    def categoria_hierarchy_3_levels(self, db):
        """
        Usa la jerarquía existente de la migración v2.0 para probar recursión.
        
        Estructura (de la migración v2.0):
        - Transporte de Mercancías (raíz)
          - Carga General (Seca) (nivel 2)
            - Camión Articulado (Tráiler) (nivel 3)
              - Tráiler Lona (Tauliner) (nivel 4)
        """
        # Obtener las categorías existentes de la migración v2.0
        root = Categoria.objects.get(nombre='Transporte de Mercancías')
        level2 = Categoria.objects.get(nombre='Carga General (Seca)')
        level3 = Categoria.objects.get(nombre='Camión Articulado (Tráiler)')
        level4 = Categoria.objects.get(nombre='Tráiler Lona (Tauliner)')
        
        return {
            'root': root,
            'level2': level2,
            'level3': level3,
            'level4': level4,
        }

    @pytest.mark.django_db
    def test_categorias_endpoint_exists(self, authenticated_client):
        """
        Test que valida que el endpoint GET /api/categorias/ existe y responde.
        
        Según openapi.yml:
        - Endpoint: GET /api/categorias/
        - Respuesta esperada: 200 OK con array de Categoria
        """
        response = authenticated_client.get('/api/categorias/')
        
        assert response.status_code == status.HTTP_200_OK, (
            f"El endpoint /categorias/ debe devolver 200 OK, "
            f"pero devolvió {response.status_code}"
        )
        
        assert isinstance(response.data, list), (
            "La respuesta debe ser un array según openapi.yml"
        )

    @pytest.mark.django_db
    def test_categorias_endpoint_is_public(self, api_client):
        """
        Test que valida que el endpoint GET /api/categorias/ es público
        (no requiere autenticación).
        
        Las categorías son datos de referencia que cualquier usuario
        debería poder ver, incluso antes de registrarse.
        """
        response = api_client.get('/api/categorias/')
        
        assert response.status_code == status.HTTP_200_OK, (
            f"El endpoint /categorias/ debe ser público y devolver 200 OK sin autenticación, "
            f"pero devolvió {response.status_code}"
        )
        
        assert isinstance(response.data, list), (
            "La respuesta debe ser un array incluso sin autenticación"
        )

    @pytest.mark.django_db
    def test_categorias_returns_hierarchical_structure(self, authenticated_client, categoria_hierarchy_3_levels):
        """
        Test CRÍTICO: Valida que el endpoint devuelve estructura jerárquica ANIDADA (no plana).
        
        Según openapi.yml:
        - Debe retornar solo nodos raíz (parent=None)
        - Cada nodo raíz debe incluir sus 'children' anidados
        - Los children deben tener su propia estructura 'children' (recursión)
        - Soporta N-niveles de profundidad
        """
        response = authenticated_client.get('/api/categorias/')
        
        assert response.status_code == status.HTTP_200_OK
        
        data = response.data
        
        # VALIDACIÓN 1: Debe retornar solo nodos raíz
        assert len(data) > 0, "Debe retornar al menos una categoría raíz"
        
        # Buscar la categoría raíz "Transporte de Mercancías"
        transporte_merc = None
        for cat in data:
            if cat['nombre'] == 'Transporte de Mercancías':
                transporte_merc = cat
                break
        
        assert transporte_merc is not None, "Debe incluir la categoría raíz 'Transporte de Mercancías'"
        
        # VALIDACIÓN 2: La categoría raíz NO debe tener parent
        assert transporte_merc['parent'] is None, (
            "Las categorías raíz deben tener parent=None"
        )
        
        # VALIDACIÓN 3: Debe tener children (estructura anidada)
        assert 'children' in transporte_merc, (
            "La categoría raíz debe incluir el campo 'children' según openapi.yml"
        )
        assert isinstance(transporte_merc['children'], list), (
            "El campo 'children' debe ser un array"
        )
        assert len(transporte_merc['children']) > 0, (
            "La categoría 'Transporte de Mercancías' debe tener al menos un child"
        )
        
        # VALIDACIÓN 4: Los children deben tener su propia estructura completa
        # Buscar 'Carga General (Seca)' en los children
        carga_general = None
        for child in transporte_merc['children']:
            if child['nombre'] == 'Carga General (Seca)':
                carga_general = child
                break
        
        assert carga_general is not None, (
            "Debe incluir la subcategoría 'Carga General (Seca)'"
        )
        assert carga_general['parent'] == transporte_merc['id'], (
            "El parent de 'Carga General (Seca)' debe ser el ID de 'Transporte de Mercancías'"
        )
        
        # VALIDACIÓN 5: RECURSIÓN N-NIVELES - Los children deben tener sus propios children
        assert 'children' in carga_general, (
            "Las subcategorías también deben incluir el campo 'children' (recursión)"
        )
        assert isinstance(carga_general['children'], list), (
            "El campo 'children' de nivel 2 debe ser un array"
        )
        assert len(carga_general['children']) > 0, (
            "'Carga General (Seca)' debe tener al menos un child (nivel 3)"
        )
        
        # VALIDACIÓN 6: Nivel 3 debe estar anidado correctamente
        # Buscar 'Camión Articulado (Tráiler)' en los children de 'Carga General (Seca)'
        trailer = None
        for child in carga_general['children']:
            if child['nombre'] == 'Camión Articulado (Tráiler)':
                trailer = child
                break
        
        assert trailer is not None, (
            "Debe incluir la subcategoría nivel 3 'Camión Articulado (Tráiler)'"
        )
        assert trailer['parent'] == carga_general['id'], (
            "El parent de 'Camión Articulado (Tráiler)' debe ser el ID de 'Carga General (Seca)'"
        )
        
        # VALIDACIÓN 7: Nivel 4 debe estar anidado correctamente
        assert 'children' in trailer, (
            "Las categorías de nivel 3 también deben incluir el campo 'children'"
        )
        assert isinstance(trailer['children'], list), (
            "El campo 'children' debe ser siempre un array"
        )
        assert len(trailer['children']) > 0, (
            "'Camión Articulado (Tráiler)' debe tener al menos un child (nivel 4)"
        )
        
        # Buscar 'Tráiler Lona (Tauliner)' en los children de 'Camión Articulado (Tráiler)'
        tauliner = None
        for child in trailer['children']:
            if child['nombre'] == 'Tráiler Lona (Tauliner)':
                tauliner = child
                break
        
        assert tauliner is not None, (
            "Debe incluir la subcategoría nivel 4 'Tráiler Lona (Tauliner)'"
        )
        assert tauliner['parent'] == trailer['id'], (
            "El parent de 'Tráiler Lona (Tauliner)' debe ser el ID de 'Camión Articulado (Tráiler)'"
        )
        
        # VALIDACIÓN 8: El nivel 4 también debe tener campo 'children' (aunque esté vacío)
        assert 'children' in tauliner, (
            "Todas las categorías deben tener el campo 'children' (incluso si está vacío)"
        )
        assert isinstance(tauliner['children'], list), (
            "El campo 'children' debe ser siempre un array"
        )

    @pytest.mark.django_db
    def test_categorias_only_returns_root_nodes(self, authenticated_client, categoria_hierarchy_3_levels):
        """
        Valida que el endpoint solo retorna nodos raíz (parent=None).
        
        Las subcategorías deben estar anidadas dentro de sus padres,
        no como elementos separados en el array raíz.
        """
        response = authenticated_client.get('/api/categorias/')
        
        assert response.status_code == status.HTTP_200_OK
        
        data = response.data
        
        # Todas las categorías en el array raíz deben tener parent=None
        for categoria in data:
            assert categoria['parent'] is None, (
                f"La categoría '{categoria['nombre']}' no debería estar en el array raíz "
                f"porque tiene parent={categoria['parent']}"
            )
        
        # Verificar que las subcategorías NO están en el array raíz
        nombres_raiz = [cat['nombre'] for cat in data]
        assert 'Carga General (Seca)' not in nombres_raiz, (
            "'Carga General (Seca)' no debe estar en el array raíz, debe estar anidada"
        )
        assert 'Camión Articulado (Tráiler)' not in nombres_raiz, (
            "'Camión Articulado (Tráiler)' no debe estar en el array raíz, debe estar anidada"
        )
        assert 'Tráiler Lona (Tauliner)' not in nombres_raiz, (
            "'Tráiler Lona (Tauliner)' no debe estar en el array raíz, debe estar anidada"
        )

    @pytest.mark.django_db
    def test_categorias_supports_n_levels(self, authenticated_client, db):
        """
        Test que valida que el serializer soporta jerarquías de N-niveles.
        
        Crea una jerarquía de 4 niveles y verifica que todos están correctamente anidados.
        """
        # Crear jerarquía de 4 niveles con nombres únicos para evitar conflictos
        level1 = Categoria.objects.create(nombre='TestNivel1', descripcion='Raíz')
        level2 = Categoria.objects.create(nombre='TestNivel2', descripcion='Nivel 2', parent=level1)
        level3 = Categoria.objects.create(nombre='TestNivel3', descripcion='Nivel 3', parent=level2)
        level4 = Categoria.objects.create(nombre='TestNivel4', descripcion='Nivel 4', parent=level3)
        
        response = authenticated_client.get('/api/categorias/')
        
        assert response.status_code == status.HTTP_200_OK
        
        # Buscar TestNivel1 en la respuesta
        nivel1_data = None
        for cat in response.data:
            if cat['nombre'] == 'TestNivel1':
                nivel1_data = cat
                break
        
        assert nivel1_data is not None
        
        # Verificar que todos los niveles están anidados
        nivel2_data = nivel1_data['children'][0]
        assert nivel2_data['nombre'] == 'TestNivel2'
        
        nivel3_data = nivel2_data['children'][0]
        assert nivel3_data['nombre'] == 'TestNivel3'
        
        nivel4_data = nivel3_data['children'][0]
        assert nivel4_data['nombre'] == 'TestNivel4'
        
        # Verificar que el nivel 4 también tiene el campo children (aunque vacío)
        assert 'children' in nivel4_data
        assert isinstance(nivel4_data['children'], list)

