<template>
  <div class="w-full">
    <label
      v-if="label"
      :for="inputId"
      class="block text-sm font-semibold text-gray-800 mb-2"
    >
      {{ label }}
      <span v-if="required" class="text-red-500 ml-1">*</span>
    </label>
    <div class="relative">
      <input
        :id="inputId"
        :type="type"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        :min="min"
        :max="max"
        :step="step"
        :class="[
          'w-full px-4 py-3 rounded-xl border-2 transition-all duration-200',
          'text-gray-900 placeholder-gray-400',
          'focus:outline-none focus:ring-4 focus:ring-primary-100 focus:border-primary-500',
          error
            ? 'border-red-400 bg-red-50 focus:border-red-500 focus:ring-red-100'
            : 'border-gray-200 bg-white hover:border-gray-300',
          disabled && 'bg-gray-50 cursor-not-allowed opacity-60 border-gray-200',
        ]"
        @input="
          $emit('update:modelValue', ($event.target as HTMLInputElement).value)
        "
        @blur="$emit('blur')"
        @focus="$emit('focus')"
      />
    </div>
    <p v-if="error" class="mt-1.5 text-sm font-medium text-red-600 flex items-center gap-1">
      <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
        <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
      </svg>
      {{ error }}
    </p>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  modelValue: string | number
  label?: string
  type?: 'text' | 'email' | 'password' | 'number' | 'tel'
  placeholder?: string
  error?: string
  disabled?: boolean
  required?: boolean
  min?: number | string
  max?: number | string
  step?: number | string
}

withDefaults(defineProps<Props>(), {
  type: 'text',
  disabled: false,
  required: false,
  label: undefined,
  placeholder: undefined,
  error: undefined,
  min: undefined,
  max: undefined,
  step: undefined,
})

defineEmits<{
  'update:modelValue': [value: string]
  blur: []
  focus: []
}>()

// Generate unique ID for label-input association
const inputId = computed(
  () => `input-${Math.random().toString(36).substr(2, 9)}`
)
</script>
