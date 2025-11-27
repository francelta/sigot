<template>
  <div class="flex flex-col h-screen bg-gray-50 dark:bg-gray-900">
    <!-- Navbar -->
    <LandingNav />
    
    <div class="pt-16 flex h-[calc(100vh-4rem)]">
      <!-- Sidebar: Lista de conversaciones (25%) -->
      <div class="w-1/4 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 flex flex-col">
        <!-- Header del sidebar -->
        <div class="px-4 py-3 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
          <h2 class="text-lg font-semibold text-gray-900 dark:text-white">Conversaciones</h2>
          <BaseButton
            variant="ghost"
            size="sm"
            @click="handleExitChat"
            class="!text-primary-500"
          >
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </BaseButton>
        </div>
        
        <!-- Lista de conversaciones -->
        <div class="flex-1 overflow-y-auto">
          <div v-if="isLoadingRooms" class="flex justify-center items-center py-8">
            <BaseSpinner size="md" color="primary" />
          </div>
          
          <div v-else-if="sortedRooms.length === 0" class="p-4 text-center bg-white dark:bg-gray-800">
            <p class="text-sm text-gray-500 dark:text-gray-400">No hay conversaciones</p>
          </div>
          
          <button
            v-for="room in sortedRooms"
            :key="room.id"
            @click="switchToRoom(room.id)"
            :class="[
              'w-full px-4 py-3 text-left border-b border-gray-100 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors',
              activeRoomId === room.id ? 'bg-primary-50 dark:bg-primary-900/20 border-l-4 border-l-primary-500' : ''
            ]"
          >
            <div class="flex items-center gap-3">
              <BaseAvatar
                :name="getOtherParticipant(room)?.username || 'Usuario'"
                size="sm"
              />
              <div class="flex-1 min-w-0">
                <div class="flex items-center justify-between mb-1">
                  <h3 class="text-sm font-semibold text-gray-900 dark:text-white truncate">
                    {{ getOtherParticipant(room)?.username || 'Usuario' }}
                  </h3>
                  <div class="flex items-center gap-2 flex-shrink-0">
                    <!-- Contador de mensajes sin leer -->
                    <span
                      v-if="getUnreadCount(room) > 0"
                      class="bg-red-500 text-white text-xs font-bold rounded-full min-w-[20px] h-5 px-2 flex items-center justify-center"
                    >
                      {{ getUnreadCount(room) > 99 ? '99+' : getUnreadCount(room) }}
                    </span>
                    <span
                      v-if="room.last_message"
                      class="text-xs text-gray-500 dark:text-gray-400"
                    >
                      {{ formatTime(room.last_message.created_at) }}
                    </span>
                  </div>
                </div>
                <p v-if="room.last_message" class="text-xs text-gray-600 dark:text-gray-300 truncate">
                  {{ room.last_message.body }}
                </p>
                <p v-else class="text-xs text-gray-400 dark:text-gray-500 italic">Sin mensajes</p>
              </div>
            </div>
          </button>
        </div>
      </div>
      
      <!-- Área de chat (75%) -->
      <div class="flex-1 flex flex-col bg-gray-100 dark:bg-gray-900 overflow-hidden">
        <!-- Header -->
        <ChatHeader :participant="otherParticipant" />

        <!-- Connection error banner -->
        <div
          v-if="connectionError"
          class="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-4 py-3 flex items-center gap-3 flex-shrink-0"
        >
          <svg
            class="w-5 h-5 text-red-600 flex-shrink-0"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          <p class="text-sm text-red-700 flex-1">{{ connectionError }}</p>
        </div>

        <!-- Reconnecting indicator -->
        <div
          v-if="isConnecting && !connectionError"
          class="bg-yellow-50 border-b border-yellow-200 px-4 py-2 flex items-center gap-2 flex-shrink-0"
        >
          <BaseSpinner size="sm" color="yellow" />
          <p class="text-sm text-yellow-700">Reconectando...</p>
        </div>

        <!-- Messages area -->
        <div
          ref="messagesContainer"
          class="flex-1 overflow-y-auto px-4 py-4 space-y-2 min-h-0 flex flex-col"
        >
          <div v-if="isLoading" class="flex justify-center items-center py-8">
            <BaseSpinner size="md" color="primary" />
          </div>

          <div
            v-else-if="messages.length === 0"
            class="flex flex-col items-center justify-center py-12"
          >
            <p class="text-gray-500 dark:text-gray-400 text-sm">No hay mensajes aún</p>
            <p class="text-gray-400 dark:text-gray-500 text-xs mt-1">Envía el primer mensaje</p>
          </div>

          <div
            v-for="(message, index) in messages"
            :key="message.id"
            :class="[
              'flex w-full mb-2',
              isMyMessage(message) ? 'justify-end' : 'justify-start items-end gap-2'
            ]"
          >
            <!-- Avatar for other user (only if not me) -->
            <BaseAvatar
              v-if="!isMyMessage(message)"
              :name="message.author.username"
              :src="message.author.photo_url"
              size="xs"
              class="flex-shrink-0 mb-1"
            />

            <BaseChatBubble
              :is-me="isMyMessage(message)"
              :message="message.body || ''"
              :attachment="message.attachment"
              :timestamp="message.created_at || ''"
              :is-last="index === messages.length - 1"
              :is-read="isMessageRead(message)"
            />
          </div>
        </div>

        <!-- Input bar - FIXED AT BOTTOM -->
        <div class="flex-shrink-0">
          <ChatInputBar @send="handleSendMessage" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, watch, nextTick, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useChatStore } from '../stores/chatStore'
