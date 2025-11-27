<template>
  <div class="space-y-6">
    <div>
      <h2 class="text-xl font-semibold text-gray-900 mb-2">
        Código Postal
      </h2>
      <p class="text-sm text-gray-600">
        Ingresa tu código postal para geocodificar tu base de actuación
      </p>
    </div>

    <BaseInput
      v-model="localData.codigo_postal"
      label="Código Postal"
      type="text"
      placeholder="28001"
      :error="errors.codigo_postal"
      required
      @update:model-value="handleUpdate"
    />
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
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
  codigo_postal: props.modelValue.step1.codigo_postal || '',
})

const errors = reactive({
  codigo_postal: '',
})

function handleUpdate() {
  // Validar código postal (formato español: 5 dígitos)
  const codigoPostalRegex = /^\d{5}$/
  if (localData.codigo_postal && !codigoPostalRegex.test(localData.codigo_postal)) {
    errors.codigo_postal = 'El código postal debe tener 5 dígitos'
  } else {
    errors.codigo_postal = ''
  }

  emit('update:modelValue', {
    ...props.modelValue,
    step1: {
      codigo_postal: localData.codigo_postal,
    },
  })
}
</script>


