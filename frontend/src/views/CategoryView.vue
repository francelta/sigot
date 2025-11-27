<template>
  <div class="p-4 max-w-6xl mx-auto">
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
        {{ categoria?.nombre || 'Categoría' }}
      </h1>
      <p v-if="categoria?.descripcion" class="text-gray-600">
        {{ categoria.descripcion }}
      </p>
    </div>

    <!-- Loading state -->
    <div v-if="isLoading" class="flex justify-center items-center py-12">
      <BaseSpinner size="lg" color="primary" />
    </div>

    <!-- Error state -->
    <div v-else-if="errorMessage" class="text-center py-12">
      <p class="text-red-600 mb-4">{{ errorMessage }}</p>
      <BaseButton variant="outline" @click="loadCategory">
        Reintentar
      </BaseButton>
    </div>

    <!-- Subcategories -->
    <div v-else-if="subcategories.length > 0" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      <button
        v-for="subcat in subcategories"
        :key="subcat.id"
        @click="handleSubcategoryClick(subcat.id)"
        class="group relative overflow-hidden rounded-xl bg-white border-2 border-gray-200 hover:border-primary-500 transition-all duration-200 p-6 text-left shadow-sigot hover:shadow-sigot-lg transform hover:scale-[1.02]"
      >
        <div class="flex items-center justify-between mb-3">
          <div class="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center group-hover:bg-primary-200 transition-colors">
            <svg class="w-6 h-6 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
          </div>
          <svg class="w-5 h-5 text-gray-400 group-hover:text-primary-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </div>
        <h3 class="text-lg font-semibold text-gray-900 mb-1 group-hover:text-primary-600 transition-colors">
          {{ subcat.nombre }}
        </h3>
        <p v-if="subcat.descripcion" class="text-sm text-gray-600 line-clamp-2">
          {{ subcat.descripcion }}
        </p>
      </button>
    </div>

    <!-- Empty state (no subcategories) -->
    <div v-else class="py-12">
      <BaseEmptyState
        title="No hay subcategorías"
        message="Esta categoría no tiene subcategorías disponibles."
      >
        <template #action>
          <BaseButton variant="outline" @click="$router.back()">
            Volver
          </BaseButton>
        </template>
      </BaseEmptyState>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { fetchCategorias } from '../api/transportistas'
import type { Categoria } from '../api/transportistas'
import BaseButton from '../components/base/BaseButton.vue'
import BaseSpinner from '../components/base/BaseSpinner.vue'
import BaseEmptyState from '../components/base/BaseEmptyState.vue'

const route = useRoute()
const router = useRouter()

const categorias = ref<Categoria[]>([])
const isLoading = ref(false)
const errorMessage = ref('')

/**
 * Get category ID from route params
 */
const categoryId = computed(() => {
  const id = route.params.id
  return typeof id === 'string' ? parseInt(id, 10) : Number(id)
})

/**
 * Find the current category
 */
const categoria = computed(() => {
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
  return findCategory(categorias.value, categoryId.value)
})

/**
 * Get subcategories of the current category
 */
const subcategories = computed(() => {
  return categoria.value?.children || []
})

/**
 * Load categories from API
 */
async function loadCategory() {
  isLoading.value = true
  errorMessage.value = ''

  try {
    const data = await fetchCategorias()
    categorias.value = data

    // Verify category exists
    if (!categoria.value) {
      errorMessage.value = 'Categoría no encontrada'
    }
  } catch (error) {
    console.error('Error loading category:', error)
    errorMessage.value =
      'Error al cargar la categoría. Por favor, intenta nuevamente.'
  } finally {
    isLoading.value = false
  }
}

/**
 * Handle subcategory button click
 * Navigate to search view with subcategory ID
 */
function handleSubcategoryClick(subcategoryId: number) {
  router.push({
    name: 'search',
    params: { subcategoria_id: subcategoryId.toString() },
  })
}

onMounted(() => {
  loadCategory()
})
</script>


