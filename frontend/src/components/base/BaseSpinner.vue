<template>
  <div
    :class="[
      'inline-block animate-spin rounded-full border-solid border-t-transparent',
      sizeClasses,
      colorClasses,
    ]"
    role="status"
    aria-label="Loading"
  >
    <span class="sr-only">Loading...</span>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl'
  color?: 'primary' | 'white' | 'gray' | 'yellow'
}

const props = withDefaults(defineProps<Props>(), {
  size: 'md',
  color: 'primary',
})

const sizeClasses = computed(() => {
  switch (props.size) {
    case 'xs':
      return 'w-3 h-3 border'
    case 'sm':
      return 'w-4 h-4 border'
    case 'md':
      return 'w-6 h-6 border-2'
    case 'lg':
      return 'w-8 h-8 border-2'
    case 'xl':
      return 'w-12 h-12 border-4'
    default:
      return 'w-6 h-6 border-2'
  }
})

const colorClasses = computed(() => {
  switch (props.color) {
    case 'primary':
      return 'border-primary'
    case 'white':
      return 'border-white'
    case 'gray':
      return 'border-gray-400'
    case 'yellow':
      return 'border-yellow-600'
    default:
      return 'border-primary'
  }
})
</script>
