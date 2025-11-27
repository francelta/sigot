# Generated migration for SIGOT models (PostgreSQL compatible - no PostGIS)

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.core.validators
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
                'db_table': 'users',
                'ordering': ['-created_at'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
                ('descripcion', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('parent', models.ForeignKey(blank=True, help_text='Categoría padre para crear jerarquías', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='db.categoria')),
            ],
            options={
                'verbose_name': 'Categoría',
                'verbose_name_plural': 'Categorías',
                'db_table': 'categorias',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='ChatRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Sala de Chat',
                'verbose_name_plural': 'Salas de Chat',
                'db_table': 'chat_rooms',
                'ordering': ['-updated_at'],
            },
        ),
        migrations.CreateModel(
            name='Transportista',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='transportista', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('disponible', models.BooleanField(default=False, help_text='Indica si el transportista está disponible para recibir solicitudes')),
                ('codigo_postal', models.CharField(blank=True, help_text='Código postal para geocodificar la base de actuación', max_length=10, null=True)),
                ('base_latitud', models.FloatField(blank=True, help_text='Latitud geocodificada desde codigo_postal', null=True)),
                ('base_longitud', models.FloatField(blank=True, help_text='Longitud geocodificada desde codigo_postal', null=True)),
                ('tipo_zona_actuacion', models.CharField(choices=[('RADIO', 'Radio'), ('ZONAS', 'Zonas')], default='RADIO', help_text='Tipo de zona de actuación: Radio (km) o Zonas (provincias/regiones)', max_length=10)),
                ('radio_km_general', models.IntegerField(blank=True, help_text='Radio de actuación general en kilómetros', null=True)),
                ('zonas_definidas', models.JSONField(blank=True, help_text='Zonas definidas manualmente', null=True)),
                ('foto_de_perfil', models.ImageField(blank=True, help_text='Foto de perfil del transportista', null=True, upload_to='transportistas/perfiles/%Y/%m/%d/')),
                ('trial_end', models.DateTimeField(blank=True, help_text='Fecha de finalización del período de prueba', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Transportista',
                'verbose_name_plural': 'Transportistas',
                'db_table': 'transportistas',
            },
        ),
        migrations.CreateModel(
            name='TransportistaCategoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('radio_km_especifico', models.IntegerField(blank=True, help_text='Radio de actuación específico para esta máquina en kilómetros', null=True)),
                ('nombre_vehiculo', models.CharField(blank=True, help_text='Nombre personalizado del vehículo', max_length=200, null=True)),
                ('marca', models.CharField(blank=True, help_text='Marca del vehículo', max_length=100, null=True)),
                ('tonelaje', models.DecimalField(blank=True, decimal_places=2, help_text='Tonelaje o capacidad de carga', max_digits=10, null=True)),
                ('caracteristicas', models.TextField(blank=True, help_text='Descripción detallada de características especiales', null=True)),
                ('imagen_maquina', models.ImageField(blank=True, help_text='Imagen de la máquina', null=True, upload_to='transportistas/maquinas/%Y/%m/%d/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('categoria', models.ForeignKey(help_text='Categoría del transportista', on_delete=django.db.models.deletion.CASCADE, related_name='transportistacategoria_set', to='db.categoria')),
                ('transportista', models.ForeignKey(help_text='Transportista propietario', on_delete=django.db.models.deletion.CASCADE, related_name='transportistacategoria_set', to='db.transportista')),
            ],
            options={
                'verbose_name': 'Máquina del Transportista',
                'verbose_name_plural': 'Máquinas de los Transportistas',
                'db_table': 'transportista_categoria',
                'unique_together': {('transportista', 'categoria')},
            },
        ),
        migrations.AddField(
            model_name='transportista',
            name='categorias',
            field=models.ManyToManyField(blank=True, help_text='Categorías de transporte', related_name='transportistas', through='db.TransportistaCategoria', to='db.categoria'),
        ),
        migrations.CreateModel(
            name='Valoracion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(choices=[(1, '1 - Muy Malo'), (2, '2 - Malo'), (3, '3 - Regular'), (4, '4 - Bueno'), (5, '5 - Excelente')], help_text='Calificación de 1 a 5 estrellas', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('comment', models.TextField(blank=True, help_text='Comentario opcional', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(help_text='Usuario que envía la valoración', on_delete=django.db.models.deletion.CASCADE, related_name='valoraciones_enviadas', to=settings.AUTH_USER_MODEL)),
                ('rated_user', models.ForeignKey(help_text='Usuario que recibe la valoración', on_delete=django.db.models.deletion.CASCADE, related_name='valoraciones_recibidas', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Valoración',
                'verbose_name_plural': 'Valoraciones',
                'db_table': 'valoraciones',
                'ordering': ['-created_at'],
                'unique_together': {('author', 'rated_user')},
            },
        ),
        migrations.CreateModel(
            name='UserChatSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_favorite', models.BooleanField(default=False, help_text='Indica si el usuario ha marcado esta sala como favorita')),
                ('is_muted', models.BooleanField(default=False, help_text='Indica si el usuario ha silenciado las notificaciones')),
                ('last_read_at', models.DateTimeField(blank=True, help_text='Última vez que el usuario leyó mensajes', null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('chatroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_settings', to='db.chatroom')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chat_settings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Configuración de Chat de Usuario',
                'verbose_name_plural': 'Configuraciones de Chat de Usuarios',
                'db_table': 'user_chat_settings',
                'unique_together': {('user', 'chatroom')},
            },
        ),
        migrations.AddField(
            model_name='chatroom',
            name='participants',
            field=models.ManyToManyField(help_text='Usuarios participantes', related_name='chat_rooms', through='db.UserChatSettings', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(help_text='Contenido del mensaje')),
                ('attachment', models.FileField(blank=True, help_text='Archivo adjunto opcional', null=True, upload_to='chat/attachments/%Y/%m/%d/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(help_text='Usuario que envió el mensaje', on_delete=django.db.models.deletion.CASCADE, related_name='messages', to=settings.AUTH_USER_MODEL)),
                ('chatroom', models.ForeignKey(help_text='Sala de chat', on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='db.chatroom')),
            ],
            options={
                'verbose_name': 'Mensaje',
                'verbose_name_plural': 'Mensajes',
                'db_table': 'messages',
                'ordering': ['created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='transportista',
            index=models.Index(fields=['disponible'], name='transportis_disponi_e8e3c9_idx'),
        ),
        migrations.AddIndex(
            model_name='transportista',
            index=models.Index(fields=['trial_end'], name='transportis_trial_e_a3c8e4_idx'),
        ),
        migrations.AddIndex(
            model_name='transportistacategoria',
            index=models.Index(fields=['transportista', 'categoria'], name='transportis_transpo_4c8e9a_idx'),
        ),
        migrations.AddIndex(
            model_name='valoracion',
            index=models.Index(fields=['rated_user', '-created_at'], name='valoracione_rated_u_f8c9a1_idx'),
        ),
        migrations.AddIndex(
            model_name='userchatsettings',
            index=models.Index(fields=['user', 'is_favorite'], name='user_chat_s_user_id_a8c9e2_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['chatroom', '-created_at'], name='messages_chatroom_c8e9a3_idx'),
        ),
        migrations.AddIndex(
            model_name='message',
            index=models.Index(fields=['author', '-created_at'], name='messages_author__d8c9a4_idx'),
        ),
    ]

