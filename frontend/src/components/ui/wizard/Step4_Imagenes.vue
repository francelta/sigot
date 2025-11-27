<template>
  <div class="space-y-6">
    <div>
      <h2 class="text-xl font-semibold text-gray-900 mb-2">
        Imágenes (Opcional)
      </h2>
      <p class="text-sm text-gray-600">
        Sube una foto de perfil y opcionalmente imágenes de tus máquinas
      </p>
    </div>

    <!-- Foto de Perfil -->
    <div class="space-y-4">
      <label class="block text-sm font-medium text-gray-700">
        Foto de Perfil
      </label>
      <div class="flex items-center gap-4">
        <input
          ref="fotoPerfilInput"
          type="file"
          accept="image/*"
          class="hidden"
          @change="handleFotoPerfilChange"
        />
        <BaseButton
          variant="outline"
          @click="fotoPerfilInput?.click()"
        >
          {{ localData.foto_de_perfil ? 'Cambiar Foto' : 'Seleccionar Foto' }}
        </BaseButton>
        <span v-if="localData.foto_de_perfil" class="text-sm text-gray-600">
          {{ localData.foto_de_perfil.name }}
        </span>
        <BaseButton
          v-if="localData.foto_de_perfil"
          variant="ghost"
          size="sm"
          @click="localData.foto_de_perfil = null; handleUpdate()"
        >
          Eliminar
        </BaseButton>
      </div>
      <div v-if="fotoPreview" class="mt-2">
        <img
          :src="fotoPreview"
          alt="Preview foto de perfil"
          class="w-32 h-32 object-cover rounded-lg border border-gray-200"
        />
      </div>
    </div>

    <!-- Imágenes de Máquinas -->
    <div v-if="selectedCategorias.length > 0" class="space-y-4 pt-4 border-t">
      <h3 class="text-lg font-semibold text-gray-900">
        Imágenes de Máquinas (Opcional)
      </h3>

      <div
        v-for="categoria in selectedCategorias"
        :key="categoria.id"
        class="space-y-2"
      >
        <label class="block text-sm font-medium text-gray-700">
          Imagen para {{ categoria.nombre }}
        </label>
        <div class="flex items-center gap-4">
          <input
            :ref="el => setFileInputRef(el, categoria.id)"
            type="file"
            accept="image/*"
            class="hidden"
            @change="(e) => handleMaquinaImagenChange(e, categoria.id)"
          />
          <BaseButton
            variant="outline"
            size="sm"
            @click="fileInputRefs[categoria.id]?.click()"
          >
            {{ localData.maquinaria_imagenes[categoria.id] ? 'Cambiar' : 'Seleccionar' }}
          </BaseButton>
          <span
            v-if="localData.maquinaria_imagenes[categoria.id]"
            class="text-sm text-gray-600"
          >
            {{ localData.maquinaria_imagenes[categoria.id]?.name }}
          </span>
          <BaseButton
            v-if="localData.maquinaria_imagenes[categoria.id]"
            variant="ghost"
            size="sm"
            @click="delete localData.maquinaria_imagenes[categoria.id]; handleUpdate()"
          >
            Eliminar
          </BaseButton>
        </div>
        <div v-if="maquinaPreviews[categoria.id]" class="mt-2">
          <img
            :src="maquinaPreviews[categoria.id]"
            :alt="`Preview ${categoria.nombre}`"
            class="w-32 h-32 object-cover rounded-lg border border-gray-200"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref, computed, watch } from 'vue'
import { fetchCategorias } from '../../../api/transportistas'
import type { Categoria } from '../../../api/transportistas'
import BaseButton from '../../base/BaseButton.vue'

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
  foto_de_perfil: props.modelValue.step4.foto_de_perfil,
  maquinaria_imagenes: { ...props.modelValue.step4.maquinaria_imagenes },
})

const categorias = ref<Categoria[]>([])
const fotoPerfilInput = ref<HTMLInputElement | null>(null)
const fileInputRefs = ref<Record<number, HTMLInputElement | null>>({})
const fotoPreview = ref<string | null>(null)
const maquinaPreviews = ref<Record<number, string>>({})

// Obtener las categorías seleccionadas
const selectedCategorias = computed(() => {
  const selectedIds = props.modelValue.step2.categoria_ids
  return categorias.value.filter(cat => selectedIds.includes(cat.id))
})

function setFileInputRef(el: any, categoriaId: number) {
  if (el) {
    fileInputRefs.value[categoriaId] = el
  }
}

function handleFotoPerfilChange(event: Event) {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (file) {
    localData.foto_de_perfil = file
    // Crear preview
    const reader = new FileReader()
    reader.onload = (e) => {
      fotoPreview.value = e.target?.result as string
    }
    reader.readAsDataURL(file)
    handleUpdate()
  }
}

function handleMaquinaImagenChange(event: Event, categoriaId: number) {
  const target = event.target as HTMLInputElement
  const file = target.files?.[0]
  if (file) {
    localData.maquinaria_imagenes[categoriaId] = file
    // Crear preview
    const reader = new FileReader()
    reader.onload = (e) => {
      maquinaPreviews.value[categoriaId] = e.target?.result as string
    }
    reader.readAsDataURL(file)
    handleUpdate()
  }
}

// Cargar categorías para mostrar nombres
async function loadCategorias() {
  try {
    const data = await fetchCategorias()
    categorias.value = data
  } catch (error) {
    console.error('Error loading categories:', error)
  }
}

// Limpiar imágenes de categorías que ya no están seleccionadas
watch(
  () => props.modelValue.step2.categoria_ids,
  (newIds) => {
    const currentIds = Object.keys(localData.maquinaria_imagenes).map(Number)
    currentIds.forEach(id => {
      if (!newIds.includes(id)) {
        delete localData.maquinaria_imagenes[id]
        delete maquinaPreviews.value[id]
      }
    })
    handleUpdate()
  },
  { immediate: true }
)

function handleUpdate() {
  emit('update:modelValue', {
    ...props.modelValue,
    step4: {
      foto_de_perfil: localData.foto_de_perfil,
      maquinaria_imagenes: { ...localData.maquinaria_imagenes },
    },
  })
}

// Cargar categorías al montar
loadCategorias()
</script>


