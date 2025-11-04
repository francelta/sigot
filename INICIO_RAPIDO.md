# 🚀 ConnecMaq - Inicio Rápido

## ✅ El Backend está 100% listo y funcional

---

## 🎯 Prueba Rápida (5 minutos)

### 1️⃣ Iniciar el Servidor
```bash
cd backend
source venv/bin/activate
python manage.py runserver
```

### 2️⃣ Crear Datos de Prueba
```bash
# En otra terminal
cd backend
source venv/bin/activate
python test_api.py
```

**Resultado esperado:** ✅ Todas las pruebas completadas exitosamente!

### 3️⃣ Acceder al Admin
Abre tu navegador en: **http://localhost:8000/admin/**

**Credenciales de prueba:**
- **Constructor:** `constructor@test.com` / `TestPass123!`
- **Proveedor:** `provider@test.com` / `TestPass123!`

---

## 🧪 Probar la API

### Opción 1: Navegador (GET requests)

**Buscar Proveedores Disponibles en 48h:**
```
http://localhost:8000/api/providers/search/?available_within_48h=true
```

**Listar Maquinaria:**
```
http://localhost:8000/api/machines/
```

### Opción 2: cURL

**1. Login (obtener token):**
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "constructor@test.com",
    "password": "TestPass123!"
  }'
```

Guarda el `access` token que recibes.

**2. Obtener Perfil:**
```bash
curl -X GET http://localhost:8000/api/users/me/ \
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```

**3. Buscar Proveedores:**
```bash
curl -X GET "http://localhost:8000/api/providers/search/?available_within_48h=true&city=Santiago" \
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```

**4. Ver Maquinaria:**
```bash
curl -X GET http://localhost:8000/api/machines/ \
  -H "Authorization: Bearer TU_TOKEN_AQUI"
```

### Opción 3: Postman/Insomnia

Importa la colección desde `backend/API_ENDPOINTS.md`

---

## 📡 Endpoints Más Importantes

### 🔐 Autenticación
```
POST /api/token/                          → Login
POST /api/token/refresh/                  → Refrescar token
POST /api/users/                          → Registro
GET  /api/users/me/                       → Perfil actual
```

### 🔍 Búsqueda (Constructor)
```
GET /api/providers/search/                → Buscar proveedores ⭐
  ?available_within_48h=true
  &category=excavator
  &city=Santiago
  &min_rating=4.0
```

### 🚜 Proveedores
```
GET    /api/providers/                    → Listar
POST   /api/providers/                    → Crear
GET    /api/providers/{id}/               → Detalle
PATCH  /api/providers/{id}/               → Actualizar
PATCH  /api/providers/{id}/toggle_availability/ → Toggle 48h ⭐
```

### 📦 Maquinaria
```
GET    /api/machines/                     → Listar
POST   /api/machines/                     → Crear
GET    /api/machines/{id}/                → Detalle
PATCH  /api/machines/{id}/toggle_availability/ → Toggle disponibilidad
```

### 💬 Chat
```
GET    /api/chat-rooms/                   → Mis chats
POST   /api/chat-rooms/find_or_create/   → Crear/buscar chat ⭐
GET    /api/chat-rooms/{id}/             → Detalle con mensajes
POST   /api/messages/                     → Enviar mensaje
POST   /api/messages/mark_room_read/     → Marcar como leído
```

### 🔌 WebSocket
```
ws://localhost:8000/ws/chat/{room_id}/    → Chat en tiempo real
```

---

## 📚 Documentación Completa

- **[README.md](README.md)** - Visión general del proyecto
- **[API_ENDPOINTS.md](backend/API_ENDPOINTS.md)** - Documentación completa de API
- **[BACKEND_COMPLETO.md](BACKEND_COMPLETO.md)** - Resumen técnico del backend

---

## 🎓 Flujo de Uso Típico

### Para Constructor:

```mermaid
Usuario → Registro → Login → Buscar Proveedores → Ver Detalle → Iniciar Chat
```

**1. Registrarse**
```bash
POST /api/users/
{
  "email": "constructor@example.com",
  "password": "SecurePass123!",
  "password2": "SecurePass123!",
  "user_type": "constructor",
  "first_name": "Juan",
  "last_name": "Pérez"
}
```

**2. Login**
```bash
POST /api/token/
{
  "email": "constructor@example.com",
  "password": "SecurePass123!"
}
```

**3. Crear Perfil**
```bash
POST /api/constructor-profiles/
{
  "company_name": "Constructora Ejemplo",
  "city": "Santiago"
}
```

**4. Buscar Proveedores**
```bash
GET /api/providers/search/?available_within_48h=true&category=excavator
```

**5. Iniciar Chat**
```bash
POST /api/chat-rooms/find_or_create/
{
  "other_user_id": 5
}
```

### Para Proveedor:

```mermaid
Usuario → Registro → Login → Crear Perfil → Agregar Maquinaria → Toggle 48h → Chat
```

**1-2. Registro y Login** (igual que constructor)

**3. Crear Perfil de Proveedor**
```bash
POST /api/providers/
{
  "company_name": "Maquinarias Ejemplo",
  "description": "Empresa de maquinaria pesada",
  "city": "Santiago",
  "available_within_48h": true
}
```

**4. Agregar Maquinaria**
```bash
POST /api/machines/
{
  "name": "Excavadora CAT 320",
  "category": "excavator",
  "brand": "Caterpillar",
  "price_per_day": 350000,
  "is_available": true
}
```

**5. Toggle Disponibilidad 48h**
```bash
PATCH /api/providers/{id}/toggle_availability/
```

---

## 🎨 Frontend (Próximo Paso)

### Crear Proyecto Vue.js

```bash
# En la raíz del proyecto
npm create vite@latest frontend -- --template vue
cd frontend
npm install

