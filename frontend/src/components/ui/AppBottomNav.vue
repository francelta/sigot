<template>
  <nav
    class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 z-50"
  >
    <div class="flex justify-around items-center h-16">
      <RouterLink
        :to="{ name: 'home' }"
        class="flex flex-col items-center justify-center flex-1 h-full text-gray-600 hover:text-primary transition-colors"
        active-class="text-primary"
      >
        <svg
          class="w-6 h-6 mb-1"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
          />
        </svg>
        <span class="text-xs font-medium">Buscar</span>
      </RouterLink>

      <RouterLink
        :to="{ name: 'chats' }"
        class="flex flex-col items-center justify-center flex-1 h-full text-gray-600 hover:text-primary transition-colors"
        active-class="text-primary"
      >
        <svg
          class="w-6 h-6 mb-1"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z"
          />
        </svg>
        <span class="text-xs font-medium">Chats</span>
      </RouterLink>
    </div>
  </nav>
</template>

<script setup lang="ts">
// Component for bottom navigation bar
</script>
