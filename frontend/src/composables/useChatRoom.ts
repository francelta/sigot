import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { useChatStore } from '../stores/chatStore'
import { getMessages } from '../api/chat'

/**
 * Composable for managing chat room logic
 * Handles WebSocket connection, message loading, and sending
 */
export function useChatRoom() {
  const route = useRoute()
  const chatStore = useChatStore()

  // Error state for connection issues
  const connectionError = ref<string | null>(null)
  const isConnecting = ref(false)

  /**
   * Get room ID from route params
   */
  const roomId = computed(() => {
    const id = route.params.id
    return typeof id === 'string' ? parseInt(id, 10) : Number(id)
  })

  /**
   * Connect to chat room on mount
   */
  onMounted(async () => {
    if (!roomId.value || isNaN(roomId.value)) {
      const errorMsg =
        'ID de sala inválido. Por favor, vuelve a la lista de chats.'
      connectionError.value = errorMsg
      console.error('Invalid room ID:', roomId.value)
      return
    }

    isConnecting.value = true
    connectionError.value = null

    try {
      // IMPORTANT: Disconnect from any previous room first
      console.log('[useChatRoom] Disconnecting from previous room before loading new one')
      chatStore.disconnect()

      // Clear messages for previous room to avoid mixing
      // (messages will be loaded fresh for the new room)

      // Load existing messages first
      console.log('[useChatRoom] Fetching messages for room:', roomId.value)
      const messagesResponse = await getMessages(roomId.value, { limit: 50 })
      console.log('[useChatRoom] Raw response:', messagesResponse)
      console.log('[useChatRoom] Raw messages from API:', JSON.stringify(messagesResponse.results, null, 2))

      // Process messages - ensure author field is properly structured
      const processedMessages = messagesResponse.results.map((msg: any) => {
        console.log('[useChatRoom] Processing message:', msg)
        const rawAuthor = msg.author ?? null
        const fallbackAuthorId =
          msg.author_id ?? msg.authorId ?? msg.authorID ?? null

        if (!rawAuthor && fallbackAuthorId == null) {
          console.warn('[useChatRoom] Message without author info:', msg)
        }

        const authorId = Number(
          (rawAuthor && rawAuthor.id) ?? fallbackAuthorId ?? 0
        )

        const author = {
          id: authorId,
          username: rawAuthor?.username || `Usuario ${authorId || 'desconocido'}`,
          email: rawAuthor?.email || '',
          is_transportista: rawAuthor?.is_transportista || false,
        }

        console.log('[useChatRoom] Resolved author:', author)

        return {
          ...msg,
          author,
        }
      })

      console.log('[useChatRoom] Processed messages:', processedMessages.length, 'messages')

      // Store messages for this room using Vue reactivity
      // CRITICAL: Must trigger reactivity properly
      chatStore.setMessagesForRoom(roomId.value, processedMessages)

      console.log('[useChatRoom] Messages stored for room', roomId.value, ':', chatStore.getMessages(roomId.value).length)

      // Connect to WebSocket
      await chatStore.connectToRoom(roomId.value)
      connectionError.value = null
    } catch (error) {
      const errorMsg =
        error instanceof Error
          ? error.message
          : 'No se pudo conectar a la sala de chat. Por favor, intenta nuevamente.'
      connectionError.value = errorMsg
      console.error('Error connecting to chat room:', error)
    } finally {
      isConnecting.value = false
    }
  })

  /**
   * Disconnect from chat room on unmount
   */
  onUnmounted(() => {
    chatStore.disconnect()
  })

  /**
   * Send a message
   */
  async function sendMessage(text: string): Promise<void> {
    if (!text.trim()) {
      throw new Error('El mensaje no puede estar vacío')
    }

    if (
      !chatStore.websocket ||
      chatStore.websocket.readyState !== WebSocket.OPEN
    ) {
      throw new Error('No hay conexión con el servidor. Intenta nuevamente.')
    }

    try {
      chatStore.sendMessage(text.trim())
    } catch (error) {
      console.error('Error sending message:', error)
      throw error
    }
  }

  return {
    roomId,
    sendMessage,
    connectionError,
    isConnecting,
  }
}
