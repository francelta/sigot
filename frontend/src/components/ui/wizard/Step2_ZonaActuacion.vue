<template>
  <div class="space-y-6">
    <div>
      <h2 class="text-xl font-semibold text-gray-900 mb-2">
        Zona de Actuación
      </h2>
      <p class="text-sm text-gray-600">
        Define el área geográfica en la que operas
      </p>
    </div>

    <div>
      <label class="block text-sm font-medium text-gray-700 mb-3">
        Tipo de Zona
      </label>
      <div class="space-y-3">
        <div
          class="flex items-center justify-between p-3 border rounded-lg cursor-pointer transition-colors"
          :class="
            localData.tipo_zona === 'RADIO'
              ? 'border-primary bg-primary-50'
              : 'border-gray-300 hover:border-gray-400'
          "
          @click="localData.tipo_zona = 'RADIO'"
        >
          <span class="text-sm font-medium text-gray-700">
            Radio (kilómetros desde mi ubicación)
          </span>
          <div
            class="w-5 h-5 rounded-full border-2 flex items-center justify-center"
            :class="
              localData.tipo_zona === 'RADIO'
                ? 'border-primary bg-primary'
                : 'border-gray-300'
            "
          >
            <div
              v-if="localData.tipo_zona === 'RADIO'"
              class="w-3 h-3 rounded-full bg-white"
            />
          </div>
        </div>
        <div
          class="flex items-center justify-between p-3 border rounded-lg cursor-pointer transition-colors"
          :class="
            localData.tipo_zona === 'ZONAS'
              ? 'border-primary bg-primary-50'
              : 'border-gray-300 hover:border-gray-400'
          "
          @click="localData.tipo_zona = 'ZONAS'"
        >
          <span class="text-sm font-medium text-gray-700">
            Zonas (provincias, regiones, etc.)
          </span>
          <div
            class="w-5 h-5 rounded-full border-2 flex items-center justify-center"
            :class="
              localData.tipo_zona === 'ZONAS'
                ? 'border-primary bg-primary'
                : 'border-gray-300'
            "
          >
            <div
              v-if="localData.tipo_zona === 'ZONAS'"
              class="w-3 h-3 rounded-full bg-white"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- Radio mode -->
    <div v-if="localData.tipo_zona === 'RADIO'" class="space-y-4">
      <BaseInput
        v-model.number="localData.radio_km"
        label="Radio en Kilómetros"
        type="number"
        placeholder="Ej: 50"
        :error="errors.radio_km"
        :min="1"
        :step="1"
        required
      />
      <p class="text-xs text-gray-500">
        Indica el radio en kilómetros desde tu dirección empresarial (debe ser
        mayor que 0)
      </p>
    </div>

    <!-- Zonas mode -->
    <div v-if="localData.tipo_zona === 'ZONAS'" class="space-y-4">
      <BaseSelect
        v-model="localData.zona_tipo"
        label="Tipo de Zona"
        placeholder="Selecciona el tipo de zona"
        :options="zonaOptions"
        :error="errors.zona_tipo"
        required
      />
      <p class="text-xs text-gray-500">
        Selecciona el alcance geográfico de tus servicios
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, watch } from 'vue'
import BaseInput from '../../base/BaseInput.vue'
import BaseSelect from '../../base/BaseSelect.vue'
import type { SelectOption } from '../../base/BaseSelect.vue'

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
  tipo_zona: props.modelValue.step2.tipo_zona,
  radio_km: props.modelValue.step2.radio_km,
  zona_tipo: props.modelValue.step2.zona_tipo,
})

const errors = reactive({
  radio_km: '',
  zona_tipo: '',
})

const zonaOptions: SelectOption[] = [
  { value: 'MUNICIPAL', label: 'Municipal' },
  { value: 'PROVINCIAL', label: 'Provincial' },
  { value: 'VARIAS_PROVINCIAS', label: 'Varias Provincias' },
  { value: 'REGIONAL', label: 'Regional' },
  { value: 'NACIONAL', label: 'Nacional' },
  { value: 'INTERNACIONAL', label: 'Internacional' },
]

// Watch for tipo_zona changes to reset dependent fields and emit updates
watch(
  () => localData.tipo_zona,
  newValue => {
    // Clear dependent fields when switching types
    if (newValue === 'RADIO') {
      // Switching to RADIO: clear zona_tipo
      localData.zona_tipo = ''
      // Clear error for zona_tipo
      errors.zona_tipo = ''
      // Emit update with zona_tipo cleared
      emit('update:modelValue', {
        ...props.modelValue,
        step2: {
          ...props.modelValue.step2,
          tipo_zona: newValue,
          zona_tipo: '', // Explicitly clear zona_tipo
        },
      })
    } else if (newValue === 'ZONAS') {
      // Switching to ZONAS: clear radio_km
      localData.radio_km = null
      // Clear error for radio_km
      errors.radio_km = ''
      // Emit update with radio_km cleared
      emit('update:modelValue', {
        ...props.modelValue,
        step2: {
          ...props.modelValue.step2,
          tipo_zona: newValue,
          radio_km: null, // Explicitly clear radio_km
        },
      })
    }
  }
)

watch(
  () => localData.radio_km,
  newValue => {
    // Validate radio_km: must be a positive number
    if (newValue !== null && newValue !== undefined) {
      if (typeof newValue !== 'number' || isNaN(newValue)) {
        errors.radio_km = 'El radio debe ser un número válido'
      } else if (newValue <= 0) {
        errors.radio_km = 'El radio debe ser un número positivo mayor que 0'
      } else {
        errors.radio_km = ''
      }
    } else {
      errors.radio_km = ''
    }

    emit('update:modelValue', {
      ...props.modelValue,
      step2: {
        ...props.modelValue.step2,
        radio_km: newValue,
      },
    })
  }
)

watch(
  () => localData.zona_tipo,
  newValue => {
    errors.zona_tipo = ''
    emit('update:modelValue', {
      ...props.modelValue,
      step2: {
        ...props.modelValue.step2,
        zona_tipo: newValue,
      },
    })
  }
)
</script>
