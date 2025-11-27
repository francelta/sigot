<template>
  <label
    :for="checkboxId"
    :class="[
      'flex items-center cursor-pointer select-none',
      disabled && 'opacity-50 cursor-not-allowed',
    ]"
  >
    <div class="relative">
      <input
        :id="checkboxId"
        type="checkbox"
        :checked="modelValue"
        :disabled="disabled"
        class="sr-only"
        @change="handleChange"
      />
      <div
        :class="[
          'w-5 h-5 rounded-md border-2 transition-all duration-200',
          'flex items-center justify-center',
          modelValue ? 'bg-primary-500 border-primary-500 shadow-sm' : 'bg-white border-gray-300',
          !disabled && 'hover:border-primary-400',
        ]"
      >
        <svg
          v-if="modelValue"
          class="w-3 h-3 text-white"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="3"
            d="M5 13l4 4L19 7"
          />
        </svg>
      </div>
    </div>
    <span v-if="label" class="ml-2 text-sm text-gray-700">{{ label }}</span>
  </label>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  modelValue: boolean
  label?: string
  disabled?: boolean
}

withDefaults(defineProps<Props>(), {
  disabled: false,
  label: undefined,
})

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
}>()

const checkboxId = computed(
  () => `checkbox-${Math.random().toString(36).substr(2, 9)}`
)

function handleChange(event: Event) {
  const target = event.target as HTMLInputElement
  emit('update:modelValue', target.checked)
}
</script>
