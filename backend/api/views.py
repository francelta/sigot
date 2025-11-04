"""
Django REST Framework ViewSets for ConnecMaq API.
"""

from rest_framework import viewsets, status, filters, serializers as drf_serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from django.contrib.auth import get_user_model
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404

from .models import (
    ConstructorProfile,
    ProviderProfile,
    Machine,
    MachineImage,
    ChatRoom,
    Message
)
from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    UserDetailSerializer,
    ConstructorProfileSerializer,
    ProviderProfileSerializer,
    ProviderProfileListSerializer,
    MachineListSerializer,
    MachineDetailSerializer,
    MachineImageSerializer,
    ChatRoomListSerializer,
    ChatRoomDetailSerializer,
    MessageSerializer,
    ProviderSearchSerializer
)

User = get_user_model()


# ==================== USER VIEWSETS ====================

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for user management.
    
    Endpoints:
    - GET /api/users/ - List users (admin only)
    - POST /api/users/ - Register new user
    - GET /api/users/{id}/ - Get user detail
    - PUT/PATCH /api/users/{id}/ - Update user
    - DELETE /api/users/{id}/ - Delete user
    - GET /api/users/me/ - Get current user profile
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return UserRegistrationSerializer
        elif self.action == 'retrieve' or self.action == 'me':
            return UserDetailSerializer
        return UserSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Get current user's profile"""
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['patch'], permission_classes=[IsAuthenticated])
    def update_profile(self, request):
        """Update current user's basic profile"""
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


# ==================== CONSTRUCTOR PROFILE VIEWSETS ====================

class ConstructorProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Constructor profiles.
    
    Endpoints:
    - GET /api/constructor-profiles/ - List all constructor profiles
    - POST /api/constructor-profiles/ - Create constructor profile
    - GET /api/constructor-profiles/{id}/ - Get constructor profile
    - PUT/PATCH /api/constructor-profiles/{id}/ - Update constructor profile
    - DELETE /api/constructor-profiles/{id}/ - Delete constructor profile
    """
    queryset = ConstructorProfile.objects.all()
    serializer_class = ConstructorProfileSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['company_name', 'city', 'region']
    ordering_fields = ['created_at', 'company_name']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # Users can only see their own profile or all if staff
        if not self.request.user.is_staff:
            queryset = queryset.filter(user=self.request.user)
        return queryset
    
    def perform_create(self, serializer):
        # Automatically set the user to the current user
        serializer.save(user=self.request.user)


# ==================== PROVIDER PROFILE VIEWSETS ====================

class ProviderProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Provider profiles.
    
    Endpoints:
    - GET /api/providers/ - List all providers (public)
    - POST /api/providers/ - Create provider profile
    - GET /api/providers/{id}/ - Get provider detail
    - PUT/PATCH /api/providers/{id}/ - Update provider profile
    - DELETE /api/providers/{id}/ - Delete provider profile
    - GET /api/providers/search/ - Search providers with filters
    - PATCH /api/providers/{id}/toggle_availability/ - Toggle 48h availability
    """
    queryset = ProviderProfile.objects.all()
    serializer_class = ProviderProfileSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['company_name', 'description', 'city', 'region']
    ordering_fields = ['rating', 'created_at', 'company_name']
    ordering = ['-available_within_48h', '-rating', '-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'search':
            return ProviderProfileListSerializer
        return ProviderProfileSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # For update/delete, users can only access their own profile
        if self.action in ['update', 'partial_update', 'destroy']:
            if not self.request.user.is_staff:
                queryset = queryset.filter(user=self.request.user)
        
        # For list view, filter by active subscriptions and verified
        if self.action == 'list':
            queryset = queryset.filter(
                subscription_status='active',
                is_verified=True
            )
        
        return queryset
    
    def perform_create(self, serializer):
        # Automatically set the user to the current user
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'], permission_classes=[AllowAny])
    def search(self, request):
        """
        Advanced search endpoint for constructors to find providers.
        
        Query Parameters:
        - category: Machine category filter
        - city: City filter
        - region: Region filter
        - available_within_48h: Filter by 48h availability (default: true)
        - min_rating: Minimum rating filter
        - verified_only: Show only verified providers
        """
        # Validate search parameters
        search_serializer = ProviderSearchSerializer(data=request.query_params)
        search_serializer.is_valid(raise_exception=True)
        params = search_serializer.validated_data
        
        # Start with active and verified providers
        queryset = ProviderProfile.objects.filter(
            subscription_status='active',
            is_verified=True
        )
        
        # Apply filters
        if params.get('available_within_48h', True):
            queryset = queryset.filter(available_within_48h=True)
        
        if 'city' in params:
            queryset = queryset.filter(city__icontains=params['city'])
        
        if 'region' in params:
            queryset = queryset.filter(region__icontains=params['region'])
        
        if 'min_rating' in params:
            queryset = queryset.filter(rating__gte=params['min_rating'])
        
        if params.get('verified_only', False):
            queryset = queryset.filter(is_verified=True)
        
        # Filter by machine category if specified
        if 'category' in params:
            queryset = queryset.filter(
                machines__category=params['category']
            ).distinct()
        
        # Annotate with machine count
        queryset = queryset.annotate(
            machines_count=Count('machines', filter=Q(machines__is_available=True))
        )
        
        # Order by availability, rating, and machines count
        queryset = queryset.order_by(
            '-available_within_48h',
            '-rating',
            '-machines_count'
        )
        
        # Paginate results
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = ProviderProfileListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = ProviderProfileListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def toggle_availability(self, request, pk=None):
        """
        Toggle the 48-hour availability status.
        Only the provider themselves can toggle this.
        """
        provider = self.get_object()
        
        # Check if user owns this profile
        if provider.user != request.user and not request.user.is_staff:
            return Response(
                {'detail': 'No tienes permiso para modificar este perfil.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Toggle availability
        provider.available_within_48h = not provider.available_within_48h
        provider.save()
        
        serializer = self.get_serializer(provider)
        return Response(serializer.data)


# ==================== MACHINE VIEWSETS ====================

class MachineViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Machines.
    
    Endpoints:
    - GET /api/machines/ - List all machines
    - POST /api/machines/ - Create machine (providers only)
    - GET /api/machines/{id}/ - Get machine detail
    - PUT/PATCH /api/machines/{id}/ - Update machine
    - DELETE /api/machines/{id}/ - Delete machine
    - PATCH /api/machines/{id}/toggle_availability/ - Toggle availability
    """
    queryset = Machine.objects.all()
    serializer_class = MachineDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'brand', 'model', 'category']
    ordering_fields = ['created_at', 'price_per_day', 'name']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return MachineListSerializer
        return MachineDetailSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by provider if specified
        provider_id = self.request.query_params.get('provider', None)
        if provider_id:
            queryset = queryset.filter(provider_id=provider_id)
        
        # Filter by category if specified
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        
        # Filter by availability
        available_only = self.request.query_params.get('available_only', None)
        if available_only and available_only.lower() == 'true':
            queryset = queryset.filter(is_available=True)
        
        # For update/delete, users can only access their own machines
        if self.action in ['update', 'partial_update', 'destroy']:
            if not self.request.user.is_staff:
                queryset = queryset.filter(provider__user=self.request.user)
        
        return queryset
    
    def perform_create(self, serializer):
        # Automatically set the provider to the current user's provider profile
        if hasattr(self.request.user, 'provider_profile'):
            serializer.save(provider=self.request.user.provider_profile)
        else:
            raise drf_serializers.ValidationError(
                'Debes tener un perfil de proveedor para crear maquinaria.'
            )
    
    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def toggle_availability(self, request, pk=None):
        """Toggle machine availability status"""
        machine = self.get_object()
        
        # Check if user owns this machine
        if machine.provider.user != request.user and not request.user.is_staff:
            return Response(
                {'detail': 'No tienes permiso para modificar esta maquinaria.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Toggle availability
        machine.is_available = not machine.is_available
        machine.save()
        
        serializer = self.get_serializer(machine)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_images(self, request, pk=None):
        """Add images to a machine"""
        machine = self.get_object()
        
        # Check if user owns this machine
        if machine.provider.user != request.user and not request.user.is_staff:
            return Response(
                {'detail': 'No tienes permiso para modificar esta maquinaria.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Handle image upload
        images_data = request.FILES.getlist('images')
        captions = request.data.getlist('captions', [])
        
        created_images = []
        for idx, image_file in enumerate(images_data):
            caption = captions[idx] if idx < len(captions) else ''
            machine_image = MachineImage.objects.create(
                machine=machine,
                image=image_file,
                caption=caption
            )
            created_images.append(machine_image)
        
        serializer = MachineImageSerializer(created_images, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# ==================== CHAT VIEWSETS ====================

class ChatRoomViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Chat Rooms.
    
    Endpoints:
    - GET /api/chat-rooms/ - List user's chat rooms
    - POST /api/chat-rooms/ - Create or get existing chat room
    - GET /api/chat-rooms/{id}/ - Get chat room with messages
    - DELETE /api/chat-rooms/{id}/ - Delete chat room
    - GET /api/chat-rooms/find_or_create/ - Find or create chat between two users
    """
    queryset = ChatRoom.objects.all()
    serializer_class = ChatRoomDetailSerializer
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ChatRoomListSerializer
        return ChatRoomDetailSerializer
    
    def get_queryset(self):
        # Users can only see their own chat rooms
        return ChatRoom.objects.filter(
            participants=self.request.user
        ).distinct()
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def find_or_create(self, request):
        """
        Find or create a chat room between current user and another user.
        
        Body: {"other_user_id": 123}
        """
        other_user_id = request.data.get('other_user_id')
        
        if not other_user_id:
            return Response(
                {'detail': 'Se requiere other_user_id.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get the other user
        other_user = get_object_or_404(User, id=other_user_id)
        
        # Check if a chat room already exists between these two users
        chat_room = ChatRoom.objects.filter(
            participants=request.user
        ).filter(
            participants=other_user
        ).first()
        
        # If not, create a new one
        if not chat_room:
            chat_room = ChatRoom.objects.create()
            chat_room.participants.add(request.user, other_user)
        
        serializer = ChatRoomDetailSerializer(chat_room, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Messages.
    
    Endpoints:
    - GET /api/messages/ - List messages (filtered by room)
    - POST /api/messages/ - Send a message
    - GET /api/messages/{id}/ - Get message detail
    - PATCH /api/messages/{id}/ - Update message (mark as read)
    - DELETE /api/messages/{id}/ - Delete message
    - POST /api/messages/{id}/mark_read/ - Mark message as read
    """
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['timestamp']
    ordering = ['timestamp']
    
    def get_queryset(self):
        queryset = Message.objects.filter(
            room__participants=self.request.user
        )
        
        # Filter by room if specified
        room_id = self.request.query_params.get('room', None)
        if room_id:
            queryset = queryset.filter(room_id=room_id)
        
        return queryset
    
    def perform_create(self, serializer):
        # Automatically set the author to the current user
        serializer.save(author=self.request.user)
    
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def mark_read(self, request, pk=None):
        """Mark a message as read"""
        message = self.get_object()
        
        # Only the recipient can mark as read (not the author)
        if message.author != request.user:
            message.read = True
            message.save()
        
        serializer = self.get_serializer(message)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def mark_room_read(self, request):
        """
        Mark all messages in a room as read.
        
        Body: {"room_id": 123}
        """
        room_id = request.data.get('room_id')
        
        if not room_id:
            return Response(
                {'detail': 'Se requiere room_id.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Mark all unread messages in the room as read (except own messages)
        updated_count = Message.objects.filter(
            room_id=room_id,
            read=False
        ).exclude(
            author=request.user
        ).update(read=True)
        
        return Response({
            'detail': f'{updated_count} mensajes marcados como leídos.'
        })
