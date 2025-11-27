<template>
  <div class="p-4 max-w-2xl mx-auto">
    <!-- Header -->
    <div class="mb-6">
      <button
        @click="$router.back()"
        class="flex items-center gap-2 text-gray-600 hover:text-primary-600 mb-4 transition-colors"
      >
        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
        <span class="text-sm font-medium">Volver</span>
      </button>
      <h1 class="text-3xl font-bold text-gray-900 mb-2">
        ¿Dónde necesitas el servicio?
      </h1>
      <p class="text-gray-600">
        Indica la ubicación donde necesitas el transporte
      </p>
    </div>

    <!-- Loading state -->
    <div v-if="isLoadingCategory" class="flex justify-center items-center py-12">
      <BaseSpinner size="lg" color="primary" />
    </div>

    <!-- Search form -->
    <BaseCard v-else padding="lg" shadow="md">
      <form class="space-y-6" @submit.prevent="handleSearch">
        <!-- Category info (read-only) -->
        <div v-if="subcategory" class="p-4 bg-primary-50 rounded-xl border border-primary-200">
          <p class="text-sm text-gray-600 mb-1">Categoría seleccionada:</p>
          <p class="font-semibold text-primary-700">{{ subcategory.nombre }}</p>
        </div>

        <!-- Location input -->
        <BaseInput
          v-model="form.ubicacion"
          label="Ubicación"
          type="text"
          placeholder="Ej: Madrid, CP: 28001, Calle Gran Vía 1"
          :error="errors.ubicacion"
          required
        />
        <p class="text-xs text-gray-500 -mt-4">
          Puedes indicar una ciudad, código postal o dirección específica
        </p>

        <!-- Error message -->
        <div v-if="errorMessage" class="p-3 bg-red-50 border border-red-200 rounded-xl">
          <p class="text-sm text-red-600">{{ errorMessage }}</p>
        </div>

        <!-- Submit button -->
        <BaseButton
          type="submit"
          variant="primary"
          :disabled="isSearching || !form.ubicacion.trim()"
          class="w-full"
          size="lg"
        >
          <span v-if="!isSearching">Buscar Transportistas</span>
          <span v-else class="flex items-center justify-center">
            <BaseSpinner size="sm" color="white" class="mr-2" />
            Buscando...
          </span>
        </BaseButton>
      </form>
    </BaseCard>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { fetchCategorias } from '../api/transportistas'
import type { Categoria } from '../api/transportistas'
import BaseCard from '../components/base/BaseCard.vue'
import BaseInput from '../components/base/BaseInput.vue'
import BaseButton from '../components/base/BaseButton.vue'
import BaseSpinner from '../components/base/BaseSpinner.vue'

const route = useRoute()
const router = useRouter()

const categorias = ref<Categoria[]>([])
const isLoadingCategory = ref(false)
const isSearching = ref(false)
const errorMessage = ref('')

const form = reactive({
  ubicacion: '',
})

const errors = reactive({
  ubicacion: '',
})

/**
 * Get subcategory ID from route params
 */
const subcategoryId = computed(() => {
  const id = route.params.subcategoria_id
  return typeof id === 'string' ? parseInt(id, 10) : Number(id)
})

/**
 * Find the subcategory
 */
const subcategory = computed(() => {
  function findCategory(cats: Categoria[], id: number): Categoria | null {
    for (const cat of cats) {
      if (cat.id === id) return cat
      if (cat.children) {
        const found = findCategory(cat.children, id)
        if (found) return found
      }
    }
    return null
  }
  return findCategory(categorias.value, subcategoryId.value)
})

/**
 * Load categories to get subcategory info
 */
async function loadCategory() {
  isLoadingCategory.value = true
  try {
    const data = await fetchCategorias()
    categorias.value = data
  } catch (error) {
    console.error('Error loading category:', error)
    errorMessage.value = 'Error al cargar la información. Por favor, intenta nuevamente.'
  } finally {
    isLoadingCategory.value = false
  }
}

/**
 * Handle form submission
 */
function handleSearch() {
  // Reset errors
  errors.ubicacion = ''
  errorMessage.value = ''

  // Validate form
  if (!form.ubicacion.trim()) {
    errors.ubicacion = 'La ubicación es requerida'
    return
  }

  isSearching.value = true

  // Build query parameters
  const query: Record<string, string> = {
    q: form.ubicacion.trim(),
  }

  // Add subcategory as category filter
  if (subcategoryId.value) {
    query.categoria = subcategoryId.value.toString()
  }

  // Navigate to results view
  router.push({
    name: 'results',
    query,
  })

  isSearching.value = false
}

onMounted(() => {
  loadCategory()
})
</script>


