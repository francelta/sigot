"""
Configuración de la aplicación de Base de Datos
"""

from django.apps import AppConfig


class DbConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sigot.infrastructure.db'
    verbose_name = 'Base de Datos'


