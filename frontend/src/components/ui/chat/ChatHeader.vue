<template>
  <div
    class="bg-white border-b border-gray-200 px-4 py-3 flex items-center justify-between"
  >
    <!-- Columna izquierda: Nombre del interlocutor -->
    <div class="flex items-center gap-3 flex-1 min-w-0">
      <RouterLink :to="{ name: 'chats' }" class="flex-shrink-0">
        <svg
          class="w-6 h-6 text-gray-600"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M15 19l-7-7 7-7"
          />
        </svg>
      </RouterLink>
      <BaseAvatar v-if="participant" :name="participant.username" size="sm" />
      <div class="flex-1 min-w-0">
        <h2 class="text-lg font-semibold text-gray-900 truncate">
          {{ participant?.username || 'Usuario' }}
        </h2>
        <p v-if="participant?.email" class="text-xs text-gray-500 truncate">
          {{ participant.email }}
        </p>
      </div>
    </div>
    
    <!-- Columna derecha: "Tú" -->
    <div class="flex-shrink-0 ml-4">
      <span class="text-lg font-semibold text-gray-900">Tú</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { User } from '../../api/types'
import BaseAvatar from '../../base/BaseAvatar.vue'

interface Props {
  participant: User | null
}

defineProps<Props>()
</script>
