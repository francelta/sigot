<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <!-- Progress indicator -->
    <div class="bg-white border-b border-gray-200 px-4 py-4">
      <div class="max-w-2xl mx-auto">
        <div class="flex items-center justify-between mb-2">
          <h1 class="text-lg font-semibold text-gray-900">
            Configuración de Perfil
          </h1>
          <span class="text-sm text-gray-500">
            Paso {{ currentStep }} de {{ totalSteps }}
          </span>
        </div>
        <div class="w-full bg-gray-200 rounded-full h-2">
          <div
            class="bg-primary h-2 rounded-full transition-all duration-300"
            :style="{ width: `${(currentStep / totalSteps) * 100}%` }"
          />
        </div>
      </div>
    </div>

    <!-- Step content -->
    <div class="flex-1 overflow-y-auto">
      <div class="max-w-2xl mx-auto p-4">
        <BaseCard padding="lg" shadow="md">
          <component
            :is="currentStepComponent"
            v-model="wizardData"
            @update:model-value="wizardData = $event"
          />
        </BaseCard>
      </div>
    </div>

    <!-- Navigation buttons -->
    <div class="bg-white border-t border-gray-200 px-4 py-4">
      <div class="max-w-2xl mx-auto flex justify-between gap-4">
        <BaseButton
          v-if="currentStep > 1"
          variant="outline"
          @click="goToPreviousStep"
        >
          Atrás
        </BaseButton>
        <div v-else />

        <BaseButton
          v-if="currentStep < totalSteps"
          variant="primary"
          :disabled="!canProceed"
          @click="goToNextStep"
        >
          Siguiente
        </BaseButton>
        <BaseButton
          v-else
          variant="primary"
          :disabled="!canProceed || isSubmitting"
          @click="handleFinish"
        >
          <span v-if="!isSubmitting">Finalizar</span>
          <span v-else class="flex items-center">
            <BaseSpinner size="sm" color="white" class="mr-2" />
            Guardando...
          </span>
        </BaseButton>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, markRaw } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/authStore'
import { submitOnboardingWizard } from '../api/transportistas'
import type { WizardDataPayload } from '../api/transportistas'
import BaseCard from '../components/base/BaseCard.vue'
import BaseButton from '../components/base/BaseButton.vue'
import BaseSpinner from '../components/base/BaseSpinner.vue'
import Step1_CodigoPostal from '../components/ui/wizard/Step1_CodigoPostal.vue'
import Step2_Maquinaria from '../components/ui/wizard/Step2_Maquinaria.vue'
import Step3_Radios from '../components/ui/wizard/Step3_Radios.vue'
import Step4_Imagenes from '../components/ui/wizard/Step4_Imagenes.vue'

const router = useRouter()
const authStore = useAuthStore()

const totalSteps = 4
const currentStep = ref(1)
const isSubmitting = ref(false)

// Wizard data structure v3.0
const wizardData = ref({
  step1: {
    codigo_postal: '',
  },
  step2: {
    categoria_ids: [] as number[],
  },
  step3: {
    radio_km_general: null as number | null,
    maquinaria_radios: {} as Record<number, number | null>,
    maquinaria_detalles: {} as Record<number, {
      nombre_vehiculo: string | null
      marca: string | null
      tonelaje: number | null
      caracteristicas: string | null
    }>,
  },
  step4: {
    foto_de_perfil: null as File | null,
    maquinaria_imagenes: {} as Record<number, File | null>,
  },
})

// Step components
const stepComponents = [
  markRaw(Step1_CodigoPostal),
  markRaw(Step2_Maquinaria),
  markRaw(Step3_Radios),
  markRaw(Step4_Imagenes),
]

const currentStepComponent = computed(() => {
  return stepComponents[currentStep.value - 1]
})

/**
 * Check if current step is valid and can proceed
 */
const canProceed = computed(() => {
  switch (currentStep.value) {
    case 1:
      // Código postal: 5 dígitos
      const codigoPostalRegex = /^\d{5}$/
      return codigoPostalRegex.test(wizardData.value.step1.codigo_postal)
    case 2:
      // Al menos una máquina seleccionada
      return wizardData.value.step2.categoria_ids.length > 0
    case 3:
      // Al menos un radio definido (general o específico)
      const tieneRadioGeneral = wizardData.value.step3.radio_km_general !== null && wizardData.value.step3.radio_km_general > 0
      const tieneRadioEspecifico = Object.values(wizardData.value.step3.maquinaria_radios).some(
        radio => radio !== null && radio > 0
      )
      return tieneRadioGeneral || tieneRadioEspecifico
    case 4:
      // Paso 4 es opcional, siempre se puede proceder
      return true
    default:
      return false
  }
})

/**
 * Navigate to next step
 */
function goToNextStep() {
  if (currentStep.value < totalSteps) {
    currentStep.value++
  }
}

/**
 * Navigate to previous step
 */
function goToPreviousStep() {
  if (currentStep.value > 1) {
    currentStep.value--
  }
}

/**
 * Handle wizard completion v3.0
 * Uses the new transactional endpoint to submit all wizard data atomically
 */
async function handleFinish() {
  if (!canProceed.value) return

  isSubmitting.value = true

  try {
    // Build payload according to WizardDataPayload v3.0 interface
    const payload: WizardDataPayload = {
      codigo_postal: wizardData.value.step1.codigo_postal,
      maquinaria: wizardData.value.step2.categoria_ids.map(categoriaId => {
        const detalles = wizardData.value.step3.maquinaria_detalles[categoriaId] || {}
        return {
          categoria_id: categoriaId,
          radio_km_especifico: wizardData.value.step3.maquinaria_radios[categoriaId] || null,
          nombre_vehiculo: detalles.nombre_vehiculo || null,
          marca: detalles.marca || null,
          tonelaje: detalles.tonelaje || null,
          caracteristicas: detalles.caracteristicas || null,
          imagen: wizardData.value.step4.maquinaria_imagenes[categoriaId] || null,
        }
      }),
      radio_km_general: wizardData.value.step3.radio_km_general,
      foto_de_perfil: wizardData.value.step4.foto_de_perfil || null,
    }

    // Submit onboarding wizard data (transactional - all or nothing)
    const response = await submitOnboardingWizard(payload)

    // Update authStore with response data (backend returns updated user and transportista)
    if (response.user) {
      authStore.user = response.user
      localStorage.setItem('auth_user', JSON.stringify(response.user))
    }

    // Mark onboarding as complete
    authStore.markOnboardingComplete()

    // Redirect to chats
    router.push({ name: 'chats' })
  } catch (error) {
    console.error('Error completing onboarding:', error)
    // Show error message to user
    alert('Error al guardar el perfil. Por favor, intenta nuevamente.')
  } finally {
    isSubmitting.value = false
  }
}
</script>
