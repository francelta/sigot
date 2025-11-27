<template>
  <!-- Transportista Dashboard -->
  <TransportistaDashboard v-if="esTransportista" />

  <!-- Client Home -->
  <div v-else class="p-4 max-w-6xl mx-auto">
    <div class="mb-8 text-center">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">
        ¿Qué necesitas transportar?
      </h1>
      <p class="text-gray-600 dark:text-gray-300">
        Selecciona una categoría para comenzar tu búsqueda
      </p>
    </div>

    <!-- Loading state -->
    <div v-if="isLoading" class="flex justify-center items-center py-12">
      <BaseSpinner size="lg" color="primary" />
    </div>

    <!-- Error state -->
    <div v-else-if="errorMessage" class="text-center py-12">
      <p class="text-red-600 mb-4">{{ errorMessage }}</p>
      <BaseButton variant="outline" @click="loadCategories">
        Reintentar
      </BaseButton>
    </div>

    <!-- Category buttons (big buttons) -->
    <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-6">
      <button
        v-for="categoria in rootCategories"
        :key="categoria.id"
        @click="handleCategoryClick(categoria.id)"
        class="group relative overflow-hidden rounded-2xl bg-white dark:bg-gray-800 border-2 border-gray-200 dark:border-gray-700 hover:border-primary-500 dark:hover:border-primary-500 transition-all duration-200 p-8 text-left shadow-sigot hover:shadow-sigot-lg transform hover:scale-[1.02]"
      >
        <div class="flex items-start justify-between mb-4">
          <div class="w-16 h-16 bg-obra-100 dark:bg-obra-900/30 rounded-xl flex items-center justify-center group-hover:bg-obra-200 dark:group-hover:bg-obra-900/50 transition-colors">
            <component :is="getCategoryIcon(categoria.nombre)" class="w-8 h-8 text-obra-600 dark:text-obra-400" />
          </div>
          <svg class="w-6 h-6 text-gray-400 dark:text-gray-500 group-hover:text-primary-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </div>
        <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-2 group-hover:text-primary-600 dark:group-hover:text-primary-400 transition-colors">
          {{ categoria.nombre }}
        </h3>
        <p v-if="categoria.descripcion" class="text-sm text-gray-600 dark:text-gray-300">
          {{ categoria.descripcion }}
        </p>
        <p v-else class="text-sm text-gray-500 dark:text-gray-400">
          Ver subcategorías disponibles
        </p>
      </button>
    </div>

    <!-- Empty state (if no categories) -->
    <div v-if="!isLoading && !errorMessage && rootCategories.length === 0" class="text-center py-12">
      <BaseEmptyState
        title="No hay categorías disponibles"
        message="Por el momento no hay categorías de transporte disponibles. Intenta más tarde."
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, h } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/authStore'
import { fetchCategorias } from '../api/transportistas'
import type { Categoria } from '../api/transportistas'
import BaseButton from '../components/base/BaseButton.vue'
import BaseSpinner from '../components/base/BaseSpinner.vue'
import BaseEmptyState from '../components/base/BaseEmptyState.vue'
import TransportistaDashboard from './TransportistaDashboard.vue'

const router = useRouter()
const authStore = useAuthStore()
const esTransportista = computed(() => authStore.esTransportista)

const categorias = ref<Categoria[]>([])
const isLoading = ref(false)
const errorMessage = ref('')

/**
 * Get appropriate icon for category based on name
 */
function getCategoryIcon(categoriaNombre: string) {
  const nombre = categoriaNombre.toLowerCase()
  
  // Icono para Transporte de Mercancías - Camión
  if (nombre.includes('mercancía') || nombre.includes('mercadería') || nombre.includes('carga') || nombre.includes('transporte')) {
    return h('img', {
      src: '/iconos/truck_front_transport_vehicle_icon_123464.ico',
      alt: 'Transporte de mercancías',
      class: 'w-8 h-8 object-contain',
    })
  }
  
  // Icono para Transporte Especial y Servicios de Grúa - Grúa
  if (nombre.includes('grúa') || nombre.includes('grua') || nombre.includes('transporte especial') || nombre.includes('servicios de grúa')) {
    return h('img', {
      src: '/iconos/crane3_122401.ico',
      alt: 'Transporte Especial y Servicios de Grúa',
      class: 'w-8 h-8 object-contain',
    })
  }
  
  // Icono para Maquinaria de Construcción y Obra - Excavadora
  if (nombre.includes('maquinaria') || nombre.includes('construcción') || nombre.includes('obra')) {
    return h('img', {
      src: '/iconos/excavator_icon_136657.ico',
      alt: 'Maquinaria de construcción',
      class: 'w-8 h-8 object-contain',
    })
  }
  
  // Icono para Sector Agrícola - Tractor
  if (nombre.includes('agrícola') || nombre.includes('agricola') || nombre.includes('agro')) {
    return h('img', {
      src: '/iconos/agriculture_tractor_icon_195475.ico',
      alt: 'Sector agrícola',
      class: 'w-8 h-8 object-contain',
    })
  }
  
  // Icono para Mecánica Especializada - Llave inglesa (mantener SVG)
  if (nombre.includes('mecánica') || nombre.includes('mecanica') || nombre.includes('reparación') || nombre.includes('reparacion') || nombre.includes('especializada')) {
    return h('svg', {
      class: 'w-8 h-8 text-obra-600',
      fill: 'none',
      stroke: 'currentColor',
      viewBox: '0 0 24 24',
    }, [
      h('path', {
        'stroke-linecap': 'round',
        'stroke-linejoin': 'round',
        'stroke-width': '2',
        d: 'M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z',
      }),
      h('path', {
        'stroke-linecap': 'round',
        'stroke-linejoin': 'round',
        'stroke-width': '2',
        d: 'M15 12a3 3 0 11-6 0 3 3 0 016 0z',
      }),
    ])
  }
  
  // Icono por defecto - Camión genérico
  return h('img', {
    src: '/iconos/truck_front_transport_vehicle_icon_123464.ico',
    alt: 'Transporte',
    class: 'w-8 h-8 object-contain',
  })
}

/**
 * Get only root categories (parent === null)
 */
const rootCategories = computed(() => {
  return categorias.value.filter(cat => cat.parent === null)
})

/**
 * Load categories from API
 */
async function loadCategories() {
  isLoading.value = true
  errorMessage.value = ''

  try {
    const data = await fetchCategorias()
    categorias.value = data
  } catch (error) {
    console.error('Error loading categories:', error)
    errorMessage.value =
      'Error al cargar las categorías. Por favor, intenta nuevamente.'
  } finally {
    isLoading.value = false
  }
}

/**
 * Handle category button click
 * Navigate to category view to show subcategories
 */
function handleCategoryClick(categoriaId: number) {
  router.push({
    name: 'category',
    params: { id: categoriaId.toString() },
  })
}

onMounted(() => {
  loadCategories()
})
</script>
