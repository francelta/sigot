<template>
  <div class="min-h-screen bg-white">
    <!-- Navigation -->
    <LandingNav />

    <!-- Hero Section -->
    <section class="pt-24 pb-16 px-4 sm:px-6 lg:px-8 bg-gradient-to-br from-gray-50 to-white">
      <div class="max-w-7xl mx-auto">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <!-- Left: Content -->
          <div class="text-center lg:text-left">
            <h1
              class="text-5xl md:text-6xl lg:text-7xl font-bold text-gray-900 mb-6 leading-tight"
            >
              Tu transporte,
              <span class="text-primary-500">cuando lo necesitas</span>
            </h1>
            <p class="text-xl md:text-2xl text-gray-600 mb-8 max-w-2xl mx-auto lg:mx-0">
              Conectamos clientes con transportistas profesionales en toda España.
              Búsqueda rápida, contacto directo, resultados garantizados.
            </p>

            <!-- CTA Buttons -->
            <div class="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
              <BaseButton
                variant="primary"
                size="lg"
                @click="$router.push({ name: 'login' })"
                class="min-w-[200px]"
              >
                Buscar un servicio
              </BaseButton>
              <BaseButton
                variant="outline"
                size="lg"
                @click="$router.push({ name: 'register' })"
                class="min-w-[200px]"
              >
                Registrarse como transportista
              </BaseButton>
            </div>
          </div>

          <!-- Right: Hero Image -->
          <div class="hidden lg:block">
            <div
              class="relative w-full h-[500px] rounded-2xl overflow-hidden shadow-sigot-lg"
            >
              <img
                src="/transporte.jpg"
                alt="Transporte de mercancías"
                class="w-full h-full object-cover"
              />
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Content Blocks -->
    <!-- Block 1: Encuentra cualquier servicio -->
    <section class="py-20 px-4 sm:px-6 lg:px-8 bg-white">
      <div class="max-w-7xl mx-auto">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <!-- Image -->
          <div class="order-2 lg:order-1">
            <div
              class="relative w-full h-[400px] rounded-2xl overflow-hidden shadow-sigot-lg"
            >
              <img
                src="/excavadora.jpg"
                alt="Maquinaria pesada y excavadoras"
                class="w-full h-full object-cover"
              />
            </div>
          </div>

          <!-- Content -->
          <div class="order-1 lg:order-2">
            <h2 class="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              Encuentra cualquier servicio
            </h2>
            <p class="text-lg text-gray-600 mb-6 leading-relaxed">
              Desde transporte de mercancías hasta maquinaria pesada. Nuestra plataforma
              conecta clientes con transportistas especializados en múltiples categorías.
              Búsqueda rápida, resultados precisos.
            </p>
            <ul class="space-y-4 mb-8">
              <li class="flex items-start gap-3">
                <svg
                  class="w-6 h-6 text-primary-500 flex-shrink-0 mt-0.5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M5 13l4 4L19 7"
                  />
                </svg>
                <span class="text-gray-700">
                  Búsqueda por categoría y ubicación
                </span>
              </li>
              <li class="flex items-start gap-3">
                <svg
                  class="w-6 h-6 text-primary-500 flex-shrink-0 mt-0.5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M5 13l4 4L19 7"
                  />
                </svg>
                <span class="text-gray-700">
                  Contacto directo con transportistas
                </span>
              </li>
              <li class="flex items-start gap-3">
                <svg
                  class="w-6 h-6 text-primary-500 flex-shrink-0 mt-0.5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M5 13l4 4L19 7"
                  />
                </svg>
                <span class="text-gray-700">
                  Transportistas verificados y valorados
                </span>
              </li>
            </ul>
            <BaseButton
              variant="primary"
              size="lg"
              @click="$router.push({ name: 'login' })"
            >
              Comenzar a buscar
            </BaseButton>
          </div>
        </div>
      </div>
    </section>

    <!-- Block 2: Controla tu negocio -->
    <section class="py-20 px-4 sm:px-6 lg:px-8 bg-gray-50">
      <div class="max-w-7xl mx-auto">
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <!-- Content -->
          <div>
            <h2 class="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              Controla tu negocio
            </h2>
            <p class="text-lg text-gray-600 mb-6 leading-relaxed">
              Si eres transportista, gestiona tu perfil, define tu zona de actuación y
              recibe solicitudes directamente. Herramientas profesionales para hacer
              crecer tu negocio.
            </p>
            <ul class="space-y-4 mb-8">
              <li class="flex items-start gap-3">
                <svg
                  class="w-6 h-6 text-primary-500 flex-shrink-0 mt-0.5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M5 13l4 4L19 7"
                  />
                </svg>
                <span class="text-gray-700">
                  Perfil completo con zona de actuación personalizada
                </span>
              </li>
              <li class="flex items-start gap-3">
                <svg
                  class="w-6 h-6 text-primary-500 flex-shrink-0 mt-0.5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M5 13l4 4L19 7"
                  />
                </svg>
                <span class="text-gray-700">
                  Chat directo con clientes potenciales
                </span>
              </li>
              <li class="flex items-start gap-3">
                <svg
                  class="w-6 h-6 text-primary-500 flex-shrink-0 mt-0.5"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M5 13l4 4L19 7"
                  />
                </svg>
                <span class="text-gray-700">
                  3 meses de prueba gratis para nuevos transportistas
                </span>
              </li>
            </ul>
            <BaseButton
              variant="primary"
              size="lg"
              @click="$router.push({ name: 'register' })"
            >
              Registrarse como transportista
            </BaseButton>
          </div>

          <!-- Image -->
          <div>
            <div
              class="relative w-full h-[400px] rounded-2xl overflow-hidden shadow-sigot-lg"
            >
              <img
                src="/tractor.jpg"
                alt="Gestión de negocio de transporte"
                class="w-full h-full object-cover"
              />
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Footer CTA Section -->
    <section class="py-20 px-4 sm:px-6 lg:px-8 bg-primary-500">
      <div class="max-w-4xl mx-auto text-center">
        <h2 class="text-4xl md:text-5xl font-bold text-white mb-6">
          ¿Listo para comenzar?
        </h2>
        <p class="text-xl text-primary-100 mb-8">
          Únete a SIGOT y descubre una nueva forma de conectar con servicios de
          transporte.
        </p>
        <div class="flex flex-col sm:flex-row gap-4 justify-center">
          <BaseButton
            variant="outline"
            size="lg"
            @click="$router.push({ name: 'register' })"
            class="bg-white border-white text-primary-500 hover:bg-primary-50 min-w-[200px]"
          >
            Crear cuenta gratis
          </BaseButton>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="bg-gray-900 text-gray-400 py-12 px-4 sm:px-6 lg:px-8">
      <div class="max-w-7xl mx-auto">
        <div class="flex flex-col md:flex-row justify-between items-center gap-4">
          <div class="flex items-center gap-2">
            <BaseLogo size="sm" variant="white" />
            <span class="text-sm">© 2024 SIGOT. Todos los derechos reservados.</span>
          </div>
          <div class="flex gap-6 text-sm">
            <a href="#" class="hover:text-white transition-colors">Términos</a>
            <a href="#" class="hover:text-white transition-colors">Privacidad</a>
            <a href="#" class="hover:text-white transition-colors">Ayuda</a>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import LandingNav from '../components/ui/LandingNav.vue'
import BaseLogo from '../components/base/BaseLogo.vue'
import BaseButton from '../components/base/BaseButton.vue'

const router = useRouter()
</script>