import { useAuthStore } from '../stores/authStore'
import { useChatRoom } from '../composables/useChatRoom'
import type { Message, ChatRoom } from '../api/chat'
import client from '../api/client'
import LandingNav from '../components/ui/LandingNav.vue'
import ChatHeader from '../components/ui/chat/ChatHeader.vue'
import ChatInputBar from '../components/ui/chat/ChatInputBar.vue'
import BaseChatBubble from '../components/base/BaseChatBubble.vue'
import BaseSpinner from '../components/base/BaseSpinner.vue'
import BaseButton from '../components/base/BaseButton.vue'
import BaseAvatar from '../components/base/BaseAvatar.vue'

const messagesContainer = ref<HTMLElement | null>(null)
const isLoading = ref(false)
const isLoadingMore = ref(false)
const displayedMessageCount = ref(8) // Start with 8 messages
const MESSAGES_PER_PAGE = 8

const authStore = useAuthStore()
const router = useRouter()
const route = useRoute()

const chatStore = useChatStore()
const { sendMessage, connectionError, isConnecting } = useChatRoom()

// Debug: Log authStore.user on mount
onMounted(() => {
  console.log('ChatRoomView mounted, authStore.user:', authStore.user)
  console.log('ChatRoomView mounted, messages:', chatStore.getMessages(Number(route.params.id)))
})

const isLoadingRooms = ref(false)

/**
 * Track unread message counts per room
 */
const unreadCounts = ref<Record<number, number>>({})

/**
 * Check if message is from current user
 * MUST be defined before messages computed
 */
function isMyMessage(message: Message): boolean {
  if (!message || !message.author) {
    return false
  }
  
  const currentUser = authStore.user
  if (!currentUser || !currentUser.id) {
    return false
  }
  
  // Convert to numbers to ensure type matching
  const authorId = Number(message.author.id)
  const userId = Number(currentUser.id)
  
  // Check if IDs match (and both are valid numbers)
  if (authorId === 0 || isNaN(authorId)) {
    return false
  }
  
  if (userId === 0 || isNaN(userId)) {
    return false
  }
  
  const isMine = authorId === userId
  
  // Debug log
  if (isMine) {
    console.log('[isMyMessage] Message is MINE:', {
      messageId: message.id,
      authorId,
      userId,
      messageBody: message.body?.substring(0, 20)
    })
  }
  
  return isMine
}

/**
 * Check if a message has been read by the recipient
 */
function isMessageRead(message: Message): boolean {
  // Only show read receipts for my messages
  if (!isMyMessage(message)) return false
  
  // Get the other participant's last_read_at from active room
  const room = chatStore.rooms.find(r => r.id === activeRoomId.value)
  if (!room) return false
  
  const otherParticipant = room.participants.find(
    p => p.id !== authStore.user?.id
  )
  
  if (!otherParticipant?.last_read_at) return false
  
  // Compare message created_at with other user's last_read_at
  const messageTime = new Date(message.created_at)
  const lastReadTime = new Date(otherParticipant.last_read_at)
  
  return messageTime <= lastReadTime
}

/**
 * Mark current room as read
 */
async function markRoomAsRead() {
  if (!activeRoomId.value) return
  
  // Temporarily disabled due to backend error
  return
  
  try {
    await client.post(`/chat/rooms/${activeRoomId.value}/mark_read/`)
  } catch (error) {
    console.error('Error marking room as read:', error)
  }
}

/**
 * Get paginated messages for the active room from store
 */
const messages = computed(() => {
  const allMessages = chatStore.getMessages(activeRoomId.value)
  // Return the last displayedMessageCount messages (oldest first)
  if (allMessages.length <= displayedMessageCount.value) {
    return allMessages
  }
  return allMessages.slice(allMessages.length - displayedMessageCount.value)
})

