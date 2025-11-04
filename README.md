# ConnecMaq 🏗️

**ConnecMaq** es una plataforma SaaS tipo "Uber para maquinaria pesada y camiones" que conecta empresas Constructoras que necesitan servicios con empresas Proveedoras que ofrecen maquinaria y equipos.

## 🎯 Visión del Proyecto

ConnecMaq permite a empresas constructoras encontrar proveedores de maquinaria pesada que puedan confirmar servicios **en menos de 48 horas**, facilitando la conexión directa mediante un sistema de chat en tiempo real.

### Actores Principales

1. **Constructores (Usuarios Gratuitos)**
   - Registro gratuito
   - Búsqueda de maquinaria por tipo y ubicación
   - Filtrado por disponibilidad en <48h
   - Chat directo con proveedores

2. **Proveedores (Usuarios de Suscripción)**
   - Suscripción mensual/anual
   - Perfil de empresa con logo y descripción
   - Catálogo de maquinaria y servicios
   - Toggle de "Disponible en < 48h"
   - Sistema de chat para atender consultas

3. **Administrador**
   - Gestión de suscripciones
   - Moderación de usuarios
   - Estadísticas de la plataforma

## 🛠️ Stack Tecnológico

### Backend
- **Django 5.2.7** - Framework web principal
- **Django REST Framework** - API REST
- **Django Channels** - WebSockets para chat en tiempo real
- **PostgreSQL** - Base de datos (producción)
- **SQLite** - Base de datos (desarrollo)
- **JWT (Simple JWT)** - Autenticación

### Frontend
- **Vue 3** - Framework frontend (Composition API)
- **Vite** - Build tool
- **Pinia** - Gestión de estado
- **TailwindCSS** - UI/Estilos
- **Capacitor/Tauri** - Para apps nativas (futuro)

## 📦 Estructura del Proyecto

```
mak/
├── backend/
│   ├── api/                    # App principal
│   │   ├── models.py          # Modelos de datos
│   │   ├── views.py           # ViewSets de DRF
│   │   ├── serializers.py     # Serializadores
│   │   ├── consumers.py       # WebSocket consumers
│   │   ├── routing.py         # WebSocket routing
│   │   ├── admin.py           # Django Admin
│   │   └── urls.py            # URLs de la API
│   ├── config/                 # Configuración del proyecto
│   │   ├── settings.py        # Settings principales
│   │   ├── urls.py            # URLs principales
│   │   ├── asgi.py            # ASGI + Channels
│   │   └── wsgi.py            # WSGI
│   ├── media/                  # Archivos subidos por usuarios
│   ├── venv/                   # Entorno virtual
│   ├── manage.py              # CLI de Django
│   ├── requirements.txt       # Dependencias Python
│   └── .env.example           # Ejemplo de variables de entorno
├── frontend/                   # Aplicación Vue.js (próximamente)
└── README.md
```

## 🚀 Instalación y Configuración

### Backend (Django)

1. **Clonar el repositorio y navegar al backend:**
```bash
cd backend
```

2. **Crear y activar el entorno virtual:**
```bash
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno:**
```bash
cp .env.example .env
# Editar .env con tus configuraciones
```

5. **Aplicar migraciones:**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Crear superusuario:**
```bash
python manage.py createsuperuser
```

7. **Ejecutar el servidor de desarrollo:**
```bash
python manage.py runserver
```

El backend estará disponible en `http://localhost:8000`

### Frontend (Vue.js)

*Próximamente: instrucciones para configurar el frontend Vue.js*

## 📊 Modelos de Datos

### User (Custom)
- Usuario personalizado que hereda de `AbstractUser`
- `email` como identificador principal
- Flags: `is_constructor`, `is_provider`

### ConstructorProfile
- Perfil de empresas constructoras
- Información de la empresa y ubicación

### ProviderProfile
- Perfil de empresas proveedoras
- **`available_within_48h`** - Toggle principal para filtrado
- Estado de suscripción
- Rating y verificación

### Machine
- Maquinaria ofrecida por proveedores
- Categorías: excavadoras, grúas, camiones, etc.
- Precios, especificaciones, disponibilidad

### ChatRoom & Message
- Sistema de chat en tiempo real
- Mensajes entre constructores y proveedores
- Indicadores de "leído"

## 🔐 Autenticación

El sistema usa **JWT (JSON Web Tokens)** para autenticación:

- `POST /api/token/` - Obtener access token
- `POST /api/token/refresh/` - Refrescar token
- Access token: 1 hora
- Refresh token: 7 días

## 📡 WebSockets (Chat)

El chat en tiempo real funciona mediante Django Channels:

```
ws://localhost:8000/ws/chat/<room_id>/
```

Tipos de mensajes:
- `chat_message` - Enviar/recibir mensajes
- `read_receipt` - Marcar mensajes como leídos

## 🎨 Admin Panel

Django Admin está disponible en `/admin/` con interfaces personalizadas para:

- Gestión de usuarios (Constructores y Proveedores)
- Perfiles de empresas
- Catálogo de maquinaria
- Salas de chat y mensajes
- Estados de suscripción

## 🧪 Testing

```bash
# Ejecutar tests
pytest

# Con coverage
pytest --cov=api
```

## 📝 Variables de Entorno

Principales variables en `.env`:

```env
SECRET_KEY=tu-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (PostgreSQL para producción)
USE_POSTGRES=False
DB_NAME=connecmaq_db
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
```

## 🌐 API Endpoints

✅ **[Ver Documentación Completa de API](backend/API_ENDPOINTS.md)**

### Endpoints Principales:

**Autenticación:**
- `POST /api/token/` - Login (obtener JWT token)
- `POST /api/token/refresh/` - Refrescar token

**Usuarios:**
- `POST /api/users/` - Registro de usuarios
- `GET /api/users/me/` - Perfil del usuario actual

**Proveedores:**
- `GET /api/providers/` - Listar proveedores
- `GET /api/providers/search/` - **Búsqueda avanzada con filtros** ⭐
- `PATCH /api/providers/{id}/toggle_availability/` - Toggle disponibilidad 48h

**Maquinaria:**
- `GET /api/machines/` - Listar maquinaria
- `POST /api/machines/` - Crear maquinaria (proveedores)
- `GET /api/machines/{id}/` - Detalle de maquinaria

**Chat:**
- `GET /api/chat-rooms/` - Listar chats del usuario
- `POST /api/chat-rooms/find_or_create/` - Crear o encontrar chat
- `POST /api/messages/` - Enviar mensaje
- `ws://localhost:8000/ws/chat/{room_id}/` - WebSocket en tiempo real

## 🚧 Roadmap

- [x] Setup inicial del proyecto Django
- [x] Modelos de datos completos
- [x] Sistema de autenticación JWT
- [x] Chat en tiempo real con Channels
- [x] Serializers y ViewSets de DRF ✨ **NUEVO**
- [x] API REST completa y funcional ✨ **NUEVO**
- [x] Sistema de búsqueda avanzado ✨ **NUEVO**
- [x] Documentación completa de API ✨ **NUEVO**
- [ ] Frontend Vue.js
- [ ] Integración de pagos (Stripe/MercadoPago)
- [ ] Sistema de reviews y ratings (preparado en modelos)
- [ ] Notificaciones push
- [ ] Apps móviles (iOS/Android)

## 👥 Contribución

Este es un proyecto en desarrollo activo. Para contribuir:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es privado y está en desarrollo.

## 📧 Contacto

Para más información sobre el proyecto, contactar al equipo de desarrollo.

---

**Construido con ❤️ para conectar la industria de la construcción**

