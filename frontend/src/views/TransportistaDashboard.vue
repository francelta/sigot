<template>
  <div class="p-4 max-w-6xl mx-auto">
    <!-- Header -->
    <div class="mb-8">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">
        Panel de Control
      </h1>
      <p class="text-gray-600 dark:text-gray-300">
        Gestiona tus vehículos y servicios
      </p>
    </div>

    <!-- Stats Cards -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
      <div class="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
        <div class="text-3xl font-bold text-primary-600">{{ maquinaria.length }}</div>
        <div class="text-sm text-gray-500 dark:text-gray-400">Vehículos</div>
      </div>
      <div class="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
        <div class="text-3xl font-bold text-green-600">{{ disponible ? 'Sí' : 'No' }}</div>
        <div class="text-sm text-gray-500 dark:text-gray-400">Disponible</div>
      </div>
      <div class="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
        <div class="text-3xl font-bold text-obra-600">{{ radioKmGeneral || '-' }}</div>
        <div class="text-sm text-gray-500 dark:text-gray-400">Radio (km)</div>
      </div>
      <div class="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
        <div class="text-3xl font-bold text-blue-600">{{ codigoPostal || '-' }}</div>
        <div class="text-sm text-gray-500 dark:text-gray-400">Código Postal</div>
      </div>
    </div>

    <!-- Toggle Disponibilidad -->
    <div class="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700 mb-6">
      <div class="flex items-center justify-between">
        <div>
          <h3 class="font-semibold text-gray-900 dark:text-white">Estado de disponibilidad</h3>
          <p class="text-sm text-gray-500 dark:text-gray-400">
            {{ disponible ? 'Estás visible para los clientes' : 'No apareces en las búsquedas' }}
          </p>
        </div>
        <button
          @click="toggleDisponibilidad"
          :disabled="isTogglingDisponibilidad"
          class="relative inline-flex h-8 w-14 items-center rounded-full transition-colors"
          :class="disponible ? 'bg-green-500' : 'bg-gray-300 dark:bg-gray-600'"
        >
          <span
            class="inline-block h-6 w-6 transform rounded-full bg-white shadow-md transition-transform"
            :class="disponible ? 'translate-x-7' : 'translate-x-1'"
          />
        </button>
      </div>
    </div>

    <!-- Vehículos/Servicios Section -->
    <div class="mb-6">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-xl font-bold text-gray-900 dark:text-white">
          Mis Vehículos / Servicios
        </h2>
        <BaseButton variant="primary" size="sm" @click="openAddModal">
          <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4" />
          </svg>
          Añadir
        </BaseButton>
      </div>

      <!-- Loading -->
      <div v-if="isLoading" class="flex justify-center py-12">
        <BaseSpinner size="lg" color="primary" />
      </div>

      <!-- Error -->
      <div v-else-if="errorMessage" class="text-center py-8">
        <p class="text-red-600 mb-4">{{ errorMessage }}</p>
        <BaseButton variant="outline" @click="loadProfile">Reintentar</BaseButton>
      </div>

      <!-- Empty State -->
      <div v-else-if="maquinaria.length === 0" class="text-center py-12 bg-gray-50 dark:bg-gray-800/50 rounded-xl border-2 border-dashed border-gray-300 dark:border-gray-600">
        <svg class="w-16 h-16 mx-auto text-gray-400 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 17a2 2 0 11-4 0 2 2 0 014 0zM19 17a2 2 0 11-4 0 2 2 0 014 0z" />
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M13 16V6a1 1 0 00-1-1H4a1 1 0 00-1 1v10a1 1 0 001 1h1m8-1a1 1 0 01-1 1H9m4-1V8a1 1 0 011-1h2.586a1 1 0 01.707.293l3.414 3.414a1 1 0 01.293.707V16a1 1 0 01-1 1h-1m-6-1a1 1 0 001 1h1M5 17a2 2 0 104 0m-4 0a2 2 0 114 0m6 0a2 2 0 104 0m-4 0a2 2 0 114 0" />
        </svg>
        <h3 class="text-lg font-semibold text-gray-700 dark:text-gray-300 mb-2">No tienes vehículos registrados</h3>
        <p class="text-gray-500 dark:text-gray-400 mb-4">Añade tu primer vehículo o servicio para empezar a recibir solicitudes</p>
        <BaseButton variant="primary" @click="openAddModal">Añadir vehículo</BaseButton>
      </div>

      <!-- Vehicles List -->
      <div v-else class="grid gap-4">
        <div
          v-for="item in maquinaria"
          :key="item.categoria.id"
          class="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 p-4 hover:shadow-md transition-shadow"
        >
          <div class="flex items-start gap-4">
            <!-- Image -->
            <div class="w-20 h-20 bg-gray-100 dark:bg-gray-700 rounded-lg flex-shrink-0 overflow-hidden">
              <img
                v-if="item.imagen_maquina_url"
                :src="item.imagen_maquina_url"
                :alt="item.nombre_vehiculo || item.categoria.nombre"
                class="w-full h-full object-cover"
              />
              <div v-else class="w-full h-full flex items-center justify-center">
                <svg class="w-10 h-10 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M9 17a2 2 0 11-4 0 2 2 0 014 0zM19 17a2 2 0 11-4 0 2 2 0 014 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M13 16V6a1 1 0 00-1-1H4a1 1 0 00-1 1v10a1 1 0 001 1h1m8-1a1 1 0 01-1 1H9m4-1V8a1 1 0 011-1h2.586a1 1 0 01.707.293l3.414 3.414a1 1 0 01.293.707V16a1 1 0 01-1 1h-1m-6-1a1 1 0 001 1h1M5 17a2 2 0 104 0m-4 0a2 2 0 114 0m6 0a2 2 0 104 0m-4 0a2 2 0 114 0" />
                </svg>
              </div>
            </div>

            <!-- Info -->
            <div class="flex-1 min-w-0">
              <h3 class="font-semibold text-gray-900 dark:text-white truncate">
                {{ item.nombre_vehiculo || item.categoria.nombre }}
              </h3>
              <p class="text-sm text-primary-600 dark:text-primary-400">{{ item.categoria.nombre }}</p>
              <div class="flex flex-wrap gap-2 mt-2">
                <span v-if="item.marca" class="text-xs bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded">
                  {{ item.marca }}
                </span>
                <span v-if="item.tonelaje" class="text-xs bg-gray-100 dark:bg-gray-700 px-2 py-1 rounded">
                  {{ item.tonelaje }} t
                </span>
                <span v-if="item.radio_km_especifico" class="text-xs bg-obra-100 dark:bg-obra-900/30 text-obra-700 dark:text-obra-400 px-2 py-1 rounded">
                  {{ item.radio_km_especifico }} km
                </span>
              </div>
              <p v-if="item.caracteristicas" class="text-xs text-gray-500 dark:text-gray-400 mt-2 line-clamp-2">
                {{ item.caracteristicas }}
              </p>
            </div>

            <!-- Actions -->
            <div class="flex gap-2 flex-shrink-0">
              <button
                @click="editItem(item)"
                class="p-2 text-gray-500 hover:text-primary-600 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
                title="Editar"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
              </button>
              <button
                @click="confirmDelete(item)"
                class="p-2 text-gray-500 hover:text-red-600 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-lg transition-colors"
                title="Eliminar"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Add/Edit Modal -->
    <div
      v-if="showModal"
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50"
      @click.self="closeModal"
    >
      <div class="bg-white dark:bg-gray-800 rounded-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto">
        <div class="p-6 border-b border-gray-200 dark:border-gray-700">
          <h3 class="text-xl font-bold text-gray-900 dark:text-white">
            {{ editingItem ? 'Editar vehículo' : 'Añadir vehículo' }}
          </h3>
        </div>

        <form @submit.prevent="saveItem" class="p-6 space-y-4">
          <!-- Categoría -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Categoría *
            </label>
            <select
              v-model="formData.categoria_id"
              required
              :disabled="!!editingItem"
              class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent disabled:opacity-50"
            >
              <option value="">Selecciona una categoría</option>
              <option v-for="cat in availableCategories" :key="cat.id" :value="cat.id">
                {{ cat.nombre }}
              </option>
            </select>
          </div>

          <!-- Nombre del vehículo -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Nombre del vehículo
            </label>
            <input
              v-model="formData.nombre_vehiculo"
              type="text"
              placeholder="Ej: Mi Excavadora CAT"
              class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
          </div>

          <!-- Marca -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Marca
            </label>
            <input
              v-model="formData.marca"
              type="text"
              placeholder="Ej: Caterpillar, Volvo..."
              class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
          </div>

          <!-- Tonelaje -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Tonelaje / Capacidad
            </label>
            <input
              v-model.number="formData.tonelaje"
              type="number"
              step="0.01"
              min="0"
              placeholder="Ej: 20"
              class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
          </div>

          <!-- Radio específico -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Radio de actuación (km)
            </label>
            <input
              v-model.number="formData.radio_km_especifico"
              type="number"
              min="1"
              placeholder="Dejar vacío para usar radio general"
              class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
          </div>

          <!-- Características -->
          <div>
            <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Características
            </label>
            <textarea
              v-model="formData.caracteristicas"
              rows="3"
              placeholder="Describe las características especiales..."
              class="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent resize-none"
            />
          </div>

          <!-- Buttons -->
          <div class="flex gap-3 pt-4">
            <BaseButton type="button" variant="outline" class="flex-1" @click="closeModal">
              Cancelar
            </BaseButton>
            <BaseButton type="submit" variant="primary" class="flex-1" :disabled="isSaving">
              {{ isSaving ? 'Guardando...' : (editingItem ? 'Guardar cambios' : 'Añadir') }}
            </BaseButton>
          </div>
        </form>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div
      v-if="showDeleteModal"
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50"
      @click.self="showDeleteModal = false"
    >
      <div class="bg-white dark:bg-gray-800 rounded-2xl w-full max-w-md p-6">
        <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-2">
          ¿Eliminar vehículo?
        </h3>
        <p class="text-gray-600 dark:text-gray-300 mb-6">
          Esta acción no se puede deshacer. El vehículo "{{ deletingItem?.nombre_vehiculo || deletingItem?.categoria.nombre }}" será eliminado permanentemente.
        </p>
        <div class="flex gap-3">
          <BaseButton variant="outline" class="flex-1" @click="showDeleteModal = false">
            Cancelar
          </BaseButton>
          <BaseButton variant="primary" class="flex-1 !bg-red-600 hover:!bg-red-700" :disabled="isDeleting" @click="deleteItem">
            {{ isDeleting ? 'Eliminando...' : 'Eliminar' }}
          </BaseButton>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { getMiPerfil, fetchCategorias, updateMiPerfil } from '../api/transportistas'
