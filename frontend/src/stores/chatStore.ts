import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { ChatRoom, Message } from '../api/chat'
import { getChatRooms, startChatRoom } from '../api/chat'
import client from '../api/client'
import { useAuthStore } from './authStore'

/**
 * Chat store (Pinia)
 * Manages chat rooms, messages, and WebSocket connections
 */
export const useChatStore = defineStore('chat', () => {
  // State
  const rooms = ref<ChatRoom[]>([])
  const activeRoomId = ref<number | null>(null)
  const messagesByRoom = ref<Record<number, Message[]>>({})  // FIXED: Separate messages per room
  const websocket = ref<WebSocket | null>(null)

  // Reconnection state
  const isIntentionallyDisconnected = ref(false)
  const reconnectAttempts = ref(0)
  const maxReconnectAttempts = 5
  const reconnectTimeoutId = ref<number | null>(null)

  // Actions
  /**
   * Fetch all chat rooms for the authenticated user
   */
  async function fetchRooms(): Promise<void> {
    try {
      const fetchedRooms = await getChatRooms()
      rooms.value = fetchedRooms
    } catch (error) {
      console.error('Error fetching chat rooms:', error)
      throw error
    }
  }

  /**
   * Calculate exponential backoff delay in milliseconds
   * @param attempt - Current reconnect attempt number (0-indexed)
   * @returns Delay in milliseconds
   */
  function getReconnectDelay(attempt: number): number {
    // Exponential backoff: 1s, 2s, 4s, 8s, 16s (max 30s)
    const baseDelay = 1000 // 1 second
    const maxDelay = 30000 // 30 seconds
    const delay = Math.min(baseDelay * Math.pow(2, attempt), maxDelay)
    return delay
  }

  /**
   * Attempt to reconnect to the chat room with exponential backoff
   * @param roomId - ID of the chat room to reconnect to
   */
  function attemptReconnect(roomId: number): void {
    if (isIntentionallyDisconnected.value) {
      // Don't reconnect if user intentionally disconnected
      return
    }

    if (reconnectAttempts.value >= maxReconnectAttempts) {
      console.error(
        `Max reconnect attempts (${maxReconnectAttempts}) reached for room ${roomId}`
      )
      return
    }

    // Increment attempt counter before calculating delay
    reconnectAttempts.value++
    const delay = getReconnectDelay(reconnectAttempts.value - 1) // -1 because we already incremented
    console.log(
      `Attempting to reconnect to room ${roomId} in ${delay}ms (attempt ${reconnectAttempts.value
      }/${maxReconnectAttempts})`
    )

    reconnectTimeoutId.value = window.setTimeout(async () => {
      try {
        await connectToRoom(roomId, false) // false = not initial connection
        // Reset attempts on successful connection (handled in onopen)
      } catch (error) {
        console.error('Reconnection attempt failed:', error)
        // Will trigger another reconnect attempt via onclose handler
        // Note: reconnectAttempts is not reset here, so next attempt will use higher delay
      }
    }, delay)
  }

  /**
   * Connect to a chat room via WebSocket
   * Closes any existing WebSocket connection and creates a new one
   * @param roomId - ID of the chat room to connect to
   * @param isInitialConnection - Whether this is the initial connection (true) or a reconnection (false)
   */
  async function connectToRoom(
    roomId: number,
    isInitialConnection: boolean = true
  ): Promise<void> {
    // Close existing WebSocket connection if any
    if (websocket.value) {
      websocket.value.close()
      websocket.value = null
    }

    // Clear any pending reconnection attempts
    if (reconnectTimeoutId.value !== null) {
      clearTimeout(reconnectTimeoutId.value)
      reconnectTimeoutId.value = null
    }

    // Reset reconnect attempts on initial connection
    if (isInitialConnection) {
      reconnectAttempts.value = 0
      isIntentionallyDisconnected.value = false
    }

    // Get JWT token from authStore
    const authStore = useAuthStore()
    const token = authStore.token

    if (!token) {
      throw new Error('User must be authenticated to connect to chat room')
    }

    // Determine WebSocket URL based on environment
    // Use the same host/port as the API (which uses a proxy in dev)
    const wsProtocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const wsHost = window.location.hostname

    // In development, the frontend proxy forwards to backend, so use same port as frontend
    // In production, use the same port as the API
    const wsPort = import.meta.env.DEV ? window.location.port || '3000' : window.location.port || ''
    const wsBaseUrl = `${wsProtocol}//${wsHost}${wsPort ? `:${wsPort}` : ''}`

    // Create WebSocket connection
    const wsUrl = `${wsBaseUrl}/ws/chat/${roomId}/?token=${token}`
    const ws = new WebSocket(wsUrl)

    // Set up WebSocket event handlers
    ws.onopen = () => {
      console.log(`Connected to chat room ${roomId}`)
      activeRoomId.value = roomId
      websocket.value = ws
      // Reset reconnect attempts on successful connection
      reconnectAttempts.value = 0
    }

    ws.onmessage = (event: MessageEvent) => {
      try {
        const data = JSON.parse(event.data)
        console.log('[chatStore] WebSocket message received:', data)

        // Skip if it's a type message (from channel layer)
        if (data.type === 'chat.message') {
          console.log('[chatStore] Processing chat.message:', data)
          console.log('[chatStore] Author from WebSocket:', data.author)

          const rawAuthor = data.author ?? null
          const fallbackAuthorId =
            data.author_id ?? data.authorId ?? data.authorID ?? null
          const authorId = Number(
            (rawAuthor && rawAuthor.id) ?? fallbackAuthorId ?? 0
          )

          // Transform the message to match the Message interface
          const message: Message = {
            id: data.id,
            chatroom_id: data.chatroom_id || activeRoomId.value,
            author: {
              id: authorId,
              username:
                rawAuthor?.username || `Usuario ${authorId || 'desconocido'}`,
              email: rawAuthor?.email || '',
              is_transportista: rawAuthor?.is_transportista || false,
              phone: null,
              created_at: new Date().toISOString(),
            },
            body: data.body || data.message || '',
            attachment: data.attachment || null,
            created_at: data.created_at || new Date().toISOString(),
          }

          console.log('[chatStore] Processed message:', message)
          console.log('[chatStore] Message author ID:', message.author.id)

          // Add new message to the room's message array
          const roomId = message.chatroom_id
          console.log('[chatStore WebSocket] Received message for room:', roomId, 'Current activeRoomId:', activeRoomId.value)

          if (!messagesByRoom.value[roomId]) {
            console.log('[chatStore WebSocket] Creating new message array for room:', roomId)
            messagesByRoom.value[roomId] = []
          }

          console.log('[chatStore WebSocket] Before adding - Room', roomId, 'has', messagesByRoom.value[roomId].length, 'messages')
          messagesByRoom.value[roomId].push(message)
          console.log('[chatStore WebSocket] After adding - Room', roomId, 'has', messagesByRoom.value[roomId].length, 'messages')

          // Update the room's last_message in the rooms list
          const roomIndex = rooms.value.findIndex(r => r.id === message.chatroom_id)
          if (roomIndex !== -1) {
            const room = rooms.value[roomIndex]
            const currentUserId = useAuthStore().user?.id

            // Update last message
            room.last_message = message

            // Increment unread count if message is not from current user and room is not active
            if (message.author.id !== currentUserId && activeRoomId.value !== message.chatroom_id) {
              console.log('[chatStore] Incrementing unread count for room', message.chatroom_id)
              const currentCount = room.unread_count || 0
              room.unread_count = currentCount + 1
            }

            // Move room to top (most recent first)
            rooms.value.splice(roomIndex, 1)
            rooms.value.unshift(room)
          } else {
            // Room not in list, might need to refresh rooms
            // This shouldn't happen, but just in case
            console.warn(`Received message for room ${message.chatroom_id} which is not in rooms list`)
          }
          console.log('[chatStore] Updated last_message for room', message.chatroom_id)
        } else if (data.type === 'chat.mark_read') {
          // Handle mark_read events - update participant's last_read_at
          console.log('[chatStore] Received mark_read event:', data)

          const roomId = data.room_id
          const userId = data.user_id
          const markedAt = data.marked_at

          // Find the room and update the participant's last_read_at
          const roomIndex = rooms.value.findIndex(r => r.id === roomId)
          if (roomIndex !== -1) {
            const room = rooms.value[roomIndex]
            const participantIndex = room.participants.findIndex(p => p.id === userId)

            if (participantIndex !== -1) {
              room.participants[participantIndex].last_read_at = markedAt
              console.log('[chatStore] Updated last_read_at for user', userId, 'in room', roomId)
            }
          }
        }
      } catch (error) {
        console.error('Error parsing WebSocket message:', error)
      }
    }

    ws.onerror = (error: Event) => {
      console.error('WebSocket error:', error)
    }

    ws.onclose = (event: CloseEvent) => {
      console.log(
        `Disconnected from chat room ${roomId} (code: ${event.code}, reason: ${event.reason})`
      )

      // Only attempt reconnection if:
      // 1. This was the active room
      // 2. Disconnection was not intentional
      // 3. We haven't exceeded max reconnect attempts
      if (
        activeRoomId.value === roomId &&
        !isIntentionallyDisconnected.value &&
        reconnectAttempts.value < maxReconnectAttempts
      ) {
        // Check if close was abnormal (code 1006) or server error (code 1011)
        const isAbnormalClose =
          event.code === 1006 || event.code === 1011 || !event.wasClean

        if (isAbnormalClose) {
          // Attempt automatic reconnection with exponential backoff
          attemptReconnect(roomId)
        } else {
          // Clean close - don't reconnect
          console.log('Clean close detected, not reconnecting')
        }
      }

      // Clear websocket reference if this was the active room
      if (activeRoomId.value === roomId) {
        // Only clear if intentionally disconnected or max attempts reached
        if (
          isIntentionallyDisconnected.value ||
          reconnectAttempts.value >= maxReconnectAttempts
        ) {
          activeRoomId.value = null
          websocket.value = null
        }
      }
    }

    websocket.value = ws
  }

  /**
   * Send a message through the WebSocket connection
   * @param text - Message text to send
   */
  function sendMessage(text: string): void {
    if (!websocket.value || websocket.value.readyState !== WebSocket.OPEN) {
      throw new Error('WebSocket is not connected')
    }

    if (!activeRoomId.value) {
      throw new Error('No active chat room')
    }

    const message = {
      message: text,
    }

    websocket.value.send(JSON.stringify(message))
  }

  /**
   * Disconnect from the current chat room
   * Marks the disconnection as intentional to prevent automatic reconnection
   */
  function disconnect(): void {
    // Mark as intentionally disconnected to prevent reconnection
    isIntentionallyDisconnected.value = true

    // Clear any pending reconnection attempts
    if (reconnectTimeoutId.value !== null) {
      clearTimeout(reconnectTimeoutId.value)
      reconnectTimeoutId.value = null
    }

    // Reset reconnect attempts
    reconnectAttempts.value = 0

    if (websocket.value) {
      websocket.value.close()
      websocket.value = null
    }
    activeRoomId.value = null
    // Clear all messages (or keep them cached?)
    messagesByRoom.value = {}
  }

  /**
   * Create or get a chat room with a participant
   * @param participantId - ID of the other participant
   * @returns Created or existing chat room
   */
  async function createOrGetRoom(participantId: number): Promise<ChatRoom> {
    try {
      const room = await startChatRoom(participantId)

      // Update rooms list if room is new
      const existingRoom = rooms.value.find(r => r.id === room.id)
      if (!existingRoom) {
        rooms.value.push(room)
      } else {
        // Update existing room
        const index = rooms.value.findIndex(r => r.id === room.id)
        rooms.value[index] = room
      }

      return room
    } catch (error) {
      console.error('Error creating/getting chat room:', error)
      throw error
    }
  }

  /**
   * Send a message with an optional attachment via HTTP
   * This triggers a WebSocket broadcast from the backend
   * @param text - Message text
   * @param file - File attachment
   */
  async function sendWithAttachment(text: string, file: File | null): Promise<void> {
    if (!activeRoomId.value) {
      throw new Error('No active chat room')
    }

    const formData = new FormData()
    if (text) formData.append('message', text)
    if (file) formData.append('attachment', file)

    try {
      await client.post(`/chat/rooms/${activeRoomId.value}/messages/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      // No need to manually add to messages, WebSocket will handle the broadcast
    } catch (error) {
      console.error('Error sending message with attachment:', error)
      throw error
    }
  }

  // Helper to set messages for a specific room (ensures reactivity)
  function setMessagesForRoom(roomId: number, messages: Message[]): void {
    console.log('[chatStore setMessagesForRoom] Setting', messages.length, 'messages for room', roomId)
    messagesByRoom.value[roomId] = messages
    console.log('[chatStore setMessagesForRoom] Verified:', messagesByRoom.value[roomId]?.length, 'messages stored')
  }

  // Helper to get messages for a specific room
  function getMessages(roomId: number | null): Message[] {
    if (!roomId) return []
    const msgs = messagesByRoom.value[roomId] || []
    console.log('[chatStore getMessages] Room', roomId, 'returning', msgs.length, 'messages')
    return msgs
  }

  return {
    // State
    rooms,
    activeRoomId,
    messagesByRoom,
    getMessages,
    websocket,
    // Actions
    fetchRooms,
    connectToRoom,
    sendMessage,
    disconnect,
    createOrGetRoom,
    sendWithAttachment,
    setMessagesForRoom,
  }
})
