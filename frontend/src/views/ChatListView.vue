<template>
  <div class="h-full flex flex-col bg-gray-50">
    <div class="bg-white border-b border-gray-200 px-4 py-3">
      <h1 class="text-xl font-semibold text-gray-900">Chats</h1>
    </div>

    <!-- Loading state -->
    <div v-if="isLoading" class="flex-1 flex justify-center items-center">
      <BaseSpinner size="lg" color="primary" />
    </div>

    <!-- Error state -->
    <div
      v-else-if="errorMessage"
      class="flex-1 flex flex-col justify-center items-center p-4"
    >
      <p class="text-red-600 mb-4">{{ errorMessage }}</p>
      <BaseButton variant="outline" @click="loadRooms">Reintentar</BaseButton>
    </div>

    <!-- Chat list -->
    <div v-else-if="rooms.length > 0" class="flex-1 overflow-y-auto">
      <RouterLink
        v-for="room in rooms"
        :key="room.id"
        :to="{ name: 'chat-room', params: { id: room.id } }"
        class="flex items-center gap-3 px-4 py-3 bg-white border-b border-gray-100 hover:bg-gray-50 transition-colors"
      >
        <BaseAvatar
          :name="getOtherParticipant(room)?.username || 'Usuario'"
          size="md"
        />
        <div class="flex-1 min-w-0">
          <div class="flex items-center justify-between mb-1">
            <h3 class="text-sm font-semibold text-gray-900 truncate">
              {{ getOtherParticipant(room)?.username || 'Usuario' }}
            </h3>
            <span
              v-if="room.last_message"
              class="text-xs text-gray-500 flex-shrink-0 ml-2"
            >
              {{ formatTime(room.last_message.created_at) }}
            </span>
          </div>
          <p v-if="room.last_message" class="text-sm text-gray-600 truncate">
            {{ room.last_message.body }}
          </p>
          <p v-else class="text-sm text-gray-400 italic">Sin mensajes</p>
        </div>
      </RouterLink>
    </div>

    <!-- Empty state -->
    <div v-else class="flex-1 flex flex-col justify-center items-center p-4">
      <p class="text-gray-600 mb-2">No tienes conversaciones</p>
      <p class="text-sm text-gray-500 text-center">
        Busca un transportista y haz clic en "Contactar" para iniciar un chat
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useChatStore } from '../stores/chatStore'
import { useAuthStore } from '../stores/authStore'
import type { ChatRoom } from '../api/chat'
import BaseAvatar from '../components/base/BaseAvatar.vue'
import BaseButton from '../components/base/BaseButton.vue'
import BaseSpinner from '../components/base/BaseSpinner.vue'

const chatStore = useChatStore()
const authStore = useAuthStore()

const isLoading = ref(false)
const errorMessage = ref('')

const rooms = computed(() => chatStore.rooms)

/**
 * Get the other participant (not the current user)
 */
function getOtherParticipant(room: ChatRoom) {
  const currentUserId = authStore.user?.id
  if (!currentUserId) return null
  return (
    room.participants.find(p => p.id !== currentUserId) || room.participants[0]
  )
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
 * Load chat rooms
 */
async function loadRooms() {
  isLoading.value = true
  errorMessage.value = ''

  try {
    await chatStore.fetchRooms()
  } catch (error) {
    console.error('Error loading chat rooms:', error)
    errorMessage.value =
      'Error al cargar las conversaciones. Intenta nuevamente.'
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  loadRooms()
})
</script>
