<template>
  <div class="space-y-6">
    <div>
      <h2 class="text-xl font-semibold text-gray-900 mb-2">
        Radio de Actuación
      </h2>
      <p class="text-sm text-gray-600">
        Define el radio de actuación general y opcionalmente por máquina
      </p>
    </div>

    <!-- Radio General -->
    <div class="space-y-4">
      <BaseInput
        v-model.number="localData.radio_km_general"
        label="Radio General (km)"
        type="number"
        placeholder="100"
        :error="errors.radio_km_general"
        min="1"
        @update:model-value="handleUpdate"
      />
      <p class="text-xs text-gray-500">
        Este radio se usará para todas las máquinas que no tengan un radio específico
      </p>
    </div>

    <!-- Detalles por Máquina -->
    <div v-if="selectedCategorias.length > 0" class="space-y-6 pt-4 border-t">
      <h3 class="text-lg font-semibold text-gray-900">
        Detalles de tus Vehículos/Máquinas
      </h3>
      <p class="text-sm text-gray-600 mb-4">
        Completa la información de cada vehículo o máquina que has seleccionado.
      </p>

      <div
        v-for="categoria in selectedCategorias"
        :key="categoria.id"
        class="space-y-4 p-4 border border-gray-200 rounded-lg bg-gray-50"
      >
        <h4 class="font-semibold text-gray-900">{{ categoria.nombre }}</h4>
        
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Radio Específico -->
          <BaseInput
            v-model.number="localData.maquinaria_radios[categoria.id]"
            label="Radio de actuación (km)"
            type="number"
            placeholder="Dejar vacío para usar radio general"
            min="1"
            @update:model-value="handleUpdate"
          />
          
          <!-- Nombre del Vehículo -->
          <BaseInput
            v-model="localData.maquinaria_detalles[categoria.id].nombre_vehiculo"
            label="Nombre del vehículo"
            type="text"
            placeholder="Ej: Mi Furgoneta Mercedes"
            @update:model-value="handleUpdate"
          />
          
          <!-- Marca -->
          <BaseInput
            v-model="localData.maquinaria_detalles[categoria.id].marca"
            label="Marca"
            type="text"
            placeholder="Ej: Mercedes, Volvo, Caterpillar"
            @update:model-value="handleUpdate"
          />
          
          <!-- Tonelaje -->
          <BaseInput
            v-model.number="localData.maquinaria_detalles[categoria.id].tonelaje"
            label="Tonelaje"
            type="number"
            placeholder="Ej: 3.5, 7.5, 20"
            step="0.01"
            min="0"
            @update:model-value="handleUpdate"
          />
        </div>
        
        <!-- Características -->
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">
            Características
          </label>
          <textarea
            v-model="localData.maquinaria_detalles[categoria.id].caracteristicas"
            class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
            rows="3"
            placeholder="Descripción detallada de características especiales..."
            @input="handleUpdate"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, computed, watch, ref } from 'vue'
import { fetchCategorias } from '../../../api/transportistas'
import type { Categoria } from '../../../api/transportistas'
import BaseInput from '../../base/BaseInput.vue'

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
    maquinaria_detalles: Record<number, {
      nombre_vehiculo: string | null
      marca: string | null
      tonelaje: number | null
      caracteristicas: string | null
    }>
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
  radio_km_general: props.modelValue.step3.radio_km_general,
  maquinaria_radios: { ...props.modelValue.step3.maquinaria_radios },
  maquinaria_detalles: { ...props.modelValue.step3.maquinaria_detalles },
})

const categorias = ref<Categoria[]>([])
const errors = reactive({
  radio_km_general: '',
})

// Obtener las categorías seleccionadas
const selectedCategorias = computed(() => {
  const selectedIds = props.modelValue.step2.categoria_ids
  return categorias.value.filter(cat => selectedIds.includes(cat.id))
})

// Cargar categorías para mostrar nombres
async function loadCategorias() {
  try {
    const data = await fetchCategorias()
    categorias.value = data
  } catch (error) {
    console.error('Error loading categories:', error)
  }
}

// Inicializar maquinaria_radios y detalles cuando cambian las categorías seleccionadas
watch(
  () => props.modelValue.step2.categoria_ids,
  (newIds) => {
    // Limpiar radios y detalles de categorías que ya no están seleccionadas
    const currentIds = Object.keys(localData.maquinaria_radios).map(Number)
    currentIds.forEach(id => {
      if (!newIds.includes(id)) {
        delete localData.maquinaria_radios[id]
        delete localData.maquinaria_detalles[id]
      }
    })
    
    // Inicializar detalles para nuevas categorías
    newIds.forEach(id => {
      if (!localData.maquinaria_detalles[id]) {
        localData.maquinaria_detalles[id] = {
          nombre_vehiculo: null,
          marca: null,
          tonelaje: null,
          caracteristicas: null,
        }
      }
    })
    
    handleUpdate()
  },
  { immediate: true }
)

function handleUpdate() {
  // Validar radio general
  if (localData.radio_km_general !== null && localData.radio_km_general <= 0) {
    errors.radio_km_general = 'El radio debe ser mayor a 0'
  } else {
    errors.radio_km_general = ''
  }

  emit('update:modelValue', {
    ...props.modelValue,
    step3: {
      radio_km_general: localData.radio_km_general,
      maquinaria_radios: { ...localData.maquinaria_radios },
      maquinaria_detalles: { ...localData.maquinaria_detalles },
    },
  })
}

// Cargar categorías al montar
loadCategorias()
</script>

