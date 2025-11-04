from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import (
    User, 
    ConstructorProfile, 
    ProviderProfile, 
    Machine, 
    MachineImage,
    ChatRoom, 
    Message
)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin interface for custom User model"""
    list_display = ['email', 'username', 'first_name', 'last_name', 'is_constructor', 'is_provider', 'is_staff']
    list_filter = ['is_constructor', 'is_provider', 'is_staff', 'is_superuser', 'is_active']
    search_fields = ['email', 'username', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('User Type'), {'fields': ('is_constructor', 'is_provider')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_constructor', 'is_provider'),
        }),
    )


@admin.register(ConstructorProfile)
class ConstructorProfileAdmin(admin.ModelAdmin):
    """Admin interface for Constructor profiles"""
    list_display = ['company_name', 'get_email', 'city', 'country', 'created_at']
    list_filter = ['country', 'region', 'created_at']
    search_fields = ['company_name', 'user__email', 'city']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        (_('User Information'), {
            'fields': ('user',)
        }),
        (_('Company Details'), {
            'fields': ('company_name', 'phone', 'address')
        }),
        (_('Location'), {
            'fields': ('city', 'region', 'country')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = _('Email')
    get_email.admin_order_field = 'user__email'


@admin.register(ProviderProfile)
class ProviderProfileAdmin(admin.ModelAdmin):
    """Admin interface for Provider profiles"""
    list_display = ['company_name', 'get_email', 'subscription_status', 'available_within_48h', 'is_verified', 'rating', 'created_at']
    list_filter = ['subscription_status', 'available_within_48h', 'is_verified', 'country', 'created_at']
    search_fields = ['company_name', 'user__email', 'city', 'description']
    readonly_fields = ['created_at', 'updated_at', 'rating', 'total_reviews']
    list_editable = ['available_within_48h', 'is_verified']
    
    fieldsets = (
        (_('User Information'), {
            'fields': ('user',)
        }),
        (_('Company Details'), {
            'fields': ('company_name', 'description', 'logo', 'phone', 'website')
        }),
        (_('Location'), {
            'fields': ('address', 'city', 'region', 'country')
        }),
        (_('Subscription'), {
            'fields': ('subscription_status', 'subscription_start_date', 'subscription_end_date')
        }),
        (_('Service Availability'), {
            'fields': ('available_within_48h', 'is_verified'),
            'description': _('The 48h toggle is the main filter for constructors searching for providers.')
        }),
        (_('Ratings'), {
            'fields': ('rating', 'total_reviews'),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = _('Email')
    get_email.admin_order_field = 'user__email'


class MachineImageInline(admin.TabularInline):
    """Inline admin for machine images"""
    model = MachineImage
    extra = 1
    fields = ['image', 'caption']


@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    """Admin interface for Machines"""
    list_display = ['name', 'category', 'get_provider', 'brand', 'is_available', 'price_per_day', 'created_at']
    list_filter = ['category', 'is_available', 'brand', 'created_at']
    search_fields = ['name', 'description', 'brand', 'model', 'provider__company_name']
    list_editable = ['is_available']
    readonly_fields = ['created_at', 'updated_at']
    inlines = [MachineImageInline]
    
    fieldsets = (
        (_('Provider'), {
            'fields': ('provider',)
        }),
        (_('Basic Information'), {
            'fields': ('name', 'category', 'description')
        }),
        (_('Specifications'), {
            'fields': ('brand', 'model', 'year', 'main_image')
        }),
        (_('Pricing'), {
            'fields': ('price_per_hour', 'price_per_day'),
            'description': _('Pricing is optional and can be negotiated via chat.')
        }),
        (_('Availability'), {
            'fields': ('is_available',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_provider(self, obj):
        return obj.provider.company_name
    get_provider.short_description = _('Provider')
    get_provider.admin_order_field = 'provider__company_name'


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    """Admin interface for Chat Rooms"""
    list_display = ['id', 'get_participants', 'created_at', 'updated_at', 'get_message_count']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['participants__email', 'participants__username']
    readonly_fields = ['created_at', 'updated_at']
    filter_horizontal = ['participants']
    
    def get_participants(self, obj):
        return ", ".join([user.email for user in obj.participants.all()[:3]])
    get_participants.short_description = _('Participants')
    
    def get_message_count(self, obj):
        return obj.messages.count()
    get_message_count.short_description = _('Messages')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    """Admin interface for Messages"""
    list_display = ['id', 'get_author', 'get_room', 'get_content_preview', 'timestamp', 'read']
    list_filter = ['read', 'timestamp']
    search_fields = ['content', 'author__email', 'author__username']
    readonly_fields = ['timestamp']
    list_editable = ['read']
    
    fieldsets = (
        (_('Message Details'), {
            'fields': ('room', 'author', 'content')
        }),
        (_('Status'), {
            'fields': ('read', 'timestamp')
        }),
    )
    
    def get_author(self, obj):
        return obj.author.email
    get_author.short_description = _('Author')
    get_author.admin_order_field = 'author__email'
    
    def get_room(self, obj):
        return f"Room #{obj.room.id}"
    get_room.short_description = _('Room')
    
    def get_content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    get_content_preview.short_description = _('Content')
