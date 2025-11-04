from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Custom User model that extends Django's AbstractUser.
    Supports both Constructor and Provider user types.
    """
    email = models.EmailField(_('email address'), unique=True)
    is_constructor = models.BooleanField(
        _('constructor status'),
        default=False,
        help_text=_('Designates whether this user is a constructor (free user).')
    )
    is_provider = models.BooleanField(
        _('provider status'),
        default=False,
        help_text=_('Designates whether this user is a provider (subscription user).')
    )
    
    # Override username to make email the primary identifier
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
    
    def __str__(self):
        return self.email


class ConstructorProfile(models.Model):
    """
    Profile for Constructor users (free tier).
    Constructors search for machinery and services.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='constructor_profile',
        primary_key=True
    )
    company_name = models.CharField(
        _('company name'),
        max_length=255,
        help_text=_('Name of the construction company')
    )
    phone = models.CharField(
        _('phone number'),
        max_length=20,
        blank=True
    )
    address = models.TextField(
        _('address'),
        blank=True
    )
    # Location fields (for future GeoDjango integration)
    city = models.CharField(_('city'), max_length=100, blank=True)
    region = models.CharField(_('region/state'), max_length=100, blank=True)
    country = models.CharField(_('country'), max_length=100, default='Chile')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('constructor profile')
        verbose_name_plural = _('constructor profiles')
    
    def __str__(self):
        return f"{self.company_name} - {self.user.email}"


class ProviderProfile(models.Model):
    """
    Profile for Provider users (paid subscription).
    Providers offer machinery and services.
    """
    SUBSCRIPTION_STATUS_CHOICES = [
        ('trial', _('Trial')),
        ('active', _('Active')),
        ('inactive', _('Inactive')),
        ('cancelled', _('Cancelled')),
    ]
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='provider_profile',
        primary_key=True
    )
    company_name = models.CharField(
        _('company name'),
        max_length=255,
        help_text=_('Name of the provider company')
    )
    description = models.TextField(
        _('description'),
        blank=True,
        help_text=_('Brief description of the company and services offered')
    )
    logo = models.ImageField(
        _('company logo'),
        upload_to='logos/',
        blank=True,
        null=True
    )
    phone = models.CharField(
        _('phone number'),
        max_length=20,
        blank=True
    )
    website = models.URLField(
        _('website'),
        blank=True
    )
    
    # Location fields
    address = models.TextField(_('address'), blank=True)
    city = models.CharField(_('city'), max_length=100, blank=True)
    region = models.CharField(_('region/state'), max_length=100, blank=True)
    country = models.CharField(_('country'), max_length=100, default='Chile')
    
    # Subscription information
    subscription_status = models.CharField(
        _('subscription status'),
        max_length=20,
        choices=SUBSCRIPTION_STATUS_CHOICES,
        default='trial'
    )
    subscription_start_date = models.DateField(
        _('subscription start date'),
        null=True,
        blank=True
    )
    subscription_end_date = models.DateField(
        _('subscription end date'),
        null=True,
        blank=True
    )
    
    # The magic switch: availability within 48 hours
    available_within_48h = models.BooleanField(
        _('available within 48 hours'),
        default=False,
        help_text=_('Toggle to indicate if you can provide services within 48 hours')
    )
    
    # Business verification
    is_verified = models.BooleanField(
        _('verified'),
        default=False,
        help_text=_('Whether the provider has been verified by admin')
    )
    
    # Rating system (for future implementation)
    rating = models.DecimalField(
        _('rating'),
        max_digits=3,
        decimal_places=2,
        default=0.00,
        help_text=_('Average rating from 0 to 5')
    )
    total_reviews = models.PositiveIntegerField(
        _('total reviews'),
        default=0
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('provider profile')
        verbose_name_plural = _('provider profiles')
        ordering = ['-available_within_48h', '-rating', '-created_at']
    
    def __str__(self):
        return f"{self.company_name} - {self.user.email}"
    
    @property
    def is_subscription_active(self):
        """Check if the subscription is currently active"""
        if self.subscription_status != 'active':
            return False
        if self.subscription_end_date:
            from django.utils import timezone
            return self.subscription_end_date >= timezone.now().date()
        return True


class Machine(models.Model):
    """
    Machinery and equipment offered by providers.
    """
    CATEGORY_CHOICES = [
        ('excavator', _('Excavadora')),
        ('crane', _('Grúa')),
        ('truck', _('Camión')),
        ('transport', _('Transporte de Áridos')),
        ('loader', _('Cargador Frontal')),
        ('bulldozer', _('Bulldozer')),
        ('roller', _('Rodillo Compactador')),
        ('mixer', _('Mixer/Hormigonera')),
        ('pump', _('Bomba de Hormigón')),
        ('forklift', _('Grúa Horquilla')),
        ('other', _('Otro')),
    ]
    
    provider = models.ForeignKey(
        ProviderProfile,
        on_delete=models.CASCADE,
        related_name='machines',
        verbose_name=_('provider')
    )
    name = models.CharField(
        _('machine name'),
        max_length=255,
        help_text=_('e.g., "Excavadora CAT 320"')
    )
    category = models.CharField(
        _('category'),
        max_length=50,
        choices=CATEGORY_CHOICES
    )
    description = models.TextField(
        _('description'),
        blank=True,
        help_text=_('Detailed description, specifications, capacity, etc.')
    )
    
    # Specifications
    brand = models.CharField(_('brand'), max_length=100, blank=True)
    model = models.CharField(_('model'), max_length=100, blank=True)
    year = models.PositiveIntegerField(_('year'), null=True, blank=True)
    
    # Pricing (optional, can be negotiated via chat)
    price_per_hour = models.DecimalField(
        _('price per hour'),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_('Hourly rate in local currency')
    )
    price_per_day = models.DecimalField(
        _('price per day'),
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_('Daily rate in local currency')
    )
    
    # Availability
    is_available = models.BooleanField(
        _('currently available'),
        default=True,
        help_text=_('Uncheck if machine is currently in use or under maintenance')
    )
    
    # Images (we'll use a separate model for multiple images)
    main_image = models.ImageField(
        _('main image'),
        upload_to='machines/',
        help_text=_('Image is required for the machine')
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('machine')
        verbose_name_plural = _('machines')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.provider.company_name})"


