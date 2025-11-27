<template>
  <div
    :class="[
      'flex flex-col max-w-[75%] rounded-lg px-3 py-2 mb-1',
      'shadow-sm',
      props.isMe
        ? props.isLast
          ? 'bg-green-700 self-end rounded-br-sm'
          : 'bg-green-500 self-end rounded-br-sm'
        : props.isLast
          ? 'bg-purple-700 self-start rounded-bl-sm'
          : 'bg-purple-500 self-start rounded-bl-sm',
    ]"
  >
    <!-- Attachment Image -->
    <div v-if="attachment" class="mb-2 rounded-lg overflow-hidden bg-black/10">
      <img
        v-if="isImage(attachment)"
        :src="getFullUrl(attachment)"
        alt="Adjunto"
        class="max-w-full h-auto max-h-64 object-contain cursor-pointer"
        @click="openImage(attachment)"
      />
      <a
        v-else
        :href="getFullUrl(attachment)"
        target="_blank"
        class="flex items-center gap-2 p-3 text-white hover:underline"
      >
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
        <span>Descargar archivo</span>
      </a>
    </div>

    <p
      v-if="message"
      :class="[
        'text-sm break-words leading-relaxed',
        'text-white',
      ]"
    >
      {{ message }}
    </p>
    <span
      :class="[
        'text-xs mt-1 self-end flex items-center gap-1',
        'text-white opacity-80',
      ]"
    >
      {{ formattedTimestamp }}
      <!-- Double check mark for sent/read messages -->
      <span
        v-if="props.isMe"
        :class="[
          'ml-1 transition-colors',
          props.isRead ? 'text-green-500' : 'text-white/60'
        ]"
      >
        ✓✓
      </span>
    </span>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  isMe: boolean
  message: string
  timestamp: string
  isLast?: boolean
  attachment?: string | null
  isRead?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  isLast: false,
  attachment: null,
})

function isImage(url: string): boolean {
  return /\.(jpg|jpeg|png|gif|webp)$/i.test(url)
}

function getFullUrl(url: string): string {
  if (url.startsWith('http')) return url
  // Assuming backend is at localhost:8000 for local dev
  // In production, this should use an env var
  return `http://localhost:8000${url}`
}

function openImage(url: string) {
  window.open(getFullUrl(url), '_blank')
}

const formattedTimestamp = computed(() => {
  try {
    const date = new Date(props.timestamp)
    const now = new Date()
    
    // Reset time parts for day comparison
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate())
    const messageDate = new Date(date.getFullYear(), date.getMonth(), date.getDate())
    const diffDays = Math.floor((today.getTime() - messageDate.getTime()) / (1000 * 60 * 60 * 24))

    const timeStr = date.toLocaleTimeString('es-ES', {
      hour: '2-digit',
      minute: '2-digit',
    })

    // Today: just show time
    if (diffDays === 0) {
      return timeStr
    }

    // Yesterday: show "ayer, a las HH:MM"
    if (diffDays === 1) {
      return `ayer, a las ${timeStr}`
    }

    // Day before yesterday: show "anteayer, a las HH:MM"
    if (diffDays === 2) {
      return `anteayer, a las ${timeStr}`
    }

    // Older: show "dayName day month, a las HH:MM"
    const dayName = date.toLocaleDateString('es-ES', { weekday: 'long' })
    const day = date.getDate()
    const month = date.toLocaleDateString('es-ES', { month: 'long' })
    
    return `${dayName} ${day} ${month}, a las ${timeStr}`
  } catch {
    return props.timestamp
  }
})
</script>
