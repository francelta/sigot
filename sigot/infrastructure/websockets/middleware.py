"""
Middleware personalizado para autenticación JWT en WebSockets
"""

from urllib.parse import parse_qs
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.settings import api_settings
from django.conf import settings

User = get_user_model()


@database_sync_to_async
def get_user_from_token(token: str):
    """Obtiene el usuario desde un token JWT."""
    try:
        # Validar el token
        UntypedToken(token)
    except (InvalidToken, TokenError) as e:
        return None
    
    # Decodificar el token para obtener el user_id
    # UntypedToken ya valida el token, ahora solo necesitamos obtener el user_id
    try:
        # Usar el algoritmo de JWT configurado
        from jwt import decode as jwt_decode
        decoded_data = jwt_decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[api_settings.ALGORITHM]
        )
        user_id = decoded_data.get('user_id')
        if user_id:
            return User.objects.get(id=user_id)
    except (User.DoesNotExist, Exception) as e:
        return None
    
    return None


class JWTAuthMiddleware(BaseMiddleware):
    """
    Middleware para autenticar WebSocket connections usando JWT tokens.
    El token puede venir como query parameter: ?token=...
    """

    async def __call__(self, scope, receive, send):
        # Solo procesar conexiones WebSocket
        if scope['type'] != 'websocket':
            return await super().__call__(scope, receive, send)
        
        # Extraer el token de los query parameters
        query_string = scope.get('query_string', b'').decode()
        query_params = parse_qs(query_string)
        token = query_params.get('token', [None])[0]
        
        # Si hay token, intentar autenticar
        if token:
            user = await get_user_from_token(token)
            if user:
                scope['user'] = user
            # Si el token es inválido, scope['user'] será AnonymousUser
            # El consumer se encargará de rechazar la conexión
        # Si no hay token, scope['user'] será AnonymousUser por defecto
        # El consumer se encargará de rechazar la conexión
        
        # Continuar con el siguiente middleware
        return await super().__call__(scope, receive, send)


def JWTAuthMiddlewareStack(inner):
    """Stack de middleware que incluye autenticación JWT."""
    return JWTAuthMiddleware(inner)