/**
 * Get active room ID from route
 */
const activeRoomId = computed(() => {
  const id = route.params.id
  return typeof id === 'string' ? parseInt(id, 10) : Number(id)
})

/**
 * Get sorted rooms by last message time (most recent first)
 */
const sortedRooms = computed(() => {
  const rooms = [...chatStore.rooms]
  return rooms.sort((a, b) => {
    // If room has no last message, put it at the end
    if (!a.last_message && !b.last_message) return 0
    if (!a.last_message) return 1
    if (!b.last_message) return -1
    
    // Sort by last message time (most recent first)
    const timeA = new Date(a.last_message!.created_at).getTime()
    const timeB = new Date(b.last_message!.created_at).getTime()
    return timeB - timeA
  })
})

/**
 * Get the other participant (not the current user) from a room
 */
function getOtherParticipant(room: ChatRoom) {
  const currentUserId = authStore.user?.id
  if (!currentUserId) return null
  return (
    room.participants.find(p => p.id !== currentUserId) || room.participants[0]
  )
}

/**
 * Calculate unread message count for a room
 * Messages are unread if:
 * - They are not from the current user
 * - The room is not the active room (user is not viewing it)
 */
function getUnreadCount(room: ChatRoom): number {
  // If this is the active room, no unread messages (mark as read)
  if (room.id === activeRoomId.value) {
    unreadCounts.value[room.id] = 0
    return 0
  }

  // If there's no last message, no unread
  if (!room.last_message) {
    return unreadCounts.value[room.id] || 0
  }

  // If the last message is from the current user, no unread
  const currentUserId = authStore.user?.id
  if (room.last_message.author.id === currentUserId) {
    unreadCounts.value[room.id] = 0
    return 0
  }

  // If we don't have a count for this room, initialize it
  if (!(room.id in unreadCounts.value)) {
    unreadCounts.value[room.id] = 1
  }

  return unreadCounts.value[room.id] || 0
}

/**
 * Format timestamp for display
 */
function formatTime(timestamp: string): string {
  try {
    const date = new Date(timestamp)
    const now = new Date()
    const diffMs = now.getTime() - date.getTime()
    const diffMins = Math.floor(diffMs / 60000)

    if (diffMins < 1) return 'Ahora'
    if (diffMins < 60) return `Hace ${diffMins} min`

    if (date.toDateString() === now.toDateString()) {
      return date.toLocaleTimeString('es-ES', {
        hour: '2-digit',
        minute: '2-digit',
      })
    }

    const yesterday = new Date(now)
    yesterday.setDate(yesterday.getDate() - 1)
    if (date.toDateString() === yesterday.toDateString()) {
      return 'Ayer'
    }

    return date.toLocaleDateString('es-ES', {
      day: 'numeric',
      month: 'short',
    })
  } catch {
    return timestamp
  }
}

/**
 * Switch to a different chat room
 */
function switchToRoom(roomId: number) {
  if (roomId === activeRoomId.value) return
  // Mark room as read when switching to it
  unreadCounts.value[roomId] = 0
  const room = chatStore.rooms.find(r => r.id === roomId)
  if (room?.last_message) {
    lastSeenMessageIds.value[roomId] = room.last_message.id
  }
  router.push({ name: 'chat-room', params: { id: roomId } })
}

/**
 * Exit chat and go back to home or chat list
 */
function handleExitChat() {
  router.push({ name: 'chats' })
}

/**
 * Get other participant (not current user) for the active room
 */
const otherParticipant = computed(() => {
  const currentUserId = authStore.user?.id
  if (!currentUserId) return null

  const activeRoom = chatStore.rooms.find(r => r.id === activeRoomId.value)
  if (!activeRoom) return null

  return (
    activeRoom.participants.find(p => p.id !== currentUserId) ||
    activeRoom.participants[0]
  )
})


/**
 * Handle sending a message
 */
async function handleSendMessage(
  text: string,
  file: File | null,
  onSuccess: () => void,
  onError: (error: Error) => void
) {
  try {
    if (file) {
      // Use HTTP endpoint for files (triggers WS broadcast)
      await chatStore.sendWithAttachment(text, file)
    } else {
      // Use WebSocket for text-only (faster)
      await sendMessage(text)
    }
    
    // Scroll to bottom after sending
    nextTick(() => {
      scrollToBottom()
    })
    // Call success callback to clear input
    onSuccess()
  } catch (error) {
    console.error('Error sending message:', error)
    // Call error callback to show error message
    const err = error instanceof Error ? error : new Error('Error desconocido')
    onError(err)
  }
}

/**
 * Scroll messages container to bottom
 */
function scrollToBottom() {
  if (messagesContainer.value) {
    messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
  }
}

