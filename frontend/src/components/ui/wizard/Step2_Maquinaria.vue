<template>
  <div class="space-y-6">
    <div>
      <h2 class="text-xl font-semibold text-gray-900 mb-2">
        Maquinaria Disponible
      </h2>
      <p class="text-sm text-gray-600">
        Selecciona las categorías que ofreces y añade tus vehículos o servicios
      </p>
    </div>

    <!-- Loading state -->
    <div v-if="isLoading" class="flex justify-center items-center py-8">
      <BaseSpinner size="lg" color="primary" />
    </div>

    <!-- Error state -->
    <div v-else-if="errorMessage" class="text-center py-8">
      <p class="text-red-600 mb-4">{{ errorMessage }}</p>
      <BaseButton variant="outline" @click="loadCategorias">
        Reintentar
      </BaseButton>
    </div>

    <!-- Categories accordion -->
    <div v-else class="space-y-3 max-h-[600px] overflow-y-auto">
      <div
        v-for="categoria in rootCategories"
        :key="categoria.id"
        class="border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden bg-white dark:bg-gray-800"
      >
        <!-- Accordion Header -->
        <button
          @click="toggleAccordion(categoria.id)"
          class="w-full px-4 py-3 flex items-center justify-between hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
        >
          <div class="flex items-center gap-3">
            <svg
              class="w-5 h-5 text-gray-500 transition-transform"
              :class="{ 'rotate-90': openAccordions[categoria.id] }"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
            <span class="font-medium text-gray-900 dark:text-white">{{ categoria.nombre }}</span>
            <span
              v-if="getVehiclesCount(categoria.id) > 0"
              class="px-2 py-0.5 text-xs bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-400 rounded-full"
            >
              {{ getVehiclesCount(categoria.id) }}
            </span>
          </div>
          <svg
            v-if="openAccordions[categoria.id]"
            class="w-5 h-5 text-gray-400"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>

        <!-- Accordion Content -->
        <div
          v-if="openAccordions[categoria.id]"
          class="px-4 py-4 border-t border-gray-200 dark:border-gray-700 space-y-4"
        >
          <!-- Existing vehicle (only one per category) -->
          <div v-if="getVehiclesForCategory(categoria.id).length > 0" class="mb-4">
            <h4 class="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
              Vehículo/Servicio registrado:
            </h4>
            <div class="p-3 bg-gray-50 dark:bg-gray-700/50 rounded-lg border border-gray-200 dark:border-gray-600">
              <div class="flex items-start justify-between">
                <div class="flex-1">
                  <div class="font-medium text-gray-900 dark:text-white">
                    {{ getVehiclesForCategory(categoria.id)[0].nombre_vehiculo || categoria.nombre }}
                  </div>
                  <div class="mt-1 flex flex-wrap gap-2 text-xs text-gray-600 dark:text-gray-400">
                    <span v-if="getVehiclesForCategory(categoria.id)[0].marca">{{ getVehiclesForCategory(categoria.id)[0].marca }}</span>
                    <span v-if="getVehiclesForCategory(categoria.id)[0].tonelaje">{{ getVehiclesForCategory(categoria.id)[0].tonelaje }} t</span>
                    <span v-if="getVehiclesForCategory(categoria.id)[0].radio_km_especifico">{{ getVehiclesForCategory(categoria.id)[0].radio_km_especifico }} km</span>
                  </div>
                  <p v-if="getVehiclesForCategory(categoria.id)[0].caracteristicas" class="mt-2 text-xs text-gray-500 dark:text-gray-400 line-clamp-2">
                    {{ getVehiclesForCategory(categoria.id)[0].caracteristicas }}
                  </p>
                </div>
                <div class="flex gap-2 ml-4">
                  <button
                    @click="editVehicle(categoria.id, 0)"
                    class="p-1.5 text-gray-500 hover:text-primary-600 hover:bg-primary-50 dark:hover:bg-primary-900/20 rounded transition-colors"
                    title="Editar"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                    </svg>
                  </button>
                  <button
                    @click="removeVehicle(categoria.id, 0)"
                    class="p-1.5 text-gray-500 hover:text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 rounded transition-colors"
                    title="Eliminar"
                  >
                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>

          <!-- Add/Edit Form -->
          <div class="p-4 bg-gray-50 dark:bg-gray-700/30 rounded-lg border border-gray-200 dark:border-gray-600">
            <h4 class="text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3">
              {{ editingVehicle ? 'Editar vehículo' : 'Añadir nuevo vehículo/servicio' }}
            </h4>
            
            <form @submit.prevent="saveVehicle(categoria.id)" class="space-y-3">
              <!-- Nombre del vehículo -->
              <div>
                <label class="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Nombre del vehículo
                </label>
                <input
                  v-model="formData.nombre_vehiculo"
                  type="text"
                  placeholder="Ej: Mi Excavadora CAT"
                  class="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                />
              </div>

              <div class="grid grid-cols-2 gap-3">
                <!-- Marca -->
                <div>
                  <label class="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Marca
                  </label>
                  <input
                    v-model="formData.marca"
                    type="text"
                    placeholder="Ej: Caterpillar"
                    class="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  />
                </div>

                <!-- Tonelaje -->
                <div>
                  <label class="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-1">
                    Tonelaje / Capacidad
                  </label>
                  <input
                    v-model.number="formData.tonelaje"
                    type="number"
                    step="0.01"
                    min="0"
                    placeholder="Ej: 20"
                    class="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  />
                </div>
              </div>

              <!-- Radio específico -->
              <div>
                <label class="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Radio de actuación (km)
                </label>
                <input
                  v-model.number="formData.radio_km_especifico"
                  type="number"
                  min="1"
                  placeholder="Opcional - dejar vacío para usar radio general"
                  class="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                />
              </div>

              <!-- Características -->
              <div>
                <label class="block text-xs font-medium text-gray-700 dark:text-gray-300 mb-1">
                  Características
                </label>
                <textarea
                  v-model="formData.caracteristicas"
                  rows="2"
                  placeholder="Describe las características especiales..."
                  class="w-full px-3 py-2 text-sm border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
                />
              </div>

              <!-- Form Actions -->
              <div class="flex gap-2 pt-2">
                <BaseButton
                  v-if="editingVehicle"
                  type="button"
                  variant="outline"
                  size="sm"
                  @click="cancelEdit"
                  class="flex-1"
                >
                  Cancelar
                </BaseButton>
                <BaseButton
                  type="submit"
                  variant="primary"
                  size="sm"
                  class="flex-1"
                >
                  {{ editingVehicle ? 'Guardar cambios' : 'Añadir' }}
                </BaseButton>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Summary -->
    <div v-if="localData.categoria_ids.length > 0" class="pt-4 border-t border-gray-200 dark:border-gray-700">
      <p class="text-sm text-gray-600 dark:text-gray-400">
        <span class="font-semibold">{{ localData.categoria_ids.length }}</span>
        categoría{{ localData.categoria_ids.length !== 1 ? 's' : '' }}
        con
        <span class="font-semibold">{{ totalVehicles }}</span>
        vehículo{{ totalVehicles !== 1 ? 's' : '' }}
        registrado{{ totalVehicles !== 1 ? 's' : '' }}
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, computed, onMounted } from 'vue'
import { fetchCategorias } from '../../../api/transportistas'
import type { Categoria } from '../../../api/transportistas'
import BaseButton from '../../base/BaseButton.vue'
import BaseSpinner from '../../base/BaseSpinner.vue'

