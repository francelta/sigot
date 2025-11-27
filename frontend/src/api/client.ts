import axios, {
  type AxiosInstance,
  type InternalAxiosRequestConfig,
} from 'axios'

/**
 * Determine the API base URL:
 * - Production: Uses VITE_API_URL environment variable
 * - Development: Falls back to localhost
 */
const getBaseURL = (): string => {
  const envUrl = import.meta.env.VITE_API_URL
  return envUrl || 'http://localhost:8000/api'
}

/**
 * Centralized Axios client for API requests
 * Configured with base URL and interceptors for authentication
 */
const client: AxiosInstance = axios.create({
  baseURL: getBaseURL(),
  headers: {
    'Content-Type': 'application/json',
  },
})

/**
 * Request interceptor: Adds JWT token to Authorization header
 * Token is read from localStorage to avoid circular dependency with authStore
 */
client.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    const token = localStorage.getItem('auth_token')
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`
      console.log('[API Client] Adding token to request:', token.substring(0, 20) + '...')
    } else {
      console.warn('[API Client] No token found in localStorage')
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

/**
 * Response interceptor: Handles 401 errors and forces logout
 * Uses dynamic import to avoid circular dependency with authStore
 */
client.interceptors.response.use(
  response => {
    return response
  },
  async error => {
    if (error.response?.status === 401) {
      console.warn('[API Client] 401 Unauthorized - clearing auth and redirecting to login')
      // Clear token from localStorage
      localStorage.removeItem('auth_token')
      localStorage.removeItem('auth_user')
      localStorage.removeItem('auth_refresh')

      // Dynamically import authStore to avoid circular dependency
      const { useAuthStore } = await import('../stores/authStore')
      const authStore = useAuthStore()
      authStore.logout()
      
      // Redirect to login if we're in the browser
      if (typeof window !== 'undefined') {
        const { default: router } = await import('../router')
        router.push('/login')
      }
    }

    // Return error response for handling by calling code
    return Promise.reject(error)
  }
)

export default client
