<template>
  <div class="bg-gray-100 dark:bg-gray-800 px-4 py-2 flex items-end gap-2">
    <!-- Error message toast -->
    <div
      v-if="errorMessage"
      class="fixed bottom-20 left-1/2 transform -translate-x-1/2 px-4 py-2 bg-red-500 text-white rounded-full shadow-lg text-sm flex items-center gap-2 z-50"
    >
      <span>{{ errorMessage }}</span>
      <button
        type="button"
        class="ml-2 text-white hover:text-gray-200"
        @click="errorMessage = ''"
      >
        ✕
      </button>
    </div>

    <!-- File Input (Hidden) -->
    <input
      ref="fileInput"
      type="file"
      class="hidden"
      accept="image/*,.pdf,.doc,.docx"
      @change="handleFileSelect"
    />

    <!-- Attachment Button -->
    <button
      type="button"
      class="p-2 text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 focus:outline-none"
      @click="triggerFileInput"
    >
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
      </svg>
    </button>

    <form class="flex-1 flex items-end gap-2" @submit.prevent="handleSubmit">
      <div class="flex-1 bg-white dark:bg-gray-700 rounded-2xl border border-gray-300 dark:border-gray-600 px-4 py-2 flex flex-col min-h-[48px] justify-center">
        <!-- Selected File Preview -->
        <div v-if="selectedFile" class="mb-2 p-2 bg-gray-50 dark:bg-gray-600 rounded-lg relative group">
          <button 
            type="button" 
            class="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1 shadow-md hover:bg-red-600 z-10" 
            @click="clearFile"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
          
          <div v-if="previewUrl && selectedFile.type.startsWith('image/')" class="flex justify-center bg-gray-200 dark:bg-gray-500 rounded-lg overflow-hidden max-h-48">
            <img :src="previewUrl" class="max-w-full h-auto object-contain" alt="Vista previa" />
          </div>
          
          <div v-else class="flex items-center gap-3 p-2">
            <div class="flex-shrink-0 w-12 h-12 bg-gray-200 dark:bg-gray-500 rounded-lg flex items-center justify-center text-gray-500 dark:text-gray-300">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <div class="flex-1 min-w-0">
              <p class="text-sm font-medium text-gray-900 dark:text-white truncate">{{ selectedFile.name }}</p>
              <p class="text-xs text-gray-500 dark:text-gray-400">{{ (selectedFile.size / 1024).toFixed(1) }} KB</p>
            </div>
          </div>
        </div>

        <input
          v-model="messageText"
          type="text"
          placeholder="Escribe un mensaje..."
          class="w-full bg-transparent border-none focus:ring-0 p-0 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 text-base leading-relaxed"
          @keydown.enter.exact.prevent="handleSubmit"
        />
      </div>

      <button
        type="submit"
        :disabled="(!canSend && !selectedFile) || isSending"
        class="p-3 rounded-full bg-primary-600 text-white hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
      >
        <BaseSpinner v-if="isSending" size="sm" color="white" class="w-5 h-5" />
        <svg v-else class="w-5 h-5 transform rotate-90" fill="currentColor" viewBox="0 0 20 20">
          <path d="M10.894 2.553a1 1 0 00-1.788 0l-7 14a1 1 0 001.169 1.409l5-1.429A1 1 0 009 15.571V11a1 1 0 112 0v4.571a1 1 0 00.725.962l5 1.428a1 1 0 001.17-1.408l-7-14z" />
        </svg>
      </button>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import BaseSpinner from '../../base/BaseSpinner.vue'

const messageText = ref('')
const errorMessage = ref('')
const isSending = ref(false)
const fileInput = ref<HTMLInputElement | null>(null)
const selectedFile = ref<File | null>(null)
const previewUrl = ref<string | null>(null)

const canSend = computed(() => messageText.value.trim().length > 0)

const emit = defineEmits<{
  send: [
    message: string,
    file: File | null,
    onSuccess: () => void,
    onError: (error: Error) => void,
  ]
}>()

function triggerFileInput() {
  fileInput.value?.click()
}

function handleFileSelect(event: Event) {
  const input = event.target as HTMLInputElement
  if (input.files && input.files.length > 0) {
    const file = input.files[0]
    selectedFile.value = file
    
    // Create preview URL for images
    if (file.type.startsWith('image/')) {
      if (previewUrl.value) URL.revokeObjectURL(previewUrl.value)
      previewUrl.value = URL.createObjectURL(file)
    } else {
      previewUrl.value = null
    }
  }
}

function clearFile() {
  selectedFile.value = null
  if (previewUrl.value) {
    URL.revokeObjectURL(previewUrl.value)
    previewUrl.value = null
  }
  if (fileInput.value) {
    fileInput.value.value = ''
  }
}

function handleSubmit() {
  if ((!canSend.value && !selectedFile.value) || isSending.value) return

  const text = messageText.value.trim()
  const file = selectedFile.value

  // Clear previous error
  errorMessage.value = ''
  isSending.value = true

  // Define success and error handlers
  const onSuccess = () => {
    messageText.value = ''
    clearFile()
    isSending.value = false
  }

  const onError = (_error: Error) => {
    errorMessage.value = 'No se pudo enviar el mensaje. Intenta nuevamente.'
    isSending.value = false
  }

  // Emit send event with callbacks
  emit('send', text, file, onSuccess, onError)
}
</script>
