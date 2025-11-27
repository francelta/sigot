<template>
  <div class="flex flex-col items-center justify-center py-12 px-4 text-center">
    <!-- Icon slot (customizable) -->
    <div
      v-if="$slots.icon"
      class="mb-4 text-gray-400"
    >
      <slot name="icon" />
    </div>
    <!-- Default icon if no slot provided -->
    <div
      v-else
      class="mb-4 w-16 h-16 rounded-full bg-gray-100 flex items-center justify-center"
    >
      <svg
        class="w-8 h-8 text-gray-400"
        fill="none"
        stroke="currentColor"
        viewBox="0 0 24 24"
      >
        <path
          stroke-linecap="round"
          stroke-linejoin="round"
          stroke-width="2"
          d="M9.172 16.172a4 4 0 015.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
        />
      </svg>
    </div>

    <!-- Title -->
    <h3
      v-if="title"
      class="text-lg font-semibold text-gray-900 mb-2"
    >
      {{ title }}
    </h3>

    <!-- Message -->
    <p
      v-if="message"
      class="text-sm text-gray-600 max-w-md mb-6"
    >
      {{ message }}
    </p>

    <!-- Default message if none provided -->
    <p
      v-else
      class="text-sm text-gray-600 max-w-md mb-6"
    >
      Ups, no tenemos servicio en esta zona para esa categoría.
    </p>

    <!-- Action slot (optional button) -->
    <div v-if="$slots.action">
      <slot name="action" />
    </div>
  </div>
</template>

<script setup lang="ts">
interface Props {
  title?: string
  message?: string
}

withDefaults(defineProps<Props>(), {
  title: undefined,
  message: undefined,
})
</script>


