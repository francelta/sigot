<template>
  <nav
    class="fixed top-0 left-0 right-0 z-50 bg-primary-500 border-b border-primary-700 transition-all duration-200"
    :class="{
      'shadow-md': isScrolled,
    }"
  >
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        <!-- Logo -->
        <div class="flex-shrink-0">
          <BaseLogo size="md" variant="primary" />
        </div>

        <!-- Desktop Navigation -->
        <div class="hidden md:flex items-center gap-4">
          <!-- Theme Toggle -->
          <button
            @click="themeStore.toggleTheme()"
            class="p-2 rounded-lg text-white hover:bg-primary-600 transition-colors"
            :title="themeStore.isDark ? 'Cambiar a modo claro' : 'Cambiar a modo oscuro'"
          >
            <!-- Sun icon (for dark mode) -->
            <svg
              v-if="themeStore.isDark"
              class="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"
              />
            </svg>
            <!-- Moon icon (for light mode) -->
            <svg
              v-else
              class="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"
              />
            </svg>
          </button>

          <template v-if="!isAuthenticated">
            <BaseButton
              variant="ghost"
              class="!text-white hover:bg-primary-600"
              style="color: white !important;"
              @click="$router.push({ name: 'login' })"
            >
              Iniciar Sesión
            </BaseButton>
            <BaseButton
              variant="primary"
              class="bg-white text-yellow-500 hover:bg-gray-100"
              @click="$router.push({ name: 'register' })"
            >
              Registrarse
            </BaseButton>
          </template>
          <template v-else>
            <!-- Trial countdown for transportistas -->
            <div
              v-if="esTransportista && trialTimeRemaining"
              class="flex items-center gap-2 px-3 py-1.5 bg-obra-500/20 rounded-lg border border-obra-400/30"
            >
              <svg
                class="w-4 h-4 text-obra-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
              <span class="text-xs font-semibold text-obra-400">
                {{ trialTimeRemaining }}
              </span>
            </div>
            <BaseButton
              variant="ghost"
              class="!text-white hover:bg-primary-600"
              style="color: white !important;"
              @click="handleLogout"
            >
              Cerrar Sesión
            </BaseButton>
          </template>
        </div>

        <!-- Mobile Menu Button -->
        <div class="md:hidden">
          <button
            @click="mobileMenuOpen = !mobileMenuOpen"
            class="p-2 rounded-lg text-white hover:bg-primary-600 transition-colors"
            aria-label="Toggle menu"
          >
            <svg
              v-if="!mobileMenuOpen"
              class="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 6h16M4 12h16M4 18h16"
              />
            </svg>
            <svg
              v-else
              class="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>
      </div>

      <!-- Mobile Menu -->
      <div
        v-if="mobileMenuOpen"
        class="md:hidden pb-4 border-t border-primary-700 mt-2 pt-4"
      >
        <div class="flex flex-col gap-2">
          <!-- Theme Toggle Mobile -->
          <button
            @click="themeStore.toggleTheme()"
            class="flex items-center gap-2 px-4 py-2 text-white hover:bg-primary-600 rounded-lg w-full text-left"
          >
            <svg
              v-if="themeStore.isDark"
              class="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M12 3v1m0 16v1m9-9h-1M4 12H3m15.364 6.364l-.707-.707M6.343 6.343l-.707-.707m12.728 0l-.707.707M6.343 17.657l-.707.707M16 12a4 4 0 11-8 0 4 4 0 018 0z"
              />
            </svg>
            <svg
              v-else
              class="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M20.354 15.354A9 9 0 018.646 3.646 9.003 9.003 0 0012 21a9.003 9.003 0 008.354-5.646z"
              />
            </svg>
            <span>{{ themeStore.isDark ? 'Modo Claro' : 'Modo Oscuro' }}</span>
          </button>

          <template v-if="!isAuthenticated">
            <BaseButton
              variant="ghost"
              class="w-full justify-start !text-white hover:bg-primary-600"
              style="color: white !important;"
              @click="handleNavClick('login')"
            >
              Iniciar Sesión
            </BaseButton>
            <BaseButton
              variant="primary"
              class="w-full justify-start bg-white text-yellow-500 hover:bg-gray-100"
              @click="handleNavClick('register')"
            >
              Registrarse
            </BaseButton>
          </template>
          <template v-else>
            <!-- Trial countdown for transportistas (mobile) -->
            <div
              v-if="esTransportista && trialTimeRemaining"
              class="flex items-center gap-2 px-3 py-2 bg-obra-500/20 rounded-lg border border-obra-400/30 mb-2"
            >
              <svg
                class="w-4 h-4 text-obra-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
              <span class="text-xs font-semibold text-obra-400">
                {{ trialTimeRemaining }}
              </span>
            </div>
            <BaseButton
              variant="ghost"
              class="w-full justify-start !text-white hover:bg-primary-600"
              style="color: white !important;"
              @click="handleLogout"
            >
              Cerrar Sesión
            </BaseButton>
          </template>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/authStore'
