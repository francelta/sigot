<template>
  <div
    :class="[
      'rounded-2xl bg-white dark:bg-gray-800 transition-shadow duration-200',
      paddingClasses,
      shadowClasses,
    ]"
  >
    <slot />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  padding?: 'none' | 'sm' | 'md' | 'lg' | 'xl'
  shadow?: 'none' | 'sm' | 'md' | 'lg'
}

const props = withDefaults(defineProps<Props>(), {
  padding: 'md',
  shadow: 'md',
})

const paddingClasses = computed(() => {
  switch (props.padding) {
    case 'none':
      return ''
    case 'sm':
      return 'p-3'
    case 'md':
      return 'p-4'
    case 'lg':
      return 'p-6'
    case 'xl':
      return 'p-8'
    default:
      return 'p-4'
  }
})

const shadowClasses = computed(() => {
  switch (props.shadow) {
    case 'none':
      return ''
    case 'sm':
      return 'shadow-sigot'
    case 'md':
      return 'shadow-sigot-lg'
    case 'lg':
      return 'shadow-2xl'
    default:
      return 'shadow-sigot-lg'
  }
})
</script>
