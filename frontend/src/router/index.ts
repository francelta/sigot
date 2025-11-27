import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/authStore'
import LoginView from '../views/LoginView.vue'
import RegisterView from '../views/RegisterView.vue'
import LandingPage from '../views/LandingPage.vue'
import AppLayout from '../layouts/AppLayout.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'landing',
      component: LandingPage,
      meta: { requiresAuth: false },
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
      meta: { requiresAuth: false },
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView,
      meta: { requiresAuth: false },
    },
    {
      path: '/onboarding/transportista',
      name: 'onboarding-transportista',
      component: () => import('../views/OnboardingWizardView.vue'),
      meta: { requiresAuth: true },
    },
    {
      path: '/app',
      component: AppLayout,
      meta: { requiresAuth: true },
      children: [
        {
          path: 'home',
          name: 'home',
          component: () => import('../views/HomeView.vue'),
        },
        {
          path: 'categoria/:id',
          name: 'category',
          component: () => import('../views/CategoryView.vue'),
        },
        {
          path: 'buscar/:subcategoria_id',
          name: 'search',
          component: () => import('../views/SearchView.vue'),
        },
        {
          path: 'results',
          name: 'results',
          component: () => import('../views/ResultsView.vue'),
        },
        {
          path: 'chats',
          name: 'chats',
          component: () => import('../views/ChatListView.vue'),
        },
        {
          path: 'chat/:id',
          name: 'chat-room',
          component: () => import('../views/ChatRoomView.vue'),
        },
      ],
    },
  ],
})

// Navigation guard
router.beforeEach((to, from, next) => {
  try {
    const authStore = useAuthStore()

    // Check authentication on app startup
    authStore.checkAuth()

    const isAuthenticated = authStore.isAuthenticated
    const requiresAuth = to.matched.some(record => record.meta.requiresAuth)

    // Public routes (login, register) - always allow access
    const publicRoutes = ['/login', '/register']
    const isPublicRoute = publicRoutes.includes(to.path)

    // Always allow access to public routes
    if (isPublicRoute) {
      next()
      return
    }

    // If user is not authenticated and trying to access protected route
    if (!isAuthenticated && requiresAuth) {
      next('/login')
      return
    }

    // Allow landing page access for everyone (authenticated or not)
    // Commented out: redirect authenticated users to home
    // if (isAuthenticated && to.path === '/') {
    //   next({ name: 'home' })
    //   return
    // }

    // Force onboarding for transportistas with incomplete profile
    if (
      isAuthenticated &&
      authStore.esTransportista &&
      !authStore.perfilCompleto &&
      to.path !== '/onboarding/transportista' &&
      !isPublicRoute
    ) {
      next('/onboarding/transportista')
      return
    }

    // Allow navigation
    next()
  } catch (error) {
    console.error('Router guard error:', error)
    // On error, allow navigation to prevent blocking
    next()
  }
})

export default router
