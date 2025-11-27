"""
Vistas de API para Autenticación
Implementa los endpoints definidos en openapi.yml
"""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model, authenticate

from sigot.infrastructure.api.serializers.auth import (
    UserRegisterSerializer,
    AuthResponseSerializer,
    UserSerializer
)
from sigot.application.use_cases.registro import RegistrarTransportista
from sigot.infrastructure.repositories.orm_transportista_repository import (
    TransportistaRepositoryORM
)

User = get_user_model()


class RegisterView(APIView):
    """
    Vista para registro de nuevos usuarios.
    Endpoint: POST /api/auth/register/
    
    Según openapi.yml:
    - Crea un nuevo usuario
    - Si is_transportista=True, crea perfil Transportista con trial_end a 3 meses
    - Retorna token JWT y datos del usuario
    """
    permission_classes = [AllowAny]  # Permitir acceso sin autenticación

    def post(self, request):
        """
        Registra un nuevo usuario.
        
        Request body (RegisterRequest):
        - username: str (min 3, max 150)
        - email: str (único)
        - password: str (min 8)
        - phone: str (opcional)
        - is_transportista: bool
        
        Response (201 Created):
        - access: JWT token
        - refresh: JWT refresh token (opcional)
        - user: User object
        """
        # Verificar duplicados antes de validar el serializer
        email = request.data.get('email')
        username = request.data.get('username')
        
        if email and User.objects.filter(email=email).exists():
            return Response(
                {
                    'error': 'CONFLICT',
                    'message': 'El email ya está registrado'
                },
                status=status.HTTP_409_CONFLICT
            )
        
        if username and User.objects.filter(username=username).exists():
            return Response(
                {
                    'error': 'CONFLICT',
                    'message': 'El nombre de usuario ya está registrado'
                },
                status=status.HTTP_409_CONFLICT
            )
        
        serializer = UserRegisterSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                {
                    'error': 'VALIDATION_ERROR',
                    'message': 'Los datos proporcionados no son válidos',
                    'details': serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Ejecutar el caso de uso
        registro_data = serializer.validated_data
        repository = TransportistaRepositoryORM()
        use_case = RegistrarTransportista(repository=repository)
        
        try:
            resultado = use_case.execute(registro_data)
        except Exception as e:
            return Response(
                {
                    'error': 'INTERNAL_ERROR',
                    'message': f'Error al crear el usuario: {str(e)}'
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Obtener el usuario creado
        user_id = resultado.get('user_id') or resultado.get('id')
        user = User.objects.get(id=user_id)
        
        # Generar tokens JWT
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        
        # Preparar respuesta según AuthResponse de openapi.yml
        response_data = {
            'access': access_token,
            'refresh': str(refresh),
            'user': UserSerializer(user).data
        }
        
        return Response(
            AuthResponseSerializer(response_data).data,
            status=status.HTTP_201_CREATED
        )


class LoginView(APIView):
    """
    Vista para inicio de sesión de usuarios.
    Endpoint: POST /api/auth/login/
    
    Según openapi.yml:
    - Autentica un usuario con username y password
    - Retorna token JWT y datos del usuario
    """
    permission_classes = [AllowAny]  # Permitir acceso sin autenticación

    def post(self, request):
        """
        Autentica un usuario y retorna tokens JWT.
        
        Request body (LoginRequest):
        - username: str
        - password: str
        
        Response (200 OK):
        - access: JWT token
        - refresh: JWT refresh token (opcional)
        - user: User object
        """
        username = request.data.get('username')
        password = request.data.get('password')
        
        # Validar que se proporcionen username y password
        if not username or not password:
            return Response(
                {
                    'error': 'VALIDATION_ERROR',
                    'message': 'Username y password son requeridos'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Autenticar usuario
        user = authenticate(username=username, password=password)
        
        if user is None:
            return Response(
                {
                    'error': 'UNAUTHORIZED',
                    'message': 'Credenciales inválidas'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Generar tokens JWT
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        
        # Preparar respuesta según AuthResponse de openapi.yml
        response_data = {
            'access': access_token,
            'refresh': str(refresh),
            'user': UserSerializer(user).data
        }
        
        return Response(
            AuthResponseSerializer(response_data).data,
            status=status.HTTP_200_OK
        )