# Instalar dependencias necesarias
npm install pinia
npm install axios
npm install vue-router
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init -p

# Configurar TailwindCSS (seguir guía oficial)
```

### Librerías Recomendadas

- **Pinia** - State management
- **Vue Router** - Routing
- **Axios** - HTTP client
- **TailwindCSS** - Styling
- **Headless UI** - Componentes accesibles
- **Socket.io-client** o **native WebSocket** - Para chat en tiempo real

---

## 🔥 Características Destacadas Implementadas

### ⭐ Toggle de Disponibilidad 48h
El "interruptor mágico" que permite a proveedores indicar que pueden atender en menos de 48 horas.

**Endpoint:**
```bash
PATCH /api/providers/{id}/toggle_availability/
```

### 🔍 Búsqueda Avanzada
Sistema de búsqueda con múltiples filtros para constructores.

**Endpoint:**
```bash
GET /api/providers/search/
  ?available_within_48h=true
  &category=excavator
  &city=Santiago
  &region=Metropolitana
  &min_rating=4.0
  &verified_only=true
```

### 💬 Chat en Tiempo Real
Sistema completo de chat con WebSockets y confirmaciones de lectura.

**REST API:**
```bash
POST /api/chat-rooms/find_or_create/
POST /api/messages/
POST /api/messages/mark_room_read/
```

**WebSocket:**
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/chat/1/');
ws.send(JSON.stringify({
  type: 'chat_message',
  message: 'Hola!'
}));
```

---

## 🐛 Troubleshooting

### Servidor no inicia
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Error de módulos
```bash
pip install -r requirements.txt
```

### Error de migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### Puerto 8000 ocupado
```bash
# Usar otro puerto
python manage.py runserver 8001

# O liberar el puerto
lsof -ti:8000 | xargs kill -9
```

---

## 📊 Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────┐
│                     FRONTEND (Vue.js)                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │Dashboard │  │  Search  │  │   Chat   │             │
│  │Constructor│  │ Providers│  │ Real-time│             │
│  └──────────┘  └──────────┘  └──────────┘             │
└──────────────────┬────────────────┬─────────────────────┘
                   │                │
        ┌──────────▼────────┐  ┌───▼──────────┐
        │   REST API        │  │  WebSocket   │
        │   (Django DRF)    │  │  (Channels)  │
        └──────────┬────────┘  └───┬──────────┘
                   │                │
        ┌──────────▼────────────────▼──────────┐
        │          BACKEND (Django)             │
        │  ┌─────────────────────────────────┐ │
        │  │  • Autenticación JWT            │ │
        │  │  • Perfiles (Constructor/Provider)│ │
        │  │  • Maquinaria                    │ │
        │  │  • Chat                          │ │
        │  │  • Búsqueda Avanzada            │ │
        │  └─────────────────────────────────┘ │
        └──────────────────┬────────────────────┘
                           │
        ┌──────────────────▼────────────────────┐
        │   DATABASE (PostgreSQL/SQLite)        │
        │  • Users                               │
        │  • Profiles                            │
        │  • Machines                            │
        │  • ChatRooms & Messages                │
        └────────────────────────────────────────┘
```

---

## ✅ Checklist de Verificación

Verifica que todo funciona:

- [ ] ✅ Servidor Django inicia sin errores
- [ ] ✅ Script de prueba (`test_api.py`) se ejecuta exitosamente
- [ ] ✅ Admin panel accesible en http://localhost:8000/admin/
- [ ] ✅ Puedes hacer login con credenciales de prueba
- [ ] ✅ API responde en http://localhost:8000/api/
- [ ] ✅ Búsqueda de proveedores funciona
- [ ] ✅ Toggle de disponibilidad 48h funciona

Si todos los ítems tienen ✅, ¡estás listo para continuar con el frontend!

---

## 📞 Próximos Pasos

### Inmediatos:
1. ✅ Backend completado
2. ➡️ Crear frontend Vue.js
3. ➡️ Implementar autenticación JWT en frontend
4. ➡️ Crear interfaces de usuario
5. ➡️ Integrar WebSocket para chat

### Futuro:
- Sistema de reviews y ratings
- Integración de pagos
- Notificaciones push
- GeoDjango para búsqueda por distancia
- Apps móviles (iOS/Android)

---

## 🎉 ¡Felicitaciones!

Tienes un backend completamente funcional con:
- ✅ 40+ endpoints REST
- ✅ Autenticación JWT
- ✅ WebSockets para chat en tiempo real
- ✅ Sistema de búsqueda avanzada
- ✅ Gestión de perfiles y maquinaria
- ✅ Documentación completa

**Happy Coding! 🚀**

