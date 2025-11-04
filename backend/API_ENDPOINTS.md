# 📡 ConnecMaq API Endpoints

Documentación completa de todos los endpoints disponibles en la API de ConnecMaq.

**Base URL**: `http://localhost:8000/api/`

---

## 🔐 Autenticación

### Obtener Token (Login)
```http
POST /api/token/
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Refrescar Token
```http
POST /api/token/refresh/
Content-Type: application/json

{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response:**
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

### Headers para requests autenticados
```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc...
```

---

## 👥 Usuarios

### Registrar Usuario
```http
POST /api/users/
Content-Type: application/json

{
  "email": "nuevo@example.com",
  "username": "nuevo_usuario",
  "password": "SecurePass123!",
  "password2": "SecurePass123!",
  "first_name": "Juan",
  "last_name": "Pérez",
  "user_type": "constructor"  // o "provider"
}
```

### Obtener Perfil del Usuario Actual
```http
GET /api/users/me/
Authorization: Bearer {token}
```

### Actualizar Perfil del Usuario Actual
```http
PATCH /api/users/update_profile/
Authorization: Bearer {token}
Content-Type: application/json

{
  "first_name": "Juan",
  "last_name": "Pérez González"
}
```

### Listar Usuarios (Admin only)
```http
GET /api/users/
Authorization: Bearer {token}
```

### Obtener Detalle de Usuario
```http
GET /api/users/{id}/
Authorization: Bearer {token}
```

---

## 🏗️ Perfiles de Constructores

### Crear Perfil de Constructor
```http
POST /api/constructor-profiles/
Authorization: Bearer {token}
Content-Type: application/json

{
  "company_name": "Constructora Ejemplo S.A.",
  "phone": "+56912345678",
  "address": "Av. Principal 123",
  "city": "Santiago",
  "region": "Metropolitana",
  "country": "Chile"
}
```

### Listar Perfiles de Constructores
```http
GET /api/constructor-profiles/
Authorization: Bearer {token}
```

### Obtener Detalle de Perfil Constructor
```http
GET /api/constructor-profiles/{id}/
Authorization: Bearer {token}
```

### Actualizar Perfil de Constructor
```http
PATCH /api/constructor-profiles/{id}/
Authorization: Bearer {token}
Content-Type: application/json

{
  "phone": "+56987654321",
  "city": "Valparaíso"
}
```

---

## 🚜 Perfiles de Proveedores

### Crear Perfil de Proveedor
```http
POST /api/providers/
Authorization: Bearer {token}
Content-Type: multipart/form-data

company_name: Maquinarias del Sur Ltda.
description: Empresa especializada en maquinaria pesada
phone: +56912345678
website: https://ejemplo.cl
address: Av. Industrial 456
city: Concepción
region: Bio Bio
country: Chile
available_within_48h: true
logo: [archivo]
```

### Listar Proveedores (Público)
```http
GET /api/providers/
```

**Query Parameters:**
- `search` - Búsqueda en nombre, descripción, ciudad
- `ordering` - Ordenar por: `rating`, `-rating`, `created_at`, `-created_at`

### Buscar Proveedores (Endpoint Principal para Constructores) ⭐
```http
GET /api/providers/search/
```

**Query Parameters:**
- `available_within_48h` - `true` o `false` (default: `true`)
- `category` - Categoría de maquinaria: `excavator`, `crane`, `truck`, etc.
- `city` - Ciudad del proveedor
- `region` - Región del proveedor
- `min_rating` - Rating mínimo (0-5)
- `verified_only` - `true` para solo verificados

**Ejemplo:**
```http
GET /api/providers/search/?available_within_48h=true&category=excavator&city=Santiago&min_rating=4.0
```

### Obtener Detalle de Proveedor
```http
GET /api/providers/{id}/
```

### Actualizar Perfil de Proveedor
```http
PATCH /api/providers/{id}/
Authorization: Bearer {token}
Content-Type: application/json

{
  "description": "Nueva descripción de la empresa",
  "phone": "+56987654321"
}
```

### Toggle Disponibilidad 48h ⭐
```http
PATCH /api/providers/{id}/toggle_availability/
Authorization: Bearer {token}
```

**Response:**
```json
{
  "user": {...},
  "company_name": "Maquinarias del Sur Ltda.",
  "available_within_48h": true,
  ...
}
```

---

## 🏗️ Maquinaria

### Crear Maquinaria (Solo Proveedores)
```http
POST /api/machines/
Authorization: Bearer {token}
Content-Type: multipart/form-data

name: Excavadora CAT 320
category: excavator
description: Excavadora hidráulica de alto rendimiento
brand: Caterpillar
model: 320
year: 2020
price_per_hour: 50000
price_per_day: 350000
is_available: true
main_image: [archivo]
```

**Categorías disponibles:**
- `excavator` - Excavadora
- `crane` - Grúa
- `truck` - Camión
- `transport` - Transporte de Áridos
- `loader` - Cargador Frontal
- `bulldozer` - Bulldozer
- `roller` - Rodillo Compactador
- `mixer` - Mixer/Hormigonera
- `pump` - Bomba de Hormigón
- `forklift` - Grúa Horquilla
- `other` - Otro

### Listar Maquinaria
```http
GET /api/machines/
```

**Query Parameters:**
- `provider` - ID del proveedor
- `category` - Categoría de maquinaria
- `available_only` - `true` para solo disponibles
- `search` - Búsqueda en nombre, descripción, marca, modelo

**Ejemplos:**
```http
GET /api/machines/?provider=5
GET /api/machines/?category=excavator&available_only=true
GET /api/machines/?search=CAT
```

### Obtener Detalle de Maquinaria
```http
GET /api/machines/{id}/
```

### Actualizar Maquinaria
```http
PATCH /api/machines/{id}/
Authorization: Bearer {token}
Content-Type: application/json

{
  "price_per_day": 400000,
  "is_available": false
}
```

### Toggle Disponibilidad de Maquinaria
```http
PATCH /api/machines/{id}/toggle_availability/
Authorization: Bearer {token}
```

### Agregar Imágenes a Maquinaria
```http
POST /api/machines/{id}/add_images/
Authorization: Bearer {token}
Content-Type: multipart/form-data

images: [archivo1, archivo2, archivo3]
captions: [Descripción 1, Descripción 2, Descripción 3]
```

### Eliminar Maquinaria
```http
DELETE /api/machines/{id}/
Authorization: Bearer {token}
```

---

## 💬 Chat

### Listar Salas de Chat del Usuario
```http
GET /api/chat-rooms/
Authorization: Bearer {token}
```

**Response:**
```json
{
  "count": 2,
  "results": [
    {
      "id": 1,
      "participants": [...],
      "last_message": {
        "id": 15,
        "content": "Hola, me interesa tu excavadora",
        "author_id": 2,
        "timestamp": "2024-01-15T10:30:00Z",
        "read": false
      },
      "unread_count": 3,
      "created_at": "2024-01-10T08:00:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

### Crear o Buscar Chat con Otro Usuario
```http
POST /api/chat-rooms/find_or_create/
Authorization: Bearer {token}
Content-Type: application/json

{
  "other_user_id": 5
}
```

**Response:** (crea una nueva sala o devuelve la existente)
```json
{
  "id": 1,
  "participants": [...],
  "messages": [...],
  "created_at": "2024-01-10T08:00:00Z"
}
```

### Obtener Detalle de Sala de Chat (con mensajes)
```http
GET /api/chat-rooms/{id}/
Authorization: Bearer {token}
```

### Eliminar Sala de Chat
```http
DELETE /api/chat-rooms/{id}/
Authorization: Bearer {token}
```

---

## 📨 Mensajes

### Listar Mensajes
```http
GET /api/messages/
Authorization: Bearer {token}
```

**Query Parameters:**
- `room` - ID de la sala de chat

**Ejemplo:**
```http
GET /api/messages/?room=1
```

### Enviar Mensaje
```http
POST /api/messages/
Authorization: Bearer {token}
Content-Type: application/json

{
  "room": 1,
  "content": "Hola, me interesa tu excavadora CAT 320"
}
```

### Marcar Mensaje como Leído
```http
POST /api/messages/{id}/mark_read/
Authorization: Bearer {token}
```

### Marcar Todos los Mensajes de una Sala como Leídos
```http
POST /api/messages/mark_room_read/
Authorization: Bearer {token}
Content-Type: application/json

{
  "room_id": 1
}
```

---

## 🔌 WebSocket (Chat en Tiempo Real)

### Conectar al WebSocket de una Sala de Chat

**URL:** `ws://localhost:8000/ws/chat/{room_id}/`

**Nota:** Debes autenticarte con JWT. En el frontend, enviar el token en la query string o headers (depende de la implementación del middleware).

### Enviar Mensaje (WebSocket)
```json
{
  "type": "chat_message",
  "message": "Hola, ¿está disponible la excavadora?"
}
```

### Recibir Mensaje (WebSocket)
```json
{
  "type": "chat_message",
  "message_id": 123,
  "message": "Hola, ¿está disponible la excavadora?",
  "author_id": 5,
  "author_email": "user@example.com",
  "author_name": "Juan Pérez",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Enviar Confirmación de Lectura (WebSocket)
```json
{
  "type": "read_receipt",
  "message_id": 123
}
```

### Recibir Confirmación de Lectura (WebSocket)
```json
{
  "type": "read_receipt",
  "message_id": 123,
  "reader_id": 10
}
```

---

## 📊 Códigos de Estado HTTP

- `200 OK` - Solicitud exitosa
- `201 Created` - Recurso creado exitosamente
- `204 No Content` - Solicitud exitosa sin contenido de respuesta
- `400 Bad Request` - Datos inválidos
- `401 Unauthorized` - No autenticado o token inválido
- `403 Forbidden` - No tiene permisos para esta acción
- `404 Not Found` - Recurso no encontrado
- `500 Internal Server Error` - Error del servidor

---

## 🧪 Ejemplos de Uso con cURL

### Registrarse como Constructor
```bash
curl -X POST http://localhost:8000/api/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "constructor@example.com",
    "username": "constructor1",
    "password": "SecurePass123!",
    "password2": "SecurePass123!",
    "first_name": "Juan",
    "last_name": "Constructor",
    "user_type": "constructor"
  }'