class MachineImage(models.Model):
    """
    Additional images for machinery (gallery).
    """
    machine = models.ForeignKey(
        Machine,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name=_('machine')
    )
    image = models.ImageField(
        _('image'),
        upload_to='machines/gallery/'
    )
    caption = models.CharField(
        _('caption'),
        max_length=255,
        blank=True
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('machine image')
        verbose_name_plural = _('machine images')
        ordering = ['uploaded_at']
    
    def __str__(self):
        return f"Image for {self.machine.name}"


class ChatRoom(models.Model):
    """
    Chat room between a Constructor and a Provider.
    """
    participants = models.ManyToManyField(
        User,
        related_name='chat_rooms',
        verbose_name=_('participants')
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('chat room')
        verbose_name_plural = _('chat rooms')
        ordering = ['-updated_at']
    
    def __str__(self):
        participant_names = ", ".join([user.email for user in self.participants.all()[:2]])
        return f"Chat: {participant_names}"
    
    @property
    def last_message(self):
        """Get the last message in this room"""
        return self.messages.order_by('-timestamp').first()


class Message(models.Model):
    """
    Individual message in a chat room.
    """
    room = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name=_('chat room')
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='messages',
        verbose_name=_('author')
    )
    content = models.TextField(_('content'))
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(
        _('read'),
        default=False,
        help_text=_('Whether the message has been read by the recipient')
    )
    
    class Meta:
        verbose_name = _('message')
        verbose_name_plural = _('messages')
        ordering = ['timestamp']
    
    def __str__(self):
        return f"{self.author.email}: {self.content[:50]}"
