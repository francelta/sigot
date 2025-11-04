"""
Django REST Framework Serializers for ConnecMaq API.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .models import (
    ConstructorProfile,
    ProviderProfile,
    Machine,
    MachineImage,
    ChatRoom,
    Message
)

User = get_user_model()


# ==================== USER SERIALIZERS ====================

class UserSerializer(serializers.ModelSerializer):
    """Basic user serializer for nested representations"""
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'full_name', 
                  'is_constructor', 'is_provider', 'date_joined']
        read_only_fields = ['id', 'date_joined']
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or obj.username


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True, label="Confirm Password")
    user_type = serializers.ChoiceField(
        choices=['constructor', 'provider'],
        write_only=True,
        required=True,
        help_text="Choose 'constructor' or 'provider'"
    )
    
    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2', 'first_name', 'last_name', 
                  'user_type', 'is_constructor', 'is_provider']
        read_only_fields = ['is_constructor', 'is_provider']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Las contraseñas no coinciden."})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user_type = validated_data.pop('user_type')
        password = validated_data.pop('password')
        
        # Set user type flags
        if user_type == 'constructor':
            validated_data['is_constructor'] = True
        elif user_type == 'provider':
            validated_data['is_provider'] = True
        
        user = User.objects.create_user(password=password, **validated_data)
        return user


class UserDetailSerializer(serializers.ModelSerializer):
    """Detailed user serializer with profile information"""
    constructor_profile = serializers.SerializerMethodField()
    provider_profile = serializers.SerializerMethodField()
    
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name',
                  'is_constructor', 'is_provider', 'date_joined',
                  'constructor_profile', 'provider_profile']
        read_only_fields = ['id', 'email', 'date_joined']
    
    def get_constructor_profile(self, obj):
        if hasattr(obj, 'constructor_profile'):
            return ConstructorProfileSerializer(obj.constructor_profile).data
        return None
    
    def get_provider_profile(self, obj):
        if hasattr(obj, 'provider_profile'):
            return ProviderProfileSerializer(obj.provider_profile).data
        return None


# ==================== CONSTRUCTOR PROFILE SERIALIZERS ====================

class ConstructorProfileSerializer(serializers.ModelSerializer):
    """Serializer for Constructor profiles"""
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = ConstructorProfile
        fields = ['user', 'user_id', 'company_name', 'phone', 'address',
                  'city', 'region', 'country', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def create(self, validated_data):
        # Get user from context if not provided
        if 'user_id' not in validated_data:
            user = self.context['request'].user
            validated_data['user'] = user
        else:
            user_id = validated_data.pop('user_id')
            validated_data['user'] = User.objects.get(id=user_id)
        
        return super().create(validated_data)


# ==================== PROVIDER PROFILE SERIALIZERS ====================

class ProviderProfileListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing providers (search results)"""
    user_email = serializers.EmailField(source='user.email', read_only=True)
    machines_count = serializers.IntegerField(source='machines.count', read_only=True)
    
    class Meta:
        model = ProviderProfile
        fields = ['user', 'user_email', 'company_name', 'description', 'logo',
                  'city', 'region', 'country', 'available_within_48h',
                  'is_verified', 'rating', 'total_reviews', 'machines_count',
                  'created_at']
        read_only_fields = ['user', 'user_email', 'rating', 'total_reviews', 
                           'is_verified', 'created_at']


class ProviderProfileSerializer(serializers.ModelSerializer):
    """Full serializer for Provider profiles"""
    user = UserSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True, required=False)
    machines = serializers.SerializerMethodField()
    is_subscription_active = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = ProviderProfile
        fields = ['user', 'user_id', 'company_name', 'description', 'logo',
                  'phone', 'website', 'address', 'city', 'region', 'country',
                  'subscription_status', 'subscription_start_date', 'subscription_end_date',
                  'available_within_48h', 'is_verified', 'rating', 'total_reviews',
                  'machines', 'is_subscription_active', 'created_at', 'updated_at']
        read_only_fields = ['user', 'rating', 'total_reviews', 'is_verified',
                           'subscription_status', 'subscription_start_date', 
                           'subscription_end_date', 'created_at', 'updated_at']
    
    def get_machines(self, obj):
        # Import here to avoid circular imports
        from .serializers import MachineListSerializer
        machines = obj.machines.filter(is_available=True)[:10]  # Limit to 10 machines
        return MachineListSerializer(machines, many=True).data
    
    def create(self, validated_data):
        # Get user from context if not provided
        if 'user_id' not in validated_data:
            user = self.context['request'].user
            validated_data['user'] = user
        else:
            user_id = validated_data.pop('user_id')
            validated_data['user'] = User.objects.get(id=user_id)
        
        return super().create(validated_data)


