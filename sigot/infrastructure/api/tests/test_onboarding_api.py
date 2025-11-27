"""
Tests de API para Onboarding Transaccional (E2E)
Valida el contrato definido en BACKEND_COORDINATION.md para el endpoint transaccional

Estas pruebas deben FALLAR (ROJO) hasta que el Agente 3 (Backend) implemente el endpoint.
"""

import pytest
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

from sigot.infrastructure.db.models import Transportista, Categoria

User = get_user_model()


@pytest.mark.api
class TestOnboardingAPI:
    """
    Suite de pruebas para el endpoint transaccional de onboarding.
    Valida que el endpoint procesa todos los datos del wizard en una única transacción.
    """

    @pytest.fixture
    def api_client(self):
        """Cliente API para hacer peticiones HTTP."""
        return APIClient()

    @pytest.fixture
    def transportista_incompleto(self, db):
        """
        Crea un usuario transportista con perfil incompleto (sin onboarding).
        Este es el estado inicial antes de completar el wizard.
        """
        user = User.objects.create_user(
            username='transportista_incompleto',
            email='trans_incompleto@example.com',
            password='password123',
            phone=None  # Perfil incompleto: sin teléfono
        )
        # Crear Transportista sin datos de onboarding
        # Esto hace que el usuario sea "transportista" (hasattr(user, 'transportista') == True)
        transportista = Transportista.objects.create(
            user=user,
            disponible=False,
            direccion_empresarial=None,  # Sin dirección
            tipo_zona_actuacion='RADIO',
            radio_km=None,  # Sin radio configurado
            zonas_definidas=None,
            trial_end=None  # Se asigna en el registro, pero lo dejamos None para el test
        )
        # Sin categorías asignadas
        return {
            'user': user,
            'transportista': transportista
        }

    @pytest.fixture
    def authenticated_transportista_client(self, api_client, transportista_incompleto):
        """
        Helper para crear un cliente API autenticado como transportista con perfil incompleto.
        """
        user = transportista_incompleto['user']
        refresh = RefreshToken.for_user(user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        return api_client

    @pytest.fixture
    def categorias_validas(self, db):
        """
        Crea categorías válidas para usar en los tests.
        Usa categorías existentes de la migración v2.0 si están disponibles,
        o crea nuevas para el test.
        """
        try:
            # Intentar usar categorías existentes de la migración
            cat1 = Categoria.objects.get(nombre='Transporte de Mercancías')
            cat2 = Categoria.objects.get(nombre='Carga General (Seca)')
            return [cat1, cat2]
        except Categoria.DoesNotExist:
            # Si no existen, crear categorías de prueba
            cat1 = Categoria.objects.create(
                nombre='Test Categoría 1',
                descripcion='Categoría de prueba 1'
            )
            cat2 = Categoria.objects.create(
                nombre='Test Categoría 2',
                descripcion='Categoría de prueba 2'
            )
            return [cat1, cat2]

    @pytest.mark.django_db
    def test_onboarding_complete_es_transaccional(
        self,
        authenticated_transportista_client,
        transportista_incompleto,
        categorias_validas
    ):
        """
        Test CRÍTICO: Valida que el endpoint procesa todos los datos del wizard
        en una única transacción y guarda TODOS los datos correctamente.
        
        Escenario:
        - Transportista con perfil incompleto (sin teléfono, dirección, radio, categorías)
        - Envía payload completo del wizard
        - Verifica que TODOS los datos se guardan correctamente
        
        Esta prueba FALLARÁ (ROJO) hasta que el Agente 3 implemente el endpoint.
        """
        user = transportista_incompleto['user']
        transportista = transportista_incompleto['transportista']
        
        # Preparar payload completo según WizardDataPayload del frontend
        payload = {
            'phone': '+34612345678',
            'direccion_empresarial': 'Calle Principal 123, Madrid, 28001',
            'tipo_zona_actuacion': 'RADIO',
            'radio_km': 100,
            'zonas_definidas': None,
            'categoria_ids': [cat.id for cat in categorias_validas]
        }
        
        # Hacer la petición POST al endpoint (que aún no existe - fallará con 404)
        response = authenticated_transportista_client.post(
            '/api/onboarding/complete/',
            payload,
            format='json'
        )
        
        # VALIDACIÓN DEL CONTRATO:
        # Según BACKEND_COORDINATION.md, debe devolver 200 OK
        assert response.status_code == status.HTTP_200_OK, (
            f"El endpoint /onboarding/complete/ debe devolver 200 OK, "
            f"pero devolvió {response.status_code}. "
            f"Respuesta: {response.data if hasattr(response, 'data') else response.content}"
        )
        
        # VALIDACIÓN DE LA ESTRUCTURA DE RESPUESTA:
        # Según BACKEND_COORDINATION.md, debe incluir message, transportista y user
        assert 'message' in response.data, (
            "La respuesta debe incluir el campo 'message' según WizardSubmissionResponse"
        )
        assert 'transportista' in response.data, (
            "La respuesta debe incluir el campo 'transportista' según WizardSubmissionResponse"
        )
        assert 'user' in response.data, (
            "La respuesta debe incluir el campo 'user' según WizardSubmissionResponse"
        )
        
        # VALIDACIÓN DE TRANSACCIONALIDAD:
        # Verificar que TODOS los datos se han guardado correctamente en la BBDD
        
        # 1. Verificar que User.phone se actualizó
        user.refresh_from_db()
        assert user.phone == '+34612345678', (
            f"El teléfono del usuario debe haberse actualizado a '+34612345678', "
            f"pero es '{user.phone}'"
        )
        
        # 2. Verificar que Transportista.direccion_empresarial se guardó
        transportista.refresh_from_db()
        assert transportista.direccion_empresarial == 'Calle Principal 123, Madrid, 28001', (
            f"La dirección empresarial debe haberse guardado, "
            f"pero es '{transportista.direccion_empresarial}'"
        )
        
        # 3. Verificar que Transportista.tipo_zona_actuacion se guardó
        assert transportista.tipo_zona_actuacion == 'RADIO', (
            f"El tipo de zona de actuación debe ser 'RADIO', "
            f"pero es '{transportista.tipo_zona_actuacion}'"
        )
        
        # 4. Verificar que Transportista.radio_km se guardó (CRÍTICO)
        assert transportista.radio_km == 100, (
            f"El radio_km debe haberse guardado como 100, "
            f"pero es '{transportista.radio_km}'"
        )
        
        # 5. Verificar que Transportista.zonas_definidas es None (para tipo RADIO)
        assert transportista.zonas_definidas is None, (
            f"Las zonas_definidas deben ser None para tipo RADIO, "
            f"pero es '{transportista.zonas_definidas}'"
        )
        
        # 6. Verificar que las categorías se asignaron correctamente (ManyToMany)
        categorias_asignadas = list(transportista.categorias.all())
        categoria_ids_asignadas = [cat.id for cat in categorias_asignadas]
        categoria_ids_esperadas = [cat.id for cat in categorias_validas]
        
        assert set(categoria_ids_asignadas) == set(categoria_ids_esperadas), (
            f"Las categorías deben haberse asignado correctamente. "
            f"Esperadas: {categoria_ids_esperadas}, "
            f"Obtenidas: {categoria_ids_asignadas}"
        )
        
        # 7. Verificar que el perfil está completo
        # Un perfil completo tiene: direccion_empresarial, tipo_zona_actuacion configurado,
        # radio_km o zonas_definidas según el tipo, y al menos una categoría
        assert transportista.direccion_empresarial is not None, (
            "El perfil debe estar completo (tiene direccion_empresarial)"
        )
        assert transportista.radio_km is not None, (
            "El perfil debe estar completo (tiene radio_km configurado)"
        )
        assert transportista.categorias.count() > 0, (
            "El perfil debe estar completo (tiene categorías asignadas)"
        )
        
        # VALIDACIÓN DE LA RESPUESTA:
        # Verificar que la respuesta incluye los datos actualizados
        transportista_data = response.data['transportista']
        assert transportista_data['direccion_empresarial'] == 'Calle Principal 123, Madrid, 28001'
        assert transportista_data['radio_km'] == 100
        assert len(transportista_data['categorias']) == len(categorias_validas)
        
        user_data = response.data['user']
        assert user_data['phone'] == '+34612345678'

    @pytest.mark.django_db
    def test_onboarding_complete_falla_atomicamente(
        self,
        authenticated_transportista_client,
        transportista_incompleto
    ):
        """
        Test CRÍTICO: Valida que el endpoint es ATÓMICO.
        
        Si falla la validación (ej. categoría inválida), NINGÚN dato debe guardarse.
        Esto verifica que el @transaction.atomic funciona correctamente.
        
        Escenario:
        - Transportista con perfil incompleto
        - Envía payload con ID de categoría inválido (que no existe)
        - Verifica que NINGÚN dato se guardó (rollback completo)
        
        Esta prueba FALLARÁ (ROJO) hasta que el Agente 3 implemente el endpoint
        con transaccionalidad.
        """
        user = transportista_incompleto['user']
        transportista = transportista_incompleto['transportista']
        
        # Guardar estado inicial para verificar que no cambió
        phone_inicial = user.phone
        direccion_inicial = transportista.direccion_empresarial
        radio_km_inicial = transportista.radio_km
        categorias_iniciales_count = transportista.categorias.count()
        
        # Preparar payload con categoría inválida (ID que no existe)
        payload = {
            'phone': '+34612345678',
            'direccion_empresarial': 'Calle Principal 123, Madrid, 28001',
            'tipo_zona_actuacion': 'RADIO',
            'radio_km': 100,
            'zonas_definidas': None,
            'categoria_ids': [99999]  # ID de categoría que no existe
        }
        
        # Hacer la petición POST al endpoint
        response = authenticated_transportista_client.post(
            '/api/onboarding/complete/',
            payload,
            format='json'
        )
        
        # VALIDACIÓN DEL CONTRATO:
        # Debe devolver 400 Bad Request por categoría inválida
        assert response.status_code == status.HTTP_400_BAD_REQUEST, (
            f"El endpoint debe devolver 400 Bad Request para categoría inválida, "
            f"pero devolvió {response.status_code}. "
            f"Respuesta: {response.data if hasattr(response, 'data') else response.content}"
        )
        
        # VALIDACIÓN DE ATOMICIDAD (CRÍTICO):
        # Verificar que NINGÚN dato se guardó en la BBDD (rollback completo)
        
        # 1. Verificar que User.phone NO se actualizó
        user.refresh_from_db()
        assert user.phone == phone_inicial, (
            f"El teléfono NO debe haberse actualizado debido al rollback. "
            f"Era '{phone_inicial}', ahora es '{user.phone}'"
        )
        
        # 2. Verificar que Transportista.direccion_empresarial NO se guardó
        transportista.refresh_from_db()
        assert transportista.direccion_empresarial == direccion_inicial, (
            f"La dirección empresarial NO debe haberse guardado debido al rollback. "
            f"Era '{direccion_inicial}', ahora es '{transportista.direccion_empresarial}'"
        )
        
        # 3. Verificar que Transportista.radio_km NO se guardó (CRÍTICO)
        assert transportista.radio_km == radio_km_inicial, (
            f"El radio_km NO debe haberse guardado debido al rollback. "
            f"Era '{radio_km_inicial}', ahora es '{transportista.radio_km}'"
        )
        
        # 4. Verificar que NO se asignaron categorías
        assert transportista.categorias.count() == categorias_iniciales_count, (
            f"NO se deben haber asignado categorías debido al rollback. "
            f"Eran {categorias_iniciales_count}, ahora son {transportista.categorias.count()}"
        )
        
        # VALIDACIÓN DE MENSAJE DE ERROR:
        # El error debe indicar que la categoría es inválida
        assert 'error' in response.data or 'details' in response.data, (
            "La respuesta de error debe incluir información sobre el error"
        )

    @pytest.mark.django_db
    def test_onboarding_complete_requiere_autenticacion(
        self,
        api_client
    ):
        """
        Test que valida que el endpoint requiere autenticación.
        
        Según BACKEND_COORDINATION.md:
        - El endpoint requiere autenticación (JWT Bearer Token)
        - Debe devolver 401 Unauthorized cuando no hay token
        """
        payload = {
            'phone': '+34612345678',
            'direccion_empresarial': 'Calle Principal 123, Madrid, 28001',
            'tipo_zona_actuacion': 'RADIO',
            'radio_km': 100,
            'zonas_definidas': None,
            'categoria_ids': [1]
        }
        
        # Hacer la petición POST sin autenticación
        response = api_client.post(
            '/api/onboarding/complete/',
            payload,
            format='json'
        )
        
        # VALIDACIÓN DEL CONTRATO:
        # Debe devolver 401 Unauthorized
        assert response.status_code == status.HTTP_401_UNAUTHORIZED, (
            f"El endpoint debe devolver 401 Unauthorized sin autenticación, "
            f"pero devolvió {response.status_code}"
        )

    @pytest.mark.django_db
    def test_onboarding_complete_solo_para_transportistas(
        self,
        api_client,
        db
    ):
        """
        Test que valida que solo los transportistas pueden completar el onboarding.
        
        Según BACKEND_COORDINATION.md:
        - Debe devolver 403 Forbidden si el usuario no es transportista
        """
        # Crear usuario normal (no transportista)
        # No crear Transportista = no es transportista
        user = User.objects.create_user(
            username='usuario_normal',
            email='normal@example.com',
            password='password123'
        )
        # No crear Transportista, por lo tanto no es transportista
        refresh = RefreshToken.for_user(user)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        payload = {
            'phone': '+34612345678',
            'direccion_empresarial': 'Calle Principal 123, Madrid, 28001',
            'tipo_zona_actuacion': 'RADIO',
            'radio_km': 100,
            'zonas_definidas': None,
            'categoria_ids': [1]
        }
        
        # Hacer la petición POST como usuario normal
        response = api_client.post(
            '/api/onboarding/complete/',
            payload,
            format='json'
        )
        
        # VALIDACIÓN DEL CONTRATO:
        # Debe devolver 403 Forbidden
        assert response.status_code == status.HTTP_403_FORBIDDEN, (
            f"El endpoint debe devolver 403 Forbidden para usuarios no transportistas, "
            f"pero devolvió {response.status_code}"
        )