import type { Transportista, Categoria, TransportistaCategoria } from '../api/transportistas'
import BaseButton from '../components/base/BaseButton.vue'
import BaseSpinner from '../components/base/BaseSpinner.vue'

const isLoading = ref(false)
const errorMessage = ref('')
const profile = ref<Transportista | null>(null)
const allCategories = ref<Categoria[]>([])

// Computed
const maquinaria = computed(() => profile.value?.maquinaria || [])
const disponible = computed(() => profile.value?.disponible || false)
const radioKmGeneral = computed(() => profile.value?.radio_km_general)
const codigoPostal = computed(() => profile.value?.codigo_postal)

// Modal state
const showModal = ref(false)
const editingItem = ref<TransportistaCategoria | null>(null)
const isSaving = ref(false)

const formData = ref({
  categoria_id: null as number | null,
  nombre_vehiculo: '',
  marca: '',
  tonelaje: null as number | null,
  radio_km_especifico: null as number | null,
  caracteristicas: '',
})

// Delete modal
const showDeleteModal = ref(false)
const deletingItem = ref<TransportistaCategoria | null>(null)
const isDeleting = ref(false)

// Disponibilidad toggle
const isTogglingDisponibilidad = ref(false)

// Available categories (not already added)
const availableCategories = computed(() => {
  const usedIds = new Set(maquinaria.value.map(m => m.categoria.id))
  // For editing, include the current category
  if (editingItem.value) {
    usedIds.delete(editingItem.value.categoria.id)
  }
  return allCategories.value.filter(c => !usedIds.has(c.id))
})

