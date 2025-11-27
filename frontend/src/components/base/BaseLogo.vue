<template>
  <div
    :class="[
      'inline-flex items-center justify-center',
      sizeClasses,
    ]"
  >
    <!-- Texto SIGOT - El logo es solo el texto -->
    <span
      :class="[
        'font-saviko',
        textSizeClasses,
      ]"
      :style="{
        fontFamily: 'Saviko Sans, sans-serif',
        fontWeight: 700,
        letterSpacing: '0.08em',
      }"
    >
      <span class="text-white">Si</span>
      <span class="text-yellow-500">GO</span>
      <span class="text-white">t</span>
    </span>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  size?: 'xs' | 'sm' | 'md' | 'lg' | 'xl'
  variant?: 'primary' | 'white' | 'dark'
}

const props = withDefaults(defineProps<Props>(), {
  size: 'md',
  variant: 'primary',
})

// Container size classes
const sizeClasses = computed(() => {
  return ''
})

// Text size classes (25% más grandes que el doble)
const textSizeClasses = computed(() => {
  switch (props.size) {
    case 'xs':
      return 'text-3xl' // 2xl * 1.25 ≈ 3xl
    case 'sm':
      return 'text-4xl' // 3xl * 1.25 ≈ 4xl
    case 'md':
      return 'text-5xl' // 4xl * 1.25 = 5xl
    case 'lg':
      return 'text-7xl' // 6xl * 1.25 ≈ 7xl
    case 'xl':
      return 'text-9xl' // 8xl * 1.25 = 10xl, pero 9xl es el máximo
    default:
      return 'text-5xl'
  }
})

</script>

