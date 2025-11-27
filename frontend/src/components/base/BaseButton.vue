<template>
  <button
    :type="type"
    :disabled="disabled"
    :class="[
      'inline-flex items-center justify-center gap-2',
      sizeClasses,
      'rounded-xl font-semibold',
      'transition-all duration-200 ease-in-out',
      'focus:outline-none focus:ring-4 focus:ring-offset-2',
      'disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:transform-none disabled:hover:shadow-none',
      variantClasses,
    ]"
    @click="$emit('click', $event)"
  >
    <slot />
  </button>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost'
  type?: 'button' | 'submit' | 'reset'
  disabled?: boolean
  size?: 'sm' | 'md' | 'lg'
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'primary',
  type: 'button',
  disabled: false,
  size: 'md',
})

defineEmits<{
  click: [event: MouseEvent]
}>()

const sizeClasses = computed(() => {
  switch (props.size) {
    case 'sm':
      return 'px-4 py-2 text-xs'
    case 'md':
      return 'px-6 py-3 text-sm'
    case 'lg':
      return 'px-8 py-4 text-base'
    default:
      return 'px-6 py-3 text-sm'
  }
})

const variantClasses = computed(() => {
  const base = 'transform hover:scale-[1.01] active:scale-[0.99]'

  switch (props.variant) {
    case 'primary':
      return [
        base,
        'bg-primary-500 text-white',
        'hover:bg-primary-600 active:bg-primary-700',
        'focus:ring-primary-200',
        'shadow-sigot hover:shadow-sigot-lg',
      ].join(' ')
    case 'secondary':
      return [
        base,
        'bg-secondary-500 text-white',
        'hover:bg-secondary-600 active:bg-secondary-700',
        'focus:ring-secondary-200',
        'shadow-sigot hover:shadow-sigot-lg',
      ].join(' ')
    case 'outline':
      return [
        base,
        'bg-white border-2 border-primary-500 text-primary-500',
        'hover:bg-primary-50 active:bg-primary-100',
        'focus:ring-primary-200',
      ].join(' ')
    case 'ghost':
      return [
        base,
        'bg-transparent text-primary-500',
        'hover:bg-primary-50 active:bg-primary-100',
        'focus:ring-primary-200',
      ].join(' ')
    default:
      return base
  }
})
</script>