async function loadProfile() {
  isLoading.value = true
  errorMessage.value = ''

  try {
    const [profileData, categories] = await Promise.all([
      getMiPerfil(),
      fetchCategorias()
    ])
    profile.value = profileData
    allCategories.value = categories
  } catch (error) {
    console.error('Error loading profile:', error)
    errorMessage.value = 'Error al cargar el perfil. Por favor, intenta nuevamente.'
  } finally {
    isLoading.value = false
  }
}

async function toggleDisponibilidad() {
  if (!profile.value || isTogglingDisponibilidad.value) return

  isTogglingDisponibilidad.value = true
  try {
    await updateMiPerfil({ disponible: !profile.value.disponible })
    profile.value.disponible = !profile.value.disponible
  } catch (error) {
    console.error('Error toggling disponibilidad:', error)
    alert('Error al cambiar disponibilidad')
  } finally {
    isTogglingDisponibilidad.value = false
  }
}

function openAddModal() {
  editingItem.value = null
  formData.value = {
    categoria_id: null,
    nombre_vehiculo: '',
    marca: '',
    tonelaje: null,
    radio_km_especifico: null,
    caracteristicas: '',
  }
  showModal.value = true
}

function editItem(item: TransportistaCategoria) {
  editingItem.value = item
  formData.value = {
    categoria_id: item.categoria.id,
    nombre_vehiculo: item.nombre_vehiculo || '',
    marca: item.marca || '',
    tonelaje: item.tonelaje,
    radio_km_especifico: item.radio_km_especifico,
    caracteristicas: item.caracteristicas || '',
  }
  showModal.value = true
}

