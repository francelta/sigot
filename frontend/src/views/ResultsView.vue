<template>
  <div class="p-4 max-w-4xl mx-auto">
    <div class="mb-6">
      <h1 class="text-2xl font-bold text-gray-900 mb-2">
        Resultados de Búsqueda
      </h1>
      <p v-if="searchParams.q" class="text-gray-600">
        Buscando en: <span class="font-semibold">{{ searchParams.q }}</span>
      </p>
    </div>

    <!-- Loading state -->
    <div v-if="isLoading" class="flex justify-center items-center py-12">
      <BaseSpinner size="lg" color="primary" />
    </div>

    <!-- Error state -->
    <div v-else-if="errorMessage" class="text-center py-12">
      <p class="text-red-600 mb-4">{{ errorMessage }}</p>
      <BaseButton variant="outline" @click="$router.push({ name: 'home' })">
        Volver a buscar
      </BaseButton>
    </div>

    <!-- Results -->
    <div v-else-if="transportistas.length > 0" class="space-y-4">
      <p class="text-sm text-gray-600 mb-4">
        Se encontraron {{ count }} transportista{{ count !== 1 ? 's' : '' }}
      </p>

      <div
        v-for="transportista in transportistas"
        :key="transportista.id"
        class="mb-4"
      >
        <BaseCard padding="lg" shadow="md">
          <div
            class="flex flex-col md:flex-row md:items-center md:justify-between gap-4"
          >
            <div class="flex-1">
              <div class="flex items-center gap-3 mb-2">
                <h3 class="text-lg font-semibold text-gray-900">
                  {{ transportista.user.username }}
                </h3>
                <span
                  v-if="transportista.disponible"
                  class="px-2 py-1 text-xs font-medium bg-green-100 text-green-800 rounded-full"
                >
                  Disponible
                </span>
                <span
                  v-else
                  class="px-2 py-1 text-xs font-medium bg-gray-100 text-gray-800 rounded-full"
                >
                  No disponible
                </span>
              </div>

              <p
                v-if="transportista.user.email"
                class="text-sm text-gray-600 mb-2"
              >
                {{ transportista.user.email }}
              </p>

              <div v-if="transportista.categorias.length > 0" class="mb-2">
                <div class="flex flex-wrap gap-2">
                  <span
                    v-for="categoria in transportista.categorias"
                    :key="categoria.id"
                    class="px-2 py-1 text-xs bg-primary-100 text-primary-800 rounded"
                  >
                    {{ categoria.nombre }}
                  </span>
                </div>
              </div>

              <div
                v-if="transportista.codigo_postal"
                class="text-sm text-gray-600"
              >
                <span class="font-medium">Código Postal:</span>
                {{ transportista.codigo_postal }}
              </div>

              <div
                v-if="
                  transportista.tipo_zona_actuacion === 'RADIO' &&
                  transportista.radio_km_general
                "
                class="text-sm text-gray-600 mt-1"
              >
                <span class="font-medium">Radio de actuación:</span>
                {{ transportista.radio_km_general }} km
              </div>
            </div>

            <div class="flex-shrink-0">
              <BaseButton
                variant="primary"
                @click="handleContact(transportista.user.id)"
              >
                Contactar
              </BaseButton>
            </div>
          </div>
        </BaseCard>
      </div>
    </div>

    <!-- No results - Use BaseEmptyState -->
    <div v-else>
      <BaseEmptyState
        title="No se encontraron transportistas"
        message="Ups, no tenemos servicio en esta zona para esa categoría. Intenta con otra ubicación o categoría."
      >
        <template #action>
          <div class="flex flex-col sm:flex-row gap-3 justify-center">
            <BaseButton variant="outline" @click="$router.push({ name: 'home' })">
              Volver al inicio
            </BaseButton>
            <BaseButton variant="primary" @click="$router.back()">
              Cambiar búsqueda
            </BaseButton>
          </div>
        </template>
      </BaseEmptyState>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { fetchTransportistasPorZona } from '../api/transportistas'
import type { Transportista } from '../api/transportistas'
import { useChatStore } from '../stores/chatStore'
import BaseCard from '../components/base/BaseCard.vue'
import BaseButton from '../components/base/BaseButton.vue'
import BaseSpinner from '../components/base/BaseSpinner.vue'
import BaseEmptyState from '../components/base/BaseEmptyState.vue'

const route = useRoute()
const router = useRouter()
const chatStore = useChatStore()

const transportistas = ref<Transportista[]>([])
const count = ref(0)
const isLoading = ref(false)
const errorMessage = ref('')

/**
 * Extract search parameters from route query
 */
const searchParams = computed(() => {
  return {
    q: (route.query.q as string) || '',
    categoria: route.query.categoria
      ? Number(route.query.categoria)
      : undefined,
  }
})

/**
 * Load transportistas on component mount
 */
onMounted(async () => {
  if (!searchParams.value.q) {
    // If no search query, redirect to home
    router.push({ name: 'home' })
    return
  }

  isLoading.value = true
  errorMessage.value = ''

  try {
    const params: { q: string; categoria?: number } = {
      q: searchParams.value.q,
    }

    if (searchParams.value.categoria) {
      params.categoria = searchParams.value.categoria
    }

    const response = await fetchTransportistasPorZona(params)
    transportistas.value = response.results
    count.value = response.count
  } catch (error) {
    console.error('Error fetching transportistas:', error)
    errorMessage.value =
      'Error al buscar transportistas. Por favor, intenta nuevamente.'
  } finally {
    isLoading.value = false
  }
})

/**
 * Handle contact button click
 * Creates or gets chat room and navigates to it
 */
async function handleContact(userId: number) {
  try {
    const room = await chatStore.createOrGetRoom(userId)
    router.push({ name: 'chat-room', params: { id: room.id } })
  } catch (error) {
    console.error('Error creating/getting chat room:', error)
    // TODO: Show error message to user
  }
}
</script>
