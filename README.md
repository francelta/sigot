# 🏗️ ConnecMaq - Sistema Integral de Gestión de Obras y Transporte

**ConnecMaq** es una plataforma SaaS que funciona como un "Uber para maquinaria pesada y camiones". Conecta empresas **Constructoras** que necesitan servicios con empresas **Proveedoras** que los ofrecen, con énfasis en servicio inmediato (confirmación en menos de 48 horas).

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0+-green.svg)](https://www.djangoproject.com/)
[![Vue.js](https://img.shields.io/badge/Vue.js-3.0+-brightgreen.svg)](https://vuejs.org/)

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Stack Tecnológico](#-stack-tecnológico)
- [Arquitectura del Proyecto](#-arquitectura-del-proyecto)
- [Instalación](#-instalación)
- [Documentación](#-documentación)
- [Estado del Proyecto](#-estado-del-proyecto)
- [Licencia](#-licencia)

---

## ✨ Características

### Para Constructores (Usuarios Gratuitos)
- ✅ Registro y autenticación gratuita
- 🔍 Búsqueda de proveedores por tipo de maquinaria
- ⚡ Filtro de "Disponible en < 48h" para servicio inmediato
- 💬 Chat directo con proveedores
- 📊 Gestión de perfil de empresa

### Para Proveedores (Usuarios de Suscripción)
- ✅ Registro y autenticación con suscripción
- 📋 Listado de flota de maquinaria
- 🖼️ Upload de imágenes de maquinaria
- ⚡ Toggle "Disponible en < 48h" para aparecer en búsquedas prioritarias
- 💬 Recepción y respuesta a consultas
- 📊 Dashboard con estadísticas
- 🏢 Perfil de empresa con logo

### Para Administradores
- 🔐 Panel de administración Django
- 👥 Gestión de usuarios
- 💳 Gestión de suscripciones
- 📊 Estadísticas y reportes

---

## 🛠️ Stack Tecnológico

### Backend
- **Framework:** Django 5.0+
- **API:** Django Rest Framework (DRF)
- **Base de Datos:** PostgreSQL (producción), SQLite (desarrollo)
- **Autenticación:** DRF Simple JWT
- **WebSockets:** Django Channels (para chat en tiempo real)
- **Storage:** Pillow para manejo de imágenes

### Frontend (En desarrollo - no incluido en este repositorio)
- **Framework:** Vue 3 (Composition API)
- **Build Tool:** Vite
- **Estado:** Pinia
- **Router:** Vue Router
- **Estilos:** TailwindCSS
- **HTTP Client:** Axios

---

## 📁 Arquitectura del Proyecto

```
connecmaq/
├── backend/
│   ├── api/                    # App principal
│   │   ├── models.py          # User, Profiles, Machine, Chat
│   │   ├── serializers.py     # Serializers DRF
│   │   ├── views.py           # ViewSets y endpoints
│   │   ├── consumers.py       # WebSocket consumers (chat)
│   │   ├── routing.py         # WebSocket routing
│   │   └── admin.py           # Admin panel config
│   ├── config/                # Configuración Django
│   │   ├── settings.py        # Settings principales
│   │   ├── urls.py            # URL routing
│   │   └── asgi.py            # ASGI config (Channels)
│   ├── manage.py
│   ├── requirements.txt       # Dependencias Python
│   └── env.example            # Variables de entorno ejemplo
├── docs/                      # Documentación completa
└── README.md                  # Este archivo
```

---

## 🚀 Instalación

### Prerrequisitos
- Python 3.10+
- PostgreSQL 13+ (producción) o SQLite (desarrollo)
- pip y virtualenv

### Configuración Backend

1. **Clonar el repositorio:**
```bash
git clone https://github.com/francelta/sigot.git
cd sigot
```

2. **Crear entorno virtual:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno:**
```bash
cp env.example .env
# Editar .env con tus configuraciones
```

5. **Ejecutar migraciones:**
```bash
python manage.py migrate
```

6. **Crear superusuario:**
```bash
python manage.py createsuperuser
```

7. **Ejecutar servidor de desarrollo:**
```bash
python manage.py runserver
# O usar el script: ./run_dev.sh
```

8. **Acceder a:**
- API: http://localhost:8000/api/
- Admin: http://localhost:8000/admin/

---

## 📚 Documentación

Este repositorio incluye documentación completa:

- **[INICIO_COMPLETO.md](INICIO_COMPLETO.md)** - Guía de inicio completa (Backend + Frontend)
- **[BACKEND_COMPLETO.md](BACKEND_COMPLETO.md)** - Documentación técnica del backend
- **[API_ENDPOINTS.md](backend/API_ENDPOINTS.md)** - Endpoints de la API REST
- **[PERFILES_COMPLETO.md](PERFILES_COMPLETO.md)** - Sistema de perfiles
- **[GUIA_PERFILES.md](GUIA_PERFILES.md)** - Guía de usuario para perfiles
- **[RESUMEN_EJECUTIVO.md](RESUMEN_EJECUTIVO.md)** - Resumen ejecutivo del proyecto

### Documentación de Soluciones
- **[SOLUCION_CORS.md](SOLUCION_CORS.md)** - Configuración CORS
- **[SOLUCION_ERRORES.md](SOLUCION_ERRORES.md)** - Errores comunes y soluciones
- **[IMAGENES_OBLIGATORIAS.md](IMAGENES_OBLIGATORIAS.md)** - Sistema de imágenes

---

## 📊 Estado del Proyecto

### ✅ Completado (Backend)

- [x] Modelos de base de datos (User, Profiles, Machine, Chat)
- [x] API REST completa con DRF
- [x] Autenticación JWT
- [x] Sistema de perfiles (Constructor/Proveedor)
- [x] CRUD de maquinaria con imágenes
- [x] Toggle "Disponible en < 48h"
- [x] Búsqueda y filtrado de proveedores
- [x] Estructura de chat con Django Channels
- [x] Panel de administración Django

### 🚧 En Desarrollo

- [ ] Frontend completo (Vue 3)
- [ ] Chat en tiempo real (WebSocket)
- [ ] Sistema de suscripciones (Stripe/MercadoPago)
- [ ] Sistema de notificaciones
- [ ] Sistema de valoraciones
- [ ] Geolocalización avanzada

### 🔮 Futuro

- [ ] App móvil (Capacitor/Tauri)
- [ ] Dashboard de estadísticas avanzado
- [ ] Integración con sistemas de pago
- [ ] Sistema de verificación de proveedores
- [ ] API pública con rate limiting

---

## 🔑 Modelos Principales

### User (AbstractUser personalizado)
```python
- email (unique)
- username
- is_constructor (bool)
- is_provider (bool)
```

### ConstructorProfile
```python
- user (OneToOne)
- company_name
- phone, address
- city, region, country
```

### ProviderProfile
```python
- user (OneToOne)
- company_name
- description
- logo (ImageField)
- phone, website, address
- city, region, country
- available_within_48h (bool) ⚡
- subscription_status
- is_verified
```

### Machine
```python
- provider (ForeignKey)
- name, category
- description
- brand, model, year
- main_image (ImageField - obligatorio)
- additional_images (ManyToMany)
- price_per_hour, price_per_day
- is_available
```

### ChatRoom & Message
```python
- ChatRoom: participants (M2M), created_at
- Message: room, author, content, timestamp, read
```

---

## 🧪 Testing

### Crear datos de prueba
```bash
cd backend
python test_api.py
```

Este script crea:
- Usuarios de prueba (constructor y proveedor)
- Perfiles completos
- Maquinaria de ejemplo
- ChatRoom de prueba

### Credenciales de prueba
- **Constructor:** `constructor@test.com` / `TestPass123!`
- **Proveedor:** `provider@test.com` / `TestPass123!`

---

## 🌐 API Endpoints Principales

### Autenticación
```
POST /api/token/          - Login (obtener JWT)
POST /api/token/refresh/  - Refresh token
POST /api/users/          - Registro
```

### Perfiles
```
GET/POST   /api/constructor-profiles/
GET/PATCH  /api/constructor-profiles/{id}/
GET/POST   /api/providers/
GET/PATCH  /api/providers/{id}/
POST       /api/providers/{id}/toggle_availability/
```

### Maquinaria
```
GET/POST   /api/machines/
GET/PUT/DELETE /api/machines/{id}/
POST       /api/machines/{id}/toggle_availability/
```

### Chat
```
GET/POST   /api/chat-rooms/
GET        /api/chat-rooms/{id}/
POST       /api/chat-rooms/get_or_create_room/
GET/POST   /api/messages/
```

Documentación completa en [API_ENDPOINTS.md](backend/API_ENDPOINTS.md)

---

## 🤝 Contribución

Este proyecto está en desarrollo activo. Las contribuciones son bienvenidas:

1. Fork el proyecto
2. Crea tu feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

---

## 👤 Autor

**Fran Carrasco**
- GitHub: [@francelta](https://github.com/francelta)
- Repositorio: https://github.com/francelta/sigot

---

## 🙏 Agradecimientos

- Django y Django Rest Framework por el excelente framework
- Vue.js por el increíble framework frontend
- La comunidad open source

---

## 📞 Soporte

Para reportar bugs o solicitar nuevas características, por favor abre un [issue](https://github.com/francelta/sigot/issues) en GitHub.

---

**Última actualización:** Noviembre 2025  
**Versión:** 1.0.0 (Backend MVP)  
**Estado:** En desarrollo activo 🚀