interface VehicleData {
  nombre_vehiculo: string | null
  marca: string | null
  tonelaje: number | null
  radio_km_especifico: number | null
  caracteristicas: string | null
}

interface WizardData {
  step1: {
    codigo_postal: string
  }
  step2: {
    categoria_ids: number[]
  }
  step3: {
    radio_km_general: number | null
    maquinaria_radios: Record<number, number | null>
    maquinaria_detalles: Record<number, VehicleData>
    // New: Store multiple vehicles per category
    maquinaria_vehicles: Record<number, VehicleData[]>
  }
  step4: {
    foto_de_perfil: File | null
    maquinaria_imagenes: Record<number, File | null>
  }
}

interface Props {
  modelValue: WizardData
}

const props = defineProps<Props>()

const emit = defineEmits<{
  'update:modelValue': [value: WizardData]
}>()

const localData = reactive({
  categoria_ids: [...props.modelValue.step2.categoria_ids],
})

const categorias = ref<Categoria[]>([])
const isLoading = ref(false)
const errorMessage = ref('')
const openAccordions = reactive<Record<number, boolean>>({})

// Form data for adding/editing vehicles
const formData = reactive<VehicleData & { editingCategoryId: number | null; editingIndex: number | null }>({
  nombre_vehiculo: '',
  marca: '',
  tonelaje: null,
  radio_km_especifico: null,
  caracteristicas: '',
  editingCategoryId: null,
  editingIndex: null,
})

const editingVehicle = computed(() => formData.editingCategoryId !== null && formData.editingIndex !== null)

// Get root categories (no parent)
const rootCategories = computed(() => {
  return categorias.value.filter(cat => cat.parent === null)
})

// Get vehicles for a specific category
function getVehiclesForCategory(categoriaId: number): VehicleData[] {
  const vehicles = props.modelValue.step3.maquinaria_vehicles?.[categoriaId] || []
  return vehicles
}

// Get count of vehicles for a category
function getVehiclesCount(categoriaId: number): number {
  return getVehiclesForCategory(categoriaId).length
}

// Total vehicles across all categories
const totalVehicles = computed(() => {
  const vehicles = props.modelValue.step3.maquinaria_vehicles || {}
  return Object.values(vehicles).reduce((sum, arr) => sum + arr.length, 0)
})

/**
 * Toggle accordion open/close
 */
function toggleAccordion(categoriaId: number) {
  openAccordions[categoriaId] = !openAccordions[categoriaId]
  
  // Reset form when opening
  if (openAccordions[categoriaId] && !editingVehicle.value) {
    resetForm()
  }
}

