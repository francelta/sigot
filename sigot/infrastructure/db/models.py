"""
Modelos de Dominio para SIGOT
Adaptador de Base de Datos - Contrato de Datos del ORM

Este archivo define los modelos de Django que representan el dominio del negocio.
Estos modelos residen en la capa de Infrastructure porque dependen de Django/GeoDjango.
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class User(AbstractUser):
    """
    Modelo de Usuario extendido de Django.
    Base para todos los usuarios del sistema (transportistas y clientes).
    """
    email = models.EmailField(unique=True, blank=False, null=False)
    phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.username} ({self.email})"


class Categoria(models.Model):
    """
    Categorías de transporte con soporte para jerarquías (subcategorías).
    Ejemplo: "Mercancías" > "Mercancías Peligrosas" > "Explosivos"
    """
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        help_text='Categoría padre para crear jerarquías'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'categorias'
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['nombre']

    def __str__(self):
        if self.parent:
            return f"{self.parent.nombre} > {self.nombre}"
        return self.nombre

    def get_full_path(self):
        """Retorna la ruta completa de la categoría en la jerarquía."""
        path = [self.nombre]
        current = self.parent
        while current:
            path.insert(0, current.nombre)
            current = current.parent
        return ' > '.join(path)


class Transportista(models.Model):
    """
    Perfil de Transportista.
    Relación 1-a-1 con User.
    Sistema de búsqueda por Zona de Actuación (no ubicación en tiempo real).
    """
    TIPO_ZONA_CHOICES = [
        ('RADIO', 'Radio'),
        ('ZONAS', 'Zonas'),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='transportista',
        primary_key=True
    )
    disponible = models.BooleanField(
        default=False,
        help_text='Indica si el transportista está disponible para recibir solicitudes'
    )
    codigo_postal = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text='Código postal para geocodificar la base de actuación'
    )
    # Coordenadas geocodificadas (usando FloatField en lugar de PointField para compatibilidad con PostgreSQL sin PostGIS)
    base_latitud = models.FloatField(
        null=True,
        blank=True,
        help_text='Latitud geocodificada desde codigo_postal'
    )
    base_longitud = models.FloatField(
        null=True,
        blank=True,
        help_text='Longitud geocodificada desde codigo_postal'
    )
    tipo_zona_actuacion = models.CharField(
        max_length=10,
        choices=TIPO_ZONA_CHOICES,
        default='RADIO',
        help_text='Tipo de zona de actuación: Radio (km) o Zonas (provincias/regiones)'
    )
    radio_km_general = models.IntegerField(
        null=True,
        blank=True,
        help_text='Radio de actuación general en kilómetros (usado si no hay radio_km_especifico en TransportistaCategoria)'
    )
    zonas_definidas = models.JSONField(
        null=True,
        blank=True,
        help_text='Zonas definidas manualmente (solo si tipo_zona_actuacion == ZONAS). Ej: {"provincias": ["Madrid", "Barcelona"], "nacional": true}'
    )
    foto_de_perfil = models.ImageField(
        upload_to='transportistas/perfiles/%Y/%m/%d/',
        blank=True,
        null=True,
        help_text='Foto de perfil del transportista (para el chat)'
    )
    trial_end = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Fecha de finalización del período de prueba (3 meses desde el registro)'
    )
    categorias = models.ManyToManyField(
        Categoria,
        through='TransportistaCategoria',
        related_name='transportistas',
        blank=True,
        help_text='Categorías de transporte (maquinaria) que maneja este transportista'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'transportistas'
        verbose_name = 'Transportista'
        verbose_name_plural = 'Transportistas'
        # Índice GiST para consultas geoespaciales eficientes
        indexes = [
            models.Index(fields=['disponible']),
            models.Index(fields=['trial_end']),
        ]

    def __str__(self):
        return f"Transportista: {self.user.username}"

    def is_trial_active(self):
        """Verifica si el período de prueba está activo."""
        if not self.trial_end:
            return False
        return timezone.now() < self.trial_end

    def can_be_available(self):
        """
        Verifica si el transportista puede ponerse disponible.
        Requiere: trial activo y zona de actuación configurada.
        """
        if not self.is_trial_active():
            return False
        
        if self.tipo_zona_actuacion == 'RADIO':
            return self.base_latitud is not None and self.base_longitud is not None and (self.radio_km_general is not None or self.transportistacategoria_set.exists())
        elif self.tipo_zona_actuacion == 'ZONAS':
            return self.zonas_definidas is not None
        
        return False


class TransportistaCategoria(models.Model):
    """
    Modelo 'through' para la relación M2M entre Transportista y Categoria.
    Almacena información específica de cada máquina/vehículo del transportista:
    - radio_km_especifico: Radio de actuación específico para esta máquina (si es null, usa radio_km_general del transportista)
    - nombre_vehiculo: Nombre personalizado del vehículo (ej. "Mi Furgoneta Mercedes")
    - marca: Marca del vehículo (ej. "Mercedes", "Volvo", "Caterpillar")
    - tonelaje: Tonelaje o capacidad de carga del vehículo
    - caracteristicas: Descripción detallada de características especiales
    - imagen_maquina: Imagen de la máquina
    """
    transportista = models.ForeignKey(
        Transportista,
        on_delete=models.CASCADE,
        related_name='transportistacategoria_set',
        help_text='Transportista propietario de esta máquina'
    )
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        related_name='transportistacategoria_set',
        help_text='Categoría (máquina) del transportista'
    )
    radio_km_especifico = models.IntegerField(
        null=True,
        blank=True,
        help_text='Radio de actuación específico para esta máquina en kilómetros. Si es null, usa radio_km_general del transportista'
    )
    nombre_vehiculo = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        help_text='Nombre personalizado del vehículo (ej. "Mi Furgoneta Mercedes")'
    )
    marca = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='Marca del vehículo (ej. "Mercedes", "Volvo", "Caterpillar")'
    )
    tonelaje = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text='Tonelaje o capacidad de carga del vehículo'
    )
    caracteristicas = models.TextField(
        blank=True,
        null=True,
        help_text='Descripción detallada de características especiales del vehículo'
    )
    imagen_maquina = models.ImageField(
        upload_to='transportistas/maquinas/%Y/%m/%d/',
        blank=True,
        null=True,
        help_text='Imagen de la máquina'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'transportista_categoria'
        verbose_name = 'Máquina del Transportista'
        verbose_name_plural = 'Máquinas de los Transportistas'
        unique_together = [['transportista', 'categoria']]
        indexes = [
            models.Index(fields=['transportista', 'categoria']),
        ]

    def __str__(self):
        return f"{self.transportista.user.username} - {self.categoria.nombre}"

    def get_radio_km_efectivo(self):
        """
        Retorna el radio de actuación efectivo para esta máquina.
        Si tiene radio_km_especifico, lo usa; si no, usa el radio_km_general del transportista.
        """
        if self.radio_km_especifico is not None:
            return self.radio_km_especifico
        return self.transportista.radio_km_general


class Valoracion(models.Model):
    """
    Sistema de valoraciones entre usuarios.
    Un usuario puede valorar a otro (ej. cliente valora transportista).
    """
    RATING_CHOICES = [
        (1, '1 - Muy Malo'),
        (2, '2 - Malo'),
        (3, '3 - Regular'),
        (4, '4 - Bueno'),
        (5, '5 - Excelente'),
    ]

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='valoraciones_enviadas',
        help_text='Usuario que envía la valoración'
    )
    rated_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='valoraciones_recibidas',
        help_text='Usuario que recibe la valoración'
    )
    rating = models.IntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text='Calificación de 1 a 5 estrellas'
    )
    comment = models.TextField(
        blank=True,
        null=True,
        help_text='Comentario opcional sobre la valoración'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'valoraciones'
        verbose_name = 'Valoración'
        verbose_name_plural = 'Valoraciones'
        # Un usuario solo puede valorar a otro una vez
        unique_together = [['author', 'rated_user']]
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['rated_user', '-created_at']),
        ]

    def __str__(self):
        return f"{self.author.username} → {self.rated_user.username}: {self.rating}⭐"

    def clean(self):
        """Valida que un usuario no se valore a sí mismo."""
        from django.core.exceptions import ValidationError
        if self.author == self.rated_user:
            raise ValidationError('Un usuario no puede valorarse a sí mismo.')


class ChatRoom(models.Model):
    """
    Sala de chat entre usuarios.
    Soporta conversaciones 1-a-1 y grupales (M2M con User).
    """
    participants = models.ManyToManyField(
        User,
        through='UserChatSettings',
        related_name='chat_rooms',
        help_text='Usuarios participantes en esta sala'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'chat_rooms'
        verbose_name = 'Sala de Chat'
        verbose_name_plural = 'Salas de Chat'
        ordering = ['-updated_at']

    def __str__(self):
        participant_names = ', '.join([u.username for u in self.participants.all()[:3]])
        if self.participants.count() > 3:
            participant_names += '...'
        return f"Chat: {participant_names}"


class UserChatSettings(models.Model):
    """
    Modelo 'through' para la relación M2M entre User y ChatRoom.
    Almacena configuraciones específicas de cada usuario en cada sala.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='chat_settings'
    )
    chatroom = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,
        related_name='user_settings'
    )
    is_favorite = models.BooleanField(
        default=False,
        help_text='Indica si el usuario ha marcado esta sala como favorita'
    )
    is_muted = models.BooleanField(
        default=False,
        help_text='Indica si el usuario ha silenciado las notificaciones de esta sala'
    )
    last_read_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Última vez que el usuario leyó mensajes en esta sala'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_chat_settings'
        verbose_name = 'Configuración de Chat de Usuario'
        verbose_name_plural = 'Configuraciones de Chat de Usuarios'
        unique_together = [['user', 'chatroom']]
        indexes = [
            models.Index(fields=['user', 'is_favorite']),
        ]

    def __str__(self):
        return f"{self.user.username} en {self.chatroom.id} (favorito: {self.is_favorite})"


class Message(models.Model):
    """
    Mensaje dentro de una sala de chat.
    Soporta texto y archivos adjuntos.
    """
    chatroom = models.ForeignKey(
        ChatRoom,
        on_delete=models.CASCADE,
        related_name='messages',
        help_text='Sala de chat a la que pertenece este mensaje'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='messages',
        help_text='Usuario que envió el mensaje'
    )
    body = models.TextField(
        help_text='Contenido del mensaje'
    )
    attachment = models.FileField(
        upload_to='chat/attachments/%Y/%m/%d/',
        blank=True,
        null=True,
        help_text='Archivo adjunto opcional (imagen, documento, etc.)'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'messages'
        verbose_name = 'Mensaje'
        verbose_name_plural = 'Mensajes'
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['chatroom', '-created_at']),
            models.Index(fields=['author', '-created_at']),
        ]

    def __str__(self):
        preview = self.body[:50] + '...' if len(self.body) > 50 else self.body
        return f"{self.author.username}: {preview}"

    def has_attachment(self):
        """Verifica si el mensaje tiene un archivo adjunto."""
        return bool(self.attachment)

