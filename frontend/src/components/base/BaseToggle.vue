<template>
  <label
    :for="toggleId"
    :class="[
      'relative inline-flex items-center cursor-pointer',
      disabled && 'opacity-50 cursor-not-allowed',
    ]"
  >
    <input
      :id="toggleId"
      type="checkbox"
      :checked="props.modelValue"
      :disabled="props.disabled"
      class="sr-only peer"
      @change="handleChange"
    />
    <div
      :class="[
        'w-11 h-6 rounded-full transition-colors duration-200',
        'peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-200 peer-focus:ring-offset-2',
        props.modelValue ? 'bg-primary-500 shadow-sm' : 'bg-gray-300',
      ]"
    >
      <div
        :class="[
          'absolute top-0.5 left-0.5 w-5 h-5 rounded-full bg-white transition-transform duration-200',
          'shadow-sm',
          props.modelValue ? 'translate-x-5' : 'translate-x-0',
        ]"
      />
    </div>
    <span v-if="props.label" class="ml-3 text-sm text-gray-700">{{
      props.label
    }}</span>
  </label>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  modelValue: boolean
  label?: string
  disabled?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  disabled: false,
  label: undefined,
})

const emit = defineEmits<{
  'update:modelValue': [value: boolean]
}>()

const toggleId = computed(
  () => `toggle-${Math.random().toString(36).substr(2, 9)}`
)

function handleChange(event: Event) {
  const target = event.target as HTMLInputElement
  emit('update:modelValue', target.checked)
}
</script>
