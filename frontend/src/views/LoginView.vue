<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 via-white to-primary-100 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 px-4 py-12">
    <BaseCard class="w-full max-w-md" padding="lg" shadow="lg">
      <div class="flex justify-center mb-6 bg-primary-500 -m-6 p-6 rounded-t-2xl">
        <BaseLogo size="xl" variant="primary" />
      </div>
      <h1 class="text-2xl font-bold text-gray-900 dark:text-white mb-2 text-center">
        Iniciar Sesión
      </h1>
      <p class="text-sm text-gray-600 dark:text-gray-300 text-center mb-6">
        Accede a tu cuenta para continuar
      </p>

      <form class="space-y-4" @submit.prevent="handleLogin">
        <BaseInput
          v-model="form.username"
          label="Usuario"
          type="text"
          placeholder="Ingresa tu usuario"
          :error="errors.username"
          required
        />

        <BaseInput
          v-model="form.password"
          label="Contraseña"
          type="password"
          placeholder="Ingresa tu contraseña"
          :error="errors.password"
          required
        />

        <div v-if="errorMessage" class="text-sm text-red-600 text-center">
          {{ errorMessage }}
        </div>

        <BaseButton
          type="submit"
          variant="primary"
          :disabled="isLoading"
          class="w-full"
        >
          <span v-if="!isLoading">Iniciar Sesión</span>
          <span v-else class="flex items-center justify-center">
            <BaseSpinner size="sm" color="white" class="mr-2" />
            Cargando...
          </span>
        </BaseButton>
      </form>

      <div class="mt-6 text-center">
        <p class="text-sm text-gray-600 dark:text-gray-300">
          ¿No tienes cuenta?
          <RouterLink
            to="/register"
            class="text-primary font-semibold hover:underline"
          >
            Regístrate
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
import BaseSpinner from '../components/base/BaseSpinner.vue'
import BaseLogo from '../components/base/BaseLogo.vue'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({
  username: '',
  password: '',
})

const errors = reactive({
  username: '',
  password: '',
})

const errorMessage = ref('')
const isLoading = ref(false)

async function handleLogin() {
  // Reset errors
  errors.username = ''
  errors.password = ''
  errorMessage.value = ''

  // Basic validation
  if (!form.username.trim()) {
    errors.username = 'El usuario es requerido'
    return
  }

  if (!form.password) {
    errors.password = 'La contraseña es requerida'
    return
  }

  isLoading.value = true

  try {
    await authStore.login({
      username: form.username.trim(),
      password: form.password,
    })

    // Redirect to home on success
    router.push({ name: 'home' })
  } catch (error: unknown) {
    // Handle error
    if (error && typeof error === 'object' && 'response' in error) {
      const axiosError = error as { response?: { data?: { message?: string } } }
      errorMessage.value =
        axiosError.response?.data?.message ||
        'Error al iniciar sesión. Verifica tus credenciales.'
    } else {
      errorMessage.value = 'Error al iniciar sesión. Intenta nuevamente.'
    }
  } finally {
    isLoading.value = false
  }
}
</script>
