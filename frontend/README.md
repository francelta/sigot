# SIGOT Frontend

PWA construida con Vue 3 + TypeScript + Vite para el Sistema de Gestión de Operadores de Transporte.

## Stack Tecnológico

- **Vue 3** (Composition API con `<script setup>`)
- **TypeScript**
- **Vite** (Build tool)
- **Pinia** (Gestión de estado)
- **Vue Router** (Rutas)
- **Axios** (Cliente HTTP)
- **Tailwind CSS** (Estilos)
- **Leaflet** (Mapas - gratuito, sin API key)

## Estructura del Proyecto

```
frontend/
├── src/
│   ├── api/           # Cliente API y servicios
│   ├── components/    # Componentes Vue
│   │   └── base/      # Componentes base (BaseButton, BaseInput)
│   ├── stores/        # Tiendas Pinia
│   ├── views/         # Vistas/páginas
│   ├── router/        # Configuración de rutas
│   ├── App.vue        # Componente raíz
│   └── main.ts        # Punto de entrada
├── index.html
└── package.json
```

## Instalación

```bash
npm install
```

## Desarrollo

```bash
npm run dev
```

La aplicación estará disponible en `http://localhost:3000`

## Build

```bash
npm run build
```

## Características Implementadas

### ✅ Tarea 1: Configuración del Proyecto
- Proyecto Vite con Vue 3 + TypeScript
- Pinia, Vue Router, Axios, Tailwind CSS configurados
- Kit de UI Base: `BaseButton.vue`, `BaseInput.vue`, `BaseCard.vue`

### ✅ Tarea 2: Flujo de Autenticación
- Tienda de autenticación (`authStore.ts`)
- Vistas de Login y Registro con estética Uber
- Integración con API (`/api/auth/login/` y `/api/auth/register/`)
- Almacenamiento seguro de JWT en localStorage
- Interceptores de Axios para añadir token automáticamente
- Guards de ruta en Vue Router

### ✅ Tarea 3: Vista de Mapa
- Mapa con **Leaflet + OpenStreetMap** (gratuito, sin API key)
- Composable `useMap.ts` con toda la lógica del mapa
- Componentes: `MapFilterBar.vue`, `TransporterInfoCard.vue`
- Geolocalización del usuario
- Marcadores interactivos para transportistas
- Filtrado por categorías

### ✅ Tarea 4: Interfaz de Chat
- Layout principal con navegación inferior (`AppLayout.vue`, `AppBottomNav.vue`)
- Lista de conversaciones estilo WhatsApp (`ChatListView.vue`)
- Sala de chat en tiempo real (`ChatRoomView.vue`)
- Componentes: `ChatMessageBubble.vue`, `ChatInputBar.vue`
- WebSocket para mensajes en tiempo real (`useChatRoom.ts`)
- Tienda de chat (`chatStore.ts`)

## Notas Importantes

- **Mapa**: Usa Leaflet con OpenStreetMap (completamente gratuito, sin configuración necesaria)
- **WebSocket**: Configurado para `ws://localhost:8000` por defecto
- Ver `MAP_SETUP.md` para más información sobre el mapa

