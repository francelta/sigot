<template>
  <div
    class="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 via-white to-primary-100 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 px-4 py-8"
  >
    <BaseCard class="w-full max-w-md" padding="lg" shadow="lg">
      <div class="flex justify-center mb-6 bg-primary-500 -m-6 p-6 rounded-t-2xl">
        <BaseLogo size="xl" variant="primary" />
      </div>
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white mb-2 text-center">
        Crear Cuenta
      </h1>
      <p class="text-sm text-gray-600 dark:text-gray-300 text-center mb-6">
        Únete a SIGOT y comienza a buscar transportistas
      </p>

      <form class="space-y-4" @submit.prevent="handleRegister">
        <BaseInput
          v-model="form.username"
          label="Usuario"
          type="text"
          placeholder="Elige un nombre de usuario"
          :error="errors.username"
          required
        />

        <BaseInput
          v-model="form.email"
          label="Email"
          type="email"
          placeholder="tu@email.com"
          :error="errors.email"
          required
        />

        <BaseInput
          v-model="form.password"
          label="Contraseña"
          type="password"
          placeholder="Mínimo 8 caracteres"
          :error="errors.password"
          required
        />

        <BaseInput
          v-model="form.phone"
          label="Teléfono (opcional)"
          type="tel"
          placeholder="+34 612 345 678"
          :error="errors.phone"
        />

        <div class="py-2">
          <BaseToggle
            v-model="form.is_transportista"
            label="Soy Transportista"
          />
          <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
            Al registrarte como transportista, obtendrás 3 meses de prueba
            gratis
          </p>
        </div>

        <div v-if="errorMessage" class="text-sm text-red-600 text-center">
          {{ errorMessage }}
        </div>

        <BaseButton
          type="submit"
          variant="primary"
          :disabled="isLoading"
          class="w-full"
        >
          <span v-if="!isLoading">Crear Cuenta</span>
          <span v-else class="flex items-center justify-center">
            <BaseSpinner size="sm" color="white" class="mr-2" />
            Creando...
          </span>
        </BaseButton>
      </form>

      <div class="mt-6 text-center">
        <p class="text-sm text-gray-600 dark:text-gray-300">
          ¿Ya tienes cuenta?
          <RouterLink
            to="/login"
            class="text-primary font-semibold hover:underline"
          >
            Inicia Sesión
          </RouterLink>
        </p>
      </div>
    </BaseCard>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import { useAuthStore } from '../stores/authStore'
import BaseCard from '../components/base/BaseCard.vue'
import BaseInput from '../components/base/BaseInput.vue'
import BaseButton from '../components/base/BaseButton.vue'
import BaseToggle from '../components/base/BaseToggle.vue'
import BaseSpinner from '../components/base/BaseSpinner.vue'
import BaseLogo from '../components/base/BaseLogo.vue'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({
  username: '',
  email: '',
  password: '',
  phone: '',
  is_transportista: false,
})

const errors = reactive({
  username: '',
  email: '',
  password: '',
  phone: '',
})

const errorMessage = ref('')
const isLoading = ref(false)

function validateForm(): boolean {
  let isValid = true

  // Reset errors
  Object.keys(errors).forEach(key => {
    errors[key as keyof typeof errors] = ''
  })
  errorMessage.value = ''

  // Validate username
  if (!form.username.trim()) {
    errors.username = 'El usuario es requerido'
    isValid = false
  } else if (form.username.trim().length < 3) {
    errors.username = 'El usuario debe tener al menos 3 caracteres'
    isValid = false
  }

  // Validate email
  if (!form.email.trim()) {
    errors.email = 'El email es requerido'
    isValid = false
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
    errors.email = 'El email no es válido'
    isValid = false
  }

  // Validate password
  if (!form.password) {
    errors.password = 'La contraseña es requerida'
    isValid = false
  } else if (form.password.length < 8) {
    errors.password = 'La contraseña debe tener al menos 8 caracteres'
    isValid = false
  }

  return isValid
}

async function handleRegister() {
  if (!validateForm()) {
    return
  }

  isLoading.value = true

  try {
    await authStore.register({
      username: form.username.trim(),
      email: form.email.trim(),
      password: form.password,
      phone: form.phone.trim() || null,
      is_transportista: form.is_transportista,
    })

    // Redirect based on user type
    if (form.is_transportista) {
      // Transportistas go to onboarding wizard
      router.push({ name: 'onboarding-transportista' })
    } else {
      // Regular users go to home
      router.push({ name: 'home' })
    }
  } catch (error: unknown) {
    // Handle error
    if (error && typeof error === 'object' && 'response' in error) {
      const axiosError = error as { response?: { data?: { message?: string } } }
      errorMessage.value =
        axiosError.response?.data?.message ||
        'Error al crear la cuenta. Intenta nuevamente.'
    } else {
      errorMessage.value = 'Error al crear la cuenta. Intenta nuevamente.'
    }
  } finally {
    isLoading.value = false
  }
}
</script>
