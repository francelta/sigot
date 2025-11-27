<template>
  <div class="pl-4">
    <BaseCheckbox
      :model-value="isSelected"
      :label="categoria.nombre"
      @update:model-value="handleToggle"
    />
    <p v-if="categoria.descripcion" class="text-xs text-gray-500 ml-7 mb-2">
      {{ categoria.descripcion }}
    </p>

    <!-- Recursive children -->
    <div
      v-if="categoria.children && categoria.children.length > 0"
      class="ml-6 mt-2"
    >
      <CategoryTree
        v-for="child in categoria.children"
        :key="child.id"
        :categoria="child"
        :selected-ids="selectedIds"
        @toggle="(id, selected) => $emit('toggle', id, selected)"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { Categoria } from '../../../api/transportistas'
import BaseCheckbox from '../../base/BaseCheckbox.vue'

interface Props {
  categoria: Categoria
  selectedIds: number[]
}

const props = defineProps<Props>()

const emit = defineEmits<{
  toggle: [categoriaId: number, isSelected: boolean]
}>()

const isSelected = computed(() => {
  return props.selectedIds.includes(props.categoria.id)
})

function handleToggle(value: boolean) {
  emit('toggle', props.categoria.id, value)
}
</script>
