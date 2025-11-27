<template>
  <div
    :class="[
      'rounded-full flex items-center justify-center font-semibold text-white',
      'bg-primary overflow-hidden',
      sizeClasses,
    ]"
  >
    <img
      v-if="src"
      :src="src"
      :alt="alt || 'Avatar'"
      class="w-full h-full object-cover"
    />
    <span v-else class="select-none">
      {{ initials }}
    </span>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  src?: string
  alt?: string
  name?: string
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl'
}

const props = withDefaults(defineProps<Props>(), {
  size: 'md',
  src: undefined,
  alt: undefined,
  name: undefined,
})

const sizeClasses = computed(() => {
  switch (props.size) {
    case 'xs':
      return 'w-6 h-6 text-xs'
    case 'sm':
      return 'w-8 h-8 text-sm'
    case 'md':
      return 'w-10 h-10 text-base'
    case 'lg':
      return 'w-12 h-12 text-lg'
    case 'xl':
      return 'w-16 h-16 text-xl'
    default:
      return 'w-10 h-10 text-base'
  }
})

const initials = computed(() => {
  if (!props.name) return '?'

  const parts = props.name.trim().split(/\s+/)
  if (parts.length >= 2) {
    return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase()
  }
  return parts[0][0].toUpperCase()
})
</script>