function closeModal() {
  showModal.value = false
  editingItem.value = null
}

async function saveItem() {
  if (!formData.value.categoria_id) return

  isSaving.value = true
  try {
    // Build maquinaria array
    const currentMaquinaria = [...maquinaria.value]
    const newItem = {
      categoria_id: formData.value.categoria_id,
      nombre_vehiculo: formData.value.nombre_vehiculo || null,
      marca: formData.value.marca || null,
      tonelaje: formData.value.tonelaje,
      radio_km_especifico: formData.value.radio_km_especifico,
      caracteristicas: formData.value.caracteristicas || null,
    }

    if (editingItem.value) {
      // Update existing
      const index = currentMaquinaria.findIndex(m => m.categoria.id === editingItem.value!.categoria.id)
      if (index !== -1) {
        currentMaquinaria[index] = {
          ...currentMaquinaria[index],
          nombre_vehiculo: newItem.nombre_vehiculo,
          marca: newItem.marca,
          tonelaje: newItem.tonelaje,
          radio_km_especifico: newItem.radio_km_especifico,
          caracteristicas: newItem.caracteristicas,
        }
      }
    } else {
      // Add new - need to find the category
      const cat = allCategories.value.find(c => c.id === newItem.categoria_id)
      if (cat) {
        currentMaquinaria.push({
          categoria: cat,
          nombre_vehiculo: newItem.nombre_vehiculo,
          marca: newItem.marca,
          tonelaje: newItem.tonelaje,
          radio_km_especifico: newItem.radio_km_especifico,
          caracteristicas: newItem.caracteristicas,
          imagen_maquina_url: null,
        } as TransportistaCategoria)
      }
    }

    // Send update to API
    await updateMiPerfil({
      maquinaria: currentMaquinaria.map(m => ({
        categoria_id: m.categoria.id,
        nombre_vehiculo: m.nombre_vehiculo,
        marca: m.marca,
        tonelaje: m.tonelaje,
        radio_km_especifico: m.radio_km_especifico,
        caracteristicas: m.caracteristicas,
      }))
    })

    // Reload profile
    await loadProfile()
    closeModal()
  } catch (error) {
    console.error('Error saving item:', error)
    alert('Error al guardar. Por favor, intenta nuevamente.')
  } finally {
    isSaving.value = false
  }
}

function confirmDelete(item: TransportistaCategoria) {
  deletingItem.value = item
  showDeleteModal.value = true
}

async function deleteItem() {
  if (!deletingItem.value) return

  isDeleting.value = true
  try {
    const currentMaquinaria = maquinaria.value.filter(
      m => m.categoria.id !== deletingItem.value!.categoria.id
    )

    await updateMiPerfil({
      maquinaria: currentMaquinaria.map(m => ({
        categoria_id: m.categoria.id,
        nombre_vehiculo: m.nombre_vehiculo,
        marca: m.marca,
        tonelaje: m.tonelaje,
        radio_km_especifico: m.radio_km_especifico,
        caracteristicas: m.caracteristicas,
      }))
    })

    await loadProfile()
    showDeleteModal.value = false
    deletingItem.value = null
  } catch (error) {
    console.error('Error deleting item:', error)
    alert('Error al eliminar. Por favor, intenta nuevamente.')
  } finally {
    isDeleting.value = false
  }
}

onMounted(() => {
  loadProfile()
})
</script>

