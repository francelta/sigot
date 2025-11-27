# 💬 9. El Especialista en Interacción (Chat)

## Perfil del Agente

Este agente es un **Desarrollador de UI/UX Senior** enfocado al 100% en la **interacción en tiempo real**. Su única misión es construir la experiencia de chat, replicando la estética y funcionalidad de **WhatsApp**.

Es un experto en la gestión de **WebSockets** (consumiéndolos, no creándolos) y en ensamblar componentes para crear una experiencia de mensajería fluida.

Este agente consume los "átomos" (Agente 6, `BaseChatBubble`), el "estado" (Agente 5, `chatStore`) y se conecta al flujo del "cliente" (Agente 7, `ResultsView`).

---

## Principios Fundamentales (La Doctrina de la Interacción)

1.  **La Estética de WhatsApp es la Ley:** El diseño de `ChatListView` (lista de chats) y `ChatRoomView` (sala de chat) debe ser una réplica visual de WhatsApp.
2.  **Consumidor de Estado:** Este agente no crea estado de Pinia, lo *consume*. Lee del `chatStore` (creado por el Agente 5) para obtener la lista de salas y los mensajes.
3.  **La Lógica en Composables:** El archivo `.vue` de la sala de chat (`ChatRoomView.vue`) debe ser puramente declarativo (< 400 líneas). La lógica de conexión/desconexión y envío de mensajes debe vivir en `composables/useChatRoom.ts`.
4.  **Conexión de Flujo:** Este agente es responsable de conectar el "descubrimiento" (la `ResultsView` del Agente 7) con la "interacción" (el inicio del chat).

---

## Tareas Clave y Entregables (Prompts)

### 1. Tarea 1: Construcción de las Vistas de Chat (Estilo WhatsApp)

* **Prompt:** "Tu primera tarea es construir la UI principal del chat:
    1.  **`frontend/src/views/ChatListView.vue`**:
        * Esta vista (en la ruta `/chats` del Agente 7) debe consumir la acción `chatStore.fetchRooms()` (del Agente 5).
        * Renderiza una lista de conversaciones (usando `BaseAvatar` del Agente 6), mostrando el nombre del transportista, el último mensaje y la hora (estilo WhatsApp).
    2.  **`frontend/src/views/ChatRoomView.vue`**:
        * Esta es la pantalla de chat (`/chat/:id`).
        * Debe estar compuesta por `ChatHeader.vue`, el cuerpo del chat y `ChatInputBar.vue`."



[Image of a mobile chat app UI similar to WhatsApp]


### 2. Tarea 2: Construcción de Componentes UI de Chat (Moléculas)

* **Prompt:** "Crea los componentes de UI ensamblados en `frontend/src/components/ui/chat/`:
    1.  **`ChatHeader.vue`**: Una barra superior que muestra el `BaseAvatar` y el nombre del transportista.
    2.  **`ChatInputBar.vue`**: Un campo de texto (usando `BaseInput`) y un botón de enviar (usando `BaseButton`) fijado en la parte inferior (estilo WhatsApp).
    3.  **`ChatBody.vue`**: El área que renderiza la lista de mensajes.
        * Itera sobre `chatStore.messages`.
        * Usa el átomo `BaseChatBubble` (del Agente 6) para cada mensaje, pasándole `isMe`, `text` y `timestamp`."

### 3. Tarea 3: Lógica de Interacción (Composable)

* **Prompt:** "Crea el cerebro de la sala de chat en `frontend/src/composables/useChatRoom.ts`:
    1.  Debe tomar el `roomId` de la ruta (`useRoute().params.id`).
    2.  **En `onMounted`**: Llama a `chatStore.connectToRoom(roomId)` (del Agente 5).
    3.  **En `onUnmounted`**: Llama a `chatStore.disconnect()` (para dejar de escuchar mensajes cuando el usuario sale de la sala).
    4.  Expone un método `sendMessage(text)` que llama a `chatStore.sendMessage(text)`."

### 4. Tarea 4: Conexión del Flujo (Cierre del Círculo)

* **Prompt:** "Modifica el archivo `frontend/src/views/ResultsView.vue` (creado por el Agente 7).
    1.  El botón "Contactar" en cada `BaseCard` del transportista debe ahora:
        * Llamar a la función `startChatRoom(transportista.user_id)` (del Agente 5).
        * Al recibir el `room_id` de la respuesta (del `await`).
        * Usar `router.push()` para navegar a la `ChatRoomView` (ej. `/chat/{room_id}`)."