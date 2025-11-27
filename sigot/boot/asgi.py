"""
ASGI config for SIGOT project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/stable/howto/deployment/asgi/
"""

import os

# IMPORTANTE: Configurar Django ANTES de importar cualquier cosa que dependa de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sigot.boot.settings')

# Importar get_asgi_application y configurar Django
from django.core.asgi import get_asgi_application

django_asgi_app = get_asgi_application()

# Ahora que Django está configurado, podemos importar módulos que dependen de Django
from channels.routing import ProtocolTypeRouter, URLRouter
from sigot.infrastructure.websockets.routing import websocket_urlpatterns
from sigot.infrastructure.websockets.middleware import JWTAuthMiddlewareStack

application = ProtocolTypeRouter(
    {
        'http': django_asgi_app,
        'websocket': JWTAuthMiddlewareStack(
            URLRouter(websocket_urlpatterns)
        ),
    }
)