```

### Login
```bash
curl -X POST http://localhost:8000/api/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "constructor@example.com",
    "password": "SecurePass123!"
  }'
```

### Buscar Proveedores Disponibles en 48h
```bash
curl -X GET "http://localhost:8000/api/providers/search/?available_within_48h=true&category=excavator&city=Santiago" \
  -H "Authorization: Bearer {tu_token}"
```

### Crear Perfil de Proveedor
```bash
curl -X POST http://localhost:8000/api/providers/ \
  -H "Authorization: Bearer {tu_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Maquinarias Ejemplo",
    "description": "Empresa de maquinaria pesada",
    "phone": "+56912345678",
    "city": "Santiago",
    "region": "Metropolitana",
    "country": "Chile",
    "available_within_48h": true
  }'
```

### Toggle Disponibilidad 48h
```bash
curl -X PATCH http://localhost:8000/api/providers/5/toggle_availability/ \
  -H "Authorization: Bearer {tu_token}"
```

### Iniciar Chat con un Proveedor
```bash
curl -X POST http://localhost:8000/api/chat-rooms/find_or_create/ \
  -H "Authorization: Bearer {tu_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "other_user_id": 10
  }'
```

---

## 🎯 Flujo Típico de Uso

### Para Constructores:
1. **Registrarse** → `POST /api/users/` (con `user_type: "constructor"`)
2. **Login** → `POST /api/token/`
3. **Crear Perfil** → `POST /api/constructor-profiles/`
4. **Buscar Proveedores** → `GET /api/providers/search/?available_within_48h=true`
5. **Ver Detalle de Proveedor** → `GET /api/providers/{id}/`
6. **Iniciar Chat** → `POST /api/chat-rooms/find_or_create/`
7. **Conectar WebSocket** → `ws://localhost:8000/ws/chat/{room_id}/`

### Para Proveedores:
1. **Registrarse** → `POST /api/users/` (con `user_type: "provider"`)
2. **Login** → `POST /api/token/`
3. **Crear Perfil** → `POST /api/providers/`
4. **Agregar Maquinaria** → `POST /api/machines/`
5. **Toggle Disponibilidad 48h** → `PATCH /api/providers/{id}/toggle_availability/`
6. **Ver Chats** → `GET /api/chat-rooms/`
7. **Responder Mensajes** → WebSocket o `POST /api/messages/`

---

## 📚 Paginación

Todos los listados están paginados (20 items por página por defecto).

**Query Parameters:**
- `page` - Número de página (ej: `?page=2`)
- `page_size` - Tamaño de página (ej: `?page_size=50`)

**Response Format:**
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/providers/?page=2",
  "previous": null,
  "results": [...]
}
```

---

## 🔍 Búsqueda y Filtrado

La mayoría de endpoints soportan:
- `search` - Búsqueda de texto
- `ordering` - Ordenamiento (prefijo `-` para descendente)

**Ejemplos:**
```http
GET /api/machines/?search=excavadora&ordering=-created_at
GET /api/providers/?search=Santiago&ordering=-rating
```

---

**Happy Coding! 🚀**

