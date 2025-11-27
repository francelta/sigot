<template>
  <div class="space-y-6">
    <div>
      <h2 class="text-xl font-semibold text-gray-900 mb-2">
        Datos de tu Negocio
      </h2>
      <p class="text-sm text-gray-600">
        Proporciona la información básica de tu empresa de transporte
      </p>
    </div>

    <BaseInput
      v-model="localData.phone"
      label="Teléfono"
      type="tel"
      placeholder="+34 612 345 678"
      :error="errors.phone"
      required
    />

    <BaseInput
      v-model="localData.direccion_empresarial"
      label="Dirección Empresarial"
      type="text"
      placeholder="Calle, número, ciudad, código postal"
      :error="errors.direccion_empresarial"
      required
    />
  </div>
</template>

<script setup lang="ts">
import { reactive, watch } from 'vue'
import BaseInput from '../../base/BaseInput.vue'

interface WizardData {
  step1: {
    phone: string
    direccion_empresarial: string
  }
  step2: {
    tipo_zona: 'RADIO' | 'ZONAS'
    radio_km: number | null
    zona_tipo: string
  }
  step3: {
    categoria_ids: number[]
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
  phone: props.modelValue.step1.phone,
  direccion_empresarial: props.modelValue.step1.direccion_empresarial,
})

const errors = reactive({
  phone: '',
  direccion_empresarial: '',
})

// Watch for changes and emit updates
watch(
  () => localData.phone,
  newValue => {
    errors.phone = ''
    emit('update:modelValue', {
      ...props.modelValue,
      step1: {
        ...props.modelValue.step1,
        phone: newValue,
      },
    })
  }
)

watch(
  () => localData.direccion_empresarial,
  newValue => {
    errors.direccion_empresarial = ''
    emit('update:modelValue', {
      ...props.modelValue,
      step1: {
        ...props.modelValue.step1,
        direccion_empresarial: newValue,
      },
    })
  }
)
</script>