/**
 * Watch for new messages and auto-scroll
 */
watch(
  messages,
  () => {
    nextTick(() => {
      scrollToBottom()
    })
  },
  { deep: true }
)

/**
 * Set loading to false once messages are loaded
 */
watch(
  () => chatStore.activeRoomId,
  () => {
    if (chatStore.activeRoomId) {
      isLoading.value = false
      // Mark current room as read when it becomes active
      unreadCounts.value[chatStore.activeRoomId] = 0
    }
  },
  { immediate: true }
)

/**
 * Track last seen message ID per room to avoid double counting
 */
const lastSeenMessageIds = ref<Record<number, number>>({})

/**
 * Watch for new messages in rooms to update unread counts
 * This watches the rooms array and updates unread counts when new messages arrive
 */
watch(
  () => chatStore.rooms,
  (newRooms, oldRooms) => {
    const currentUserId = authStore.user?.id
    if (!currentUserId) return
    
    newRooms.forEach((room) => {
      // Skip if this is the active room (already marked as read)
      if (room.id === activeRoomId.value) {
        unreadCounts.value[room.id] = 0
        if (room.last_message) {
          lastSeenMessageIds.value[room.id] = room.last_message.id
        }
        return
      }
      
      // If there's a last message from another user
      if (room.last_message && room.last_message.author.id !== currentUserId) {
        const lastSeenId = lastSeenMessageIds.value[room.id] || 0
        
        // Only increment if this is a new message we haven't seen
        if (room.last_message.id > lastSeenId) {
          const existingCount = unreadCounts.value[room.id] || 0
          unreadCounts.value[room.id] = existingCount + 1
          lastSeenMessageIds.value[room.id] = room.last_message.id
        }
      } else if (room.last_message && room.last_message.author.id === currentUserId) {
        // Message from current user, mark as read
        unreadCounts.value[room.id] = 0
        if (room.last_message) {
          lastSeenMessageIds.value[room.id] = room.last_message.id
        }
      }
    })
  },
  { deep: true }
)

/**
 * Load chat rooms
 */
async function loadRooms() {
  isLoadingRooms.value = true
  try {
    await chatStore.fetchRooms()
  } catch (error) {
    console.error('Error loading chat rooms:', error)
  } finally {
    isLoadingRooms.value = false
  }
}

/**
 * Load more messages when scrolling to top
 */
function handleScroll() {
  if (!messagesContainer.value || isLoadingMore.value) return

  const container = messagesContainer.value
  const scrollTop = container.scrollTop

  // If scrolled to top (with 50px threshold), load more
  if (scrollTop <= 50 && displayedMessageCount.value < chatStore.getMessages(activeRoomId.value).length) {
    loadMoreMessages()
  }
}

/**
 * Load more messages
 */
function loadMoreMessages() {
  if (isLoadingMore.value) return
  
  const totalMessages = chatStore.getMessages(activeRoomId.value).length
  const remaining = totalMessages - displayedMessageCount.value
  
  if (remaining <= 0) return

  isLoadingMore.value = true
  
  // Capture current scroll height before adding messages
  const container = messagesContainer.value
  const previousScrollHeight = container?.scrollHeight || 0

  // Load 8 more messages
  const toLoad = Math.min(MESSAGES_PER_PAGE, remaining)
  displayedMessageCount.value += toLoad

  // After DOM updates, restore scroll position
  nextTick(() => {
    if (container) {
      const newScrollHeight = container.scrollHeight
      const heightDifference = newScrollHeight - previousScrollHeight
      container.scrollTop = heightDifference
    }
    isLoadingMore.value = false
  })
}

/**
 * Watch for new messages and auto-scroll
 */
watch(
  () => chatStore.getMessages(activeRoomId.value).length,
  (newLength, oldLength) => {
    if (newLength > oldLength) {
      // New message received, scroll to bottom
      scrollToBottom()
    }
  }
)

/**
 * Watch for room changes and reset pagination
 */
watch(
  activeRoomId,
  () => {
    displayedMessageCount.value = MESSAGES_PER_PAGE
    nextTick(() => {
      scrollToBottom()
      // Mark room as read when opening it
      markRoomAsRead()
    })
  }
)

onMounted(() => {
  // Load chat rooms
  loadRooms()
  
  // Initial scroll to bottom
  nextTick(() => {
    scrollToBottom()
  })
  
  // Add scroll listener
  if (messagesContainer.value) {
    messagesContainer.value.addEventListener('scroll', handleScroll)
  }
})

onUnmounted(() => {
  if (messagesContainer.value) {
    messagesContainer.value.removeEventListener('scroll', handleScroll)
  }
})
</script>