import { useThemeStore } from '../../stores/themeStore'
import { getMiPerfil } from '../../api/transportistas'
import type { Transportista } from '../../api/transportistas'
import BaseLogo from '../base/BaseLogo.vue'
import BaseButton from '../base/BaseButton.vue'

const router = useRouter()
const authStore = useAuthStore()
const themeStore = useThemeStore()
const isScrolled = ref(false)
const mobileMenuOpen = ref(false)

const isAuthenticated = computed(() => authStore.isAuthenticated)
const esTransportista = computed(() => authStore.esTransportista)

const transportistaProfile = ref<Transportista | null>(null)
const trialTimeRemaining = ref<string>('')
let trialIntervalId: number | null = null

/**
 * Calculate time remaining until trial_end
 */
function calculateTrialTimeRemaining(): string {
  if (!transportistaProfile.value?.trial_end) {
    return ''
  }

  const now = new Date()
  const trialEnd = new Date(transportistaProfile.value.trial_end)
  const diffMs = trialEnd.getTime() - now.getTime()

  if (diffMs <= 0) {
    return 'Trial expirado'
  }

  const days = Math.floor(diffMs / (1000 * 60 * 60 * 24))
  const hours = Math.floor((diffMs % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60))
  const minutes = Math.floor((diffMs % (1000 * 60 * 60)) / (1000 * 60))

  if (days > 0) {
    return `${days}d ${hours}h`
  } else if (hours > 0) {
    return `${hours}h ${minutes}m`
  } else {
    return `${minutes}m`
  }
}

/**
 * Update trial time remaining
 */
function updateTrialTime() {
  trialTimeRemaining.value = calculateTrialTimeRemaining()
}

/**
 * Load transportista profile
 */
async function loadTransportistaProfile() {
  if (!esTransportista.value) return

  try {
    transportistaProfile.value = await getMiPerfil()
    updateTrialTime()
    
    // Update every minute
    trialIntervalId = window.setInterval(() => {
      updateTrialTime()
    }, 60000) // Update every minute
  } catch (error) {
    console.error('Error loading transportista profile:', error)
  }
}

function handleScroll() {
  isScrolled.value = window.scrollY > 10
}

function handleNavClick(routeName: string) {
  mobileMenuOpen.value = false
  router.push({ name: routeName })
}

async function handleLogout() {
  mobileMenuOpen.value = false
  await authStore.logout()
  router.push({ name: 'landing' })
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
  handleScroll() // Check initial state
  themeStore.initTheme()
  
  // Load transportista profile if user is transportista
  if (esTransportista.value) {
    loadTransportistaProfile()
  }
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
  if (trialIntervalId !== null) {
    clearInterval(trialIntervalId)
  }
})

onBeforeUnmount(() => {
  if (trialIntervalId !== null) {
    clearInterval(trialIntervalId)
  }
})
</script>

