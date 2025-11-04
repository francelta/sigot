# 🚀 ConnecMaq - Quick Start Guide

## ⚡ Inicio Rápido (3 comandos)

```bash
# 1. Ir al backend
cd backend

# 2. Ejecutar el servidor
./run_dev.sh

# 3. En otra terminal, crear tu usuario admin
python manage.py createsuperuser
```

**Ya está! 🎉** Accede a:
- API: http://localhost:8000
- Admin: http://localhost:8000/admin

---

## 📦 Lo que tienes instalado:

### ✅ Backend Completo
- ✅ Django 5.0 + Django REST Framework
- ✅ JWT Authentication (Simple JWT)
- ✅ WebSockets (Django Channels)
- ✅ CORS configurado
- ✅ 7 modelos de base de datos
- ✅ Admin panel personalizado

### 📊 Modelos Listos para Usar

```python
# Usuarios
User (custom)           # Email como login, flags is_constructor/is_provider
ConstructorProfile      # Perfil de Constructores
ProviderProfile         # Perfil de Proveedores (con toggle de 48h)

# Maquinaria
Machine                 # Catálogo de maquinaria
MachineImage           # Galería de fotos

# Chat
ChatRoom               # Salas de conversación
Message                # Mensajes (con "leído")
```

---

## 🎯 Tu Primer Endpoint

### 1. Obtener Token JWT

```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "tu@email.com",
    "password": "tupassword"
  }'
```

Respuesta:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLC...",
  "refresh": "eyJ0eXAiOiJKV1QiLC..."
}
```

### 2. Usar el Token

```bash
curl http://localhost:8000/api/providers/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## 🔥 Características Destacadas

### 1. Toggle de "Disponible en < 48h" ⏰

El modelo `ProviderProfile` tiene un campo especial:

```python
available_within_48h = models.BooleanField(default=False)
```

Este es el **filtro principal** que usarán los Constructores para encontrar proveedores.

### 2. Chat en Tiempo Real 💬

WebSocket conectado a:
```
ws://localhost:8000/ws/chat/<room_id>/
```

Enviar mensaje:
```javascript
{
  "type": "chat_message",
  "message": "Hola, necesito una excavadora"
}
```

### 3. Múltiples Categorías de Maquinaria 🚜

11 categorías predefinidas:
- Excavadora
- Grúa
- Camión
- Transporte de Áridos
- Cargador Frontal
- Bulldozer
- Rodillo Compactador
- Mixer/Hormigonera
- Bomba de Hormigón
- Grúa Horquilla
- Otro

---

## 📁 Archivos Importantes

### Configuración
- `backend/config/settings.py` - Todas las configuraciones
- `backend/.env.example` - Variables de entorno

### Modelos y Lógica
- `backend/api/models.py` - 7 modelos de datos
- `backend/api/admin.py` - Interfaces de admin
- `backend/api/consumers.py` - WebSocket para chat

### URLs
- `backend/config/urls.py` - URLs principales
- `backend/api/urls.py` - URLs de la API

---

## 🧪 Testing

### Verificar que todo funcione:
```bash
cd backend
source venv/bin/activate
python manage.py check
```

### Crear datos de prueba desde el Admin:
1. Ve a http://localhost:8000/admin
2. Crea un Usuario
3. Marca `is_provider = True`
4. Crea un ProviderProfile para ese usuario
5. Añade maquinaria a ese proveedor
6. Activa el toggle `available_within_48h`

---

## 💡 Comandos Útiles

```bash
# Activar entorno virtual
cd backend
source venv/bin/activate

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Shell interactivo
python manage.py shell

# Ver todas las URLs
python manage.py show_urls  # (requiere django-extensions)

# Resetear DB (¡CUIDADO!)
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

---

## 🎨 Próximas Tareas

### Backend - API REST (Siguiente Paso)

1. **Crear `api/serializers.py`**
   ```python
   from rest_framework import serializers
   from .models import User, ProviderProfile, Machine
   
   class ProviderSerializer(serializers.ModelSerializer):
       class Meta:
           model = ProviderProfile
           fields = '__all__'
   ```

2. **Crear `api/views.py`**
   ```python
   from rest_framework import viewsets
   from .models import ProviderProfile
   from .serializers import ProviderSerializer
   
   class ProviderViewSet(viewsets.ModelViewSet):
       queryset = ProviderProfile.objects.all()
       serializer_class = ProviderSerializer
   ```

3. **Registrar en `api/urls.py`**
   ```python
   from rest_framework.routers import DefaultRouter
   from .views import ProviderViewSet
   
   router = DefaultRouter()
   router.register('providers', ProviderViewSet)
   ```

### Frontend - Vue.js

1. Setup inicial con Vite
2. Instalar TailwindCSS
3. Configurar Pinia (state management)
4. Crear componentes de autenticación
5. Conectar con la API

---

## 🐛 Troubleshooting

### Error: "No module named 'api'"
```bash
cd backend
source venv/bin/activate
```

### Error: "Port 8000 already in use"
```bash
# Opción 1: Usar otro puerto
python manage.py runserver 8001

# Opción 2: Matar el proceso
lsof -ti:8000 | xargs kill -9
```

### Error: "CORS policy"
Verifica que el frontend esté en las URLs permitidas en `settings.py`:
```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",  # Vite
]
```

---

## 📞 ¿Necesitas Ayuda?

1. **Revisa** `README.md` - Documentación completa
2. **Revisa** `SETUP_COMPLETED.md` - Detalles del setup
3. **Código** - Todo está documentado en español
4. **Django Admin** - Explora los modelos visualmente

---

## 🎓 Recursos de Aprendizaje

- [Django Tutorial](https://docs.djangoproject.com/en/5.0/intro/tutorial01/)
- [DRF Tutorial](https://www.django-rest-framework.org/tutorial/quickstart/)
- [Channels Tutorial](https://channels.readthedocs.io/en/stable/tutorial/)
- [Vue 3 Docs](https://vuejs.org/)

---

**¡Éxito con tu proyecto! 🚀**

*ConnecMaq - Conectando la industria de la construcción*