# ==================== MACHINE SERIALIZERS ====================

class MachineImageSerializer(serializers.ModelSerializer):
    """Serializer for machine images"""
    
    class Meta:
        model = MachineImage
        fields = ['id', 'image', 'caption', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']


class MachineListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing machines"""
    provider_name = serializers.CharField(source='provider.company_name', read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = Machine
        fields = ['id', 'name', 'category', 'category_display', 'brand', 'model',
                  'main_image', 'price_per_hour', 'price_per_day', 'is_available',
                  'provider', 'provider_name', 'created_at']
        read_only_fields = ['id', 'provider', 'provider_name', 'created_at']


class MachineDetailSerializer(serializers.ModelSerializer):
    """Full serializer for machine details"""
    provider = ProviderProfileListSerializer(read_only=True)
    provider_id = serializers.PrimaryKeyRelatedField(
        queryset=ProviderProfile.objects.all(),
        source='provider',
        write_only=True,
        required=False
    )
    images = MachineImageSerializer(many=True, read_only=True)
    category_display = serializers.CharField(source='get_category_display', read_only=True)
    
    class Meta:
        model = Machine
        fields = ['id', 'provider', 'provider_id', 'name', 'category', 'category_display',
                  'description', 'brand', 'model', 'year', 'price_per_hour', 'price_per_day',
                  'is_available', 'main_image', 'images', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        # Set provider from request user if not provided
        if 'provider' not in validated_data:
            user = self.context['request'].user
            if hasattr(user, 'provider_profile'):
                validated_data['provider'] = user.provider_profile
            else:
                raise serializers.ValidationError(
                    "User must have a provider profile to create machines."
                )
        
        return super().create(validated_data)


# ==================== CHAT SERIALIZERS ====================

class MessageSerializer(serializers.ModelSerializer):
    """Serializer for chat messages"""
    author = UserSerializer(read_only=True)
    author_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Message
        fields = ['id', 'room', 'author', 'author_id', 'content', 'timestamp', 'read']
        read_only_fields = ['id', 'timestamp']
    
    def create(self, validated_data):
        # Get author from context if not provided
        if 'author_id' not in validated_data:
            validated_data['author'] = self.context['request'].user
        else:
            author_id = validated_data.pop('author_id')
            validated_data['author'] = User.objects.get(id=author_id)
        
        return super().create(validated_data)


class ChatRoomListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for listing chat rooms"""
    participants = UserSerializer(many=True, read_only=True)
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()
    
    class Meta:
        model = ChatRoom
        fields = ['id', 'participants', 'last_message', 'unread_count', 
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_last_message(self, obj):
        last_msg = obj.last_message
        if last_msg:
            return {
                'id': last_msg.id,
                'content': last_msg.content,
                'author_id': last_msg.author.id,
                'timestamp': last_msg.timestamp,
                'read': last_msg.read
            }
        return None
    
    def get_unread_count(self, obj):
        user = self.context['request'].user
        return obj.messages.filter(read=False).exclude(author=user).count()


class ChatRoomDetailSerializer(serializers.ModelSerializer):
    """Full serializer for chat room with messages"""
    participants = UserSerializer(many=True, read_only=True)
    participant_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    messages = MessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = ChatRoom
        fields = ['id', 'participants', 'participant_ids', 'messages', 
                  'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        participant_ids = validated_data.pop('participant_ids', [])
        
        # Add current user to participants if not included
        current_user_id = self.context['request'].user.id
        if current_user_id not in participant_ids:
            participant_ids.append(current_user_id)
        
        # Create chat room
        chat_room = ChatRoom.objects.create()
        
        # Add participants
        users = User.objects.filter(id__in=participant_ids)
        chat_room.participants.set(users)
        
        return chat_room


# ==================== SPECIAL SERIALIZERS ====================

class ProviderSearchSerializer(serializers.Serializer):
    """Serializer for provider search parameters"""
    category = serializers.CharField(required=False, help_text="Machine category")
    city = serializers.CharField(required=False, help_text="City filter")
    region = serializers.CharField(required=False, help_text="Region filter")
    available_within_48h = serializers.BooleanField(
        default=True,
        help_text="Filter by 48h availability"
    )
    min_rating = serializers.DecimalField(
        max_digits=3,
        decimal_places=2,
        required=False,
        help_text="Minimum rating (0-5)"
    )
    verified_only = serializers.BooleanField(
        default=False,
        help_text="Show only verified providers"
    )

