"""
Tests del Caso de Uso de Registro de Transportista
Valida la lógica de negocio: trial_end debe ser 3 meses en el futuro

Esta prueba debe FALLAR (ROJO) hasta que el Agente de Backend implemente el caso de uso.
"""

import pytest
from datetime import datetime, timedelta
from unittest.mock import Mock, MagicMock
from calendar import monthrange


def add_months(date, months):
    """
    Suma meses a una fecha de forma segura.
    Maneja correctamente los meses con diferentes números de días.
    """
    month = date.month - 1 + months
    year = date.year + month // 12
    month = month % 12 + 1
    day = min(date.day, monthrange(year, month)[1])
    return date.replace(year=year, month=month, day=day)

# Importaremos el caso de uso cuando el Agente de Backend lo cree
# from sigot.application.use_cases.registro import RegistrarTransportista


@pytest.mark.unit
class TestRegistroUseCase:
    """
    Suite de pruebas para el caso de uso de registro de transportista.
    Valida la regla de negocio: trial_end = 3 meses desde el registro.
    """

    def test_transportista_obtiene_trial_al_registrarse(self):
        """
        Test que verifica que al registrar un transportista, se le asigna
        un período de prueba (trial_end) de exactamente 3 meses en el futuro.
        
        REGLA DE NEGOCIO:
        - Cuando un usuario se registra como transportista (is_transportista=True),
          se debe crear un perfil Transportista con trial_end = fecha_actual + 3 meses.
        
        Esta prueba FALLARÁ (ROJO) porque:
        1. El caso de uso RegistrarTransportista aún no existe
        2. El repositorio aún no está implementado
        """
        # Datos de entrada para el registro
        registro_data = {
            "username": "transportista_test",
            "email": "transportista@example.com",
            "password": "password123",
            "is_transportista": True
        }

        # Mock del repositorio (simularemos el TransportistaRepositoryPort)
        # Cuando el Agente de Backend implemente el repositorio, usaremos el real
        mock_repository = Mock()
        
        # Configuramos el mock para simular el guardado
        # El método save() debería retornar los datos del transportista guardado
        def mock_save(transportista_data):
            # Simulamos que el repositorio guarda y retorna los datos con ID
            return {
                "id": 1,
                "user_id": 1,
                "disponible": False,
                "ubicacion": None,
                "trial_end": transportista_data.trial_end,
                "categoria_ids": []
            }
        
        mock_repository.save = Mock(side_effect=mock_save)

        # Fecha de referencia para calcular los 3 meses
        fecha_registro = datetime.now()
        fecha_esperada_trial_end = add_months(fecha_registro, 3)

        # Intentamos importar y usar el caso de uso
        # Esto FALLARÁ (ROJO) hasta que el Agente de Backend lo implemente
        try:
            from sigot.application.use_cases.registro import RegistrarTransportista
            use_case = RegistrarTransportista(repository=mock_repository)
            resultado = use_case.execute(registro_data)
        except (ImportError, ModuleNotFoundError, AttributeError) as e:
            pytest.fail(
                f"El caso de uso RegistrarTransportista aún no está implementado. "
                f"Error: {e}. "
                f"El Agente de Backend debe crear sigot/application/use_cases/registro.py"
            )

        # VALIDACIÓN DE LA REGLA DE NEGOCIO:
        # El trial_end debe estar aproximadamente 3 meses en el futuro
        assert resultado['trial_end'] is not None, (
            "El transportista debe tener un trial_end asignado al registrarse"
        )

        # Verificamos que la diferencia es aproximadamente 3 meses (con tolerancia de 1 día)
        diferencia = resultado['trial_end'] - fecha_registro
        fecha_esperada = add_months(fecha_registro, 3)
        diferencia_esperada = fecha_esperada - fecha_registro
        dias_tolerancia = 1  # Tolerancia de 1 día para evitar problemas de precisión

        assert abs((diferencia.days - diferencia_esperada.days)) <= dias_tolerancia, (
            f"El trial_end debe ser aproximadamente 3 meses desde el registro. "
            f"Esperado: ~{diferencia_esperada.days} días, "
            f"Obtenido: {diferencia.days} días"
        )

        # Verificamos que el trial_end es una fecha futura
        assert resultado['trial_end'] > fecha_registro, (
            "El trial_end debe ser una fecha futura"
        )

    def test_usuario_no_transportista_no_obtiene_trial(self):
        """
        Test que verifica que un usuario que NO es transportista
        no debe tener un perfil Transportista ni trial_end.
        
        REGLA DE NEGOCIO:
        - Solo los usuarios con is_transportista=True deben tener perfil Transportista.
        """
        registro_data = {
            "username": "usuario_normal",
            "email": "usuario@example.com",
            "password": "password123",
            "is_transportista": False  # NO es transportista
        }

        mock_repository = Mock()

        # Intentamos importar y usar el caso de uso
        # Esto FALLARÁ (ROJO) hasta que el Agente de Backend lo implemente
        try:
            from sigot.application.use_cases.registro import RegistrarTransportista
            use_case = RegistrarTransportista(repository=mock_repository)
            resultado = use_case.execute(registro_data)
            
            # El repositorio NO debe ser llamado para usuarios no transportistas
            mock_repository.save.assert_not_called()
        except (ImportError, ModuleNotFoundError, AttributeError) as e:
            pytest.fail(
                f"El caso de uso RegistrarTransportista aún no está implementado. "
                f"Error: {e}. "
                f"El Agente de Backend debe crear sigot/application/use_cases/registro.py"
            )

