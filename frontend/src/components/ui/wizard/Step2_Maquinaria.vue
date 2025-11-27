<template>
  <div class="space-y-6">
    <div>
      <h2 class="text-xl font-semibold text-gray-900 mb-2">
        Maquinaria Disponible
      </h2>
      <p class="text-sm text-gray-600">
        Selecciona las máquinas que tienes disponibles
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

    <!-- Categories tree -->
    <div v-else class="space-y-2 max-h-96 overflow-y-auto">
      <CategoryTree
        v-for="categoria in categorias"
        :key="categoria.id"
        :categoria="categoria"
        :selected-ids="localData.categoria_ids"
        @toggle="
          (id: number, selected: boolean) => handleToggleCategory(id, selected)
        "
      />
    </div>

    <div v-if="localData.categoria_ids.length > 0" class="pt-4 border-t">
      <p class="text-sm text-gray-600">
        <span class="font-semibold">{{ localData.categoria_ids.length }}</span>
        máquina{{ localData.categoria_ids.length !== 1 ? 's' : '' }}
        seleccionada{{ localData.categoria_ids.length !== 1 ? 's' : '' }}
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted } from 'vue'
import { fetchCategorias } from '../../../api/transportistas'
import type { Categoria } from '../../../api/transportistas'
import BaseButton from '../../base/BaseButton.vue'
import BaseSpinner from '../../base/BaseSpinner.vue'
import CategoryTree from './CategoryTree.vue'

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
 * Handle category toggle
 */
function handleToggleCategory(categoriaId: number, isSelected: boolean) {
  if (isSelected) {
    if (!localData.categoria_ids.includes(categoriaId)) {
      localData.categoria_ids.push(categoriaId)
    }
  } else {
    const index = localData.categoria_ids.indexOf(categoriaId)
    if (index > -1) {
      localData.categoria_ids.splice(index, 1)
    }
  }

  emit('update:modelValue', {
    ...props.modelValue,
    step2: {
      categoria_ids: [...localData.categoria_ids],
    },
  })
}

onMounted(() => {
  loadCategorias()
})
</script>


