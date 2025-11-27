import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User } from '../api/types'
import { loginUser, registerUser } from '../api/auth'
import type { LoginPayload, RegisterPayload } from '../api/types'

/**
 * Authentication store (Pinia)
 * Manages user authentication state, token, and auth-related actions
 */
export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<User | null>(null)
  const token = ref<string | null>(null)

  // Getters
  const isAuthenticated = computed(() => {
    return token.value !== null && user.value !== null
  })

  const esTransportista = computed(() => {
    return user.value?.is_transportista ?? false
  })

  const perfilCompleto = computed(() => {
    if (!user.value || !user.value.is_transportista) return true
    // For transportistas, check if they have completed onboarding
    // This is a simple check - in production, you'd check the actual transportista profile
    // For now, we'll use a flag in localStorage
    const onboardingComplete = localStorage.getItem(
      'transportista_onboarding_complete'
    )
    return onboardingComplete === 'true'
  })

  // Actions
  /**
   * Login user with credentials
   * @param payload - Login credentials
   */
  async function login(payload: LoginPayload): Promise<void> {
    const response = await loginUser(payload)

    // Store token and user
    token.value = response.access
    user.value = response.user

    // Persist to localStorage
    localStorage.setItem('auth_token', response.access)
    if (response.refresh) {
      localStorage.setItem('auth_refresh', response.refresh)
    }
    localStorage.setItem('auth_user', JSON.stringify(response.user))
    
    // Note: We don't clear onboarding flag on login because the backend should tell us
    // if the transportista has completed onboarding. For now, we rely on localStorage.
    // TODO: Check backend transportista profile to determine if onboarding is complete
  }

  /**
   * Register new user
   * @param payload - Registration data
   */
  async function register(payload: RegisterPayload): Promise<void> {
    const response = await registerUser(payload)

    // Store token and user
    token.value = response.access
    user.value = response.user

    // Persist to localStorage
    localStorage.setItem('auth_token', response.access)
    if (response.refresh) {
      localStorage.setItem('auth_refresh', response.refresh)
    }
    localStorage.setItem('auth_user', JSON.stringify(response.user))
    
    // If user is a transportista, clear onboarding flag (new transportista needs to complete onboarding)
    if (response.user.is_transportista) {
      localStorage.removeItem('transportista_onboarding_complete')
    }
  }

  /**
   * Logout user
   * Clears state and localStorage, redirects to login
   */
  function logout(): void {
    // Clear state
    user.value = null
    token.value = null

    // Clear localStorage
    localStorage.removeItem('auth_token')
    localStorage.removeItem('auth_refresh')
    localStorage.removeItem('auth_user')

    // Redirect to login (router will be available when router is set up)
    // For now, we'll just clear the state
    // Router redirect will be handled by the component using this store
  }

  /**
   * Check authentication on app startup
   * Loads token and user from localStorage if available
   */
  function checkAuth(): void {
    const storedToken = localStorage.getItem('auth_token')
    const storedUser = localStorage.getItem('auth_user')

    if (storedToken && storedUser) {
      try {
        token.value = storedToken
        user.value = JSON.parse(storedUser) as User
      } catch (error) {
        // If parsing fails, clear corrupted data
        console.error('Error parsing stored user data:', error)
        logout()
      }
    }
  }

  /**
   * Mark transportista onboarding as complete
   */
  function markOnboardingComplete(): void {
    localStorage.setItem('transportista_onboarding_complete', 'true')
  }

  return {
    // State
    user,
    token,
    // Getters
    isAuthenticated,
    esTransportista,
    perfilCompleto,
    // Actions
    login,
    register,
    logout,
    checkAuth,
    markOnboardingComplete,
  }
})