/**
 * Load categories from API
 */
async function loadCategorias() {
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
 * Reset form to empty state
 */
function resetForm() {
  formData.nombre_vehiculo = ''
  formData.marca = ''
  formData.tonelaje = null
  formData.radio_km_especifico = null
  formData.caracteristicas = ''
  formData.editingCategoryId = null
  formData.editingIndex = null
}

/**
 * Save vehicle (add or update)
 */
function saveVehicle(categoriaId: number) {
  const vehicleData: VehicleData = {
    nombre_vehiculo: formData.nombre_vehiculo || null,
    marca: formData.marca || null,
    tonelaje: formData.tonelaje,
    radio_km_especifico: formData.radio_km_especifico,
    caracteristicas: formData.caracteristicas || null,
  }

  // Initialize maquinaria_vehicles if it doesn't exist
  const currentVehicles = { ...(props.modelValue.step3.maquinaria_vehicles || {}) }
  
  if (!currentVehicles[categoriaId]) {
    currentVehicles[categoriaId] = []
  }

  if (editingVehicle.value && formData.editingCategoryId === categoriaId && formData.editingIndex !== null) {
    // Update existing vehicle
    currentVehicles[categoriaId][formData.editingIndex] = vehicleData
  } else {
    // Replace existing vehicle or add new (only one per category)
    if (currentVehicles[categoriaId].length > 0) {
      currentVehicles[categoriaId][0] = vehicleData
    } else {
      currentVehicles[categoriaId].push(vehicleData)
    }
  }

  // Ensure categoria is in categoria_ids
  const categoriaIds = [...localData.categoria_ids]
  if (!categoriaIds.includes(categoriaId)) {
    categoriaIds.push(categoriaId)
  }

  // Update wizard data
  const updatedStep3 = {
    ...props.modelValue.step3,
    maquinaria_vehicles: currentVehicles,
    // Also update legacy fields for backward compatibility
    maquinaria_radios: {
      ...props.modelValue.step3.maquinaria_radios,
      [categoriaId]: vehicleData.radio_km_especifico || props.modelValue.step3.maquinaria_radios[categoriaId] || null,
    },
    maquinaria_detalles: {
      ...props.modelValue.step3.maquinaria_detalles,
      [categoriaId]: vehicleData,
    },
  }

  emit('update:modelValue', {
    ...props.modelValue,
    step2: {
      categoria_ids: categoriaIds,
    },
    step3: updatedStep3,
  })

  resetForm()
}

/**
 * Edit vehicle
 */
function editVehicle(categoriaId: number, index: number) {
  const vehicles = getVehiclesForCategory(categoriaId)
  if (vehicles[index]) {
    const vehicle = vehicles[index]
    formData.nombre_vehiculo = vehicle.nombre_vehiculo || ''
    formData.marca = vehicle.marca || ''
    formData.tonelaje = vehicle.tonelaje
    formData.radio_km_especifico = vehicle.radio_km_especifico
    formData.caracteristicas = vehicle.caracteristicas || ''
    formData.editingCategoryId = categoriaId
    formData.editingIndex = index
    
    // Ensure accordion is open
    openAccordions[categoriaId] = true
  }
}

/**
 * Cancel editing
 */
function cancelEdit() {
  resetForm()
}

/**
 * Remove vehicle
 */
function removeVehicle(categoriaId: number, index: number) {
  const currentVehicles = { ...(props.modelValue.step3.maquinaria_vehicles || {}) }
  
  if (currentVehicles[categoriaId]) {
    currentVehicles[categoriaId].splice(index, 1)
    
    // If no vehicles left, remove category from categoria_ids
    if (currentVehicles[categoriaId].length === 0) {
      delete currentVehicles[categoriaId]
      const categoriaIds = localData.categoria_ids.filter(id => id !== categoriaId)
      localData.categoria_ids = categoriaIds
    }
  }

  // Clean up legacy fields
  const maquinaria_radios = { ...props.modelValue.step3.maquinaria_radios }
  const maquinaria_detalles = { ...props.modelValue.step3.maquinaria_detalles }
  
  if (currentVehicles[categoriaId]?.length === 0) {
    delete maquinaria_radios[categoriaId]
    delete maquinaria_detalles[categoriaId]
  } else if (currentVehicles[categoriaId]?.length > 0) {
    // Update with first vehicle's data for backward compatibility
    const firstVehicle = currentVehicles[categoriaId][0]
    maquinaria_radios[categoriaId] = firstVehicle.radio_km_especifico
    maquinaria_detalles[categoriaId] = firstVehicle
  }

  emit('update:modelValue', {
    ...props.modelValue,
    step2: {
      categoria_ids: [...localData.categoria_ids],
    },
    step3: {
      ...props.modelValue.step3,
      maquinaria_vehicles: currentVehicles,
      maquinaria_radios,
      maquinaria_detalles,
    },
  })

  // Reset form if we were editing this vehicle
  if (formData.editingCategoryId === categoriaId && formData.editingIndex === index) {
    resetForm()
  }
}

onMounted(() => {
  loadCategorias()
})
</script>
