<template>
  <span :class="['inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-bold uppercase tracking-wide shadow-sm', statusClasses]">
    <span class="w-1.5 h-1.5 rounded-full" :class="dotClass"></span>
    <slot></slot>
  </span>
</template>

<script lang="ts" setup>
import { computed } from 'vue';

const props = defineProps<{
  status: 'active' | 'inactive' | 'maintenance' | 'available' | 'in-use' | string;
}>();

const statusClasses = computed(() => {
  switch (props.status.toLowerCase()) {
    case 'active':
    case 'available':
      return 'bg-green-100 text-green-700 border border-green-200';
    case 'inactive':
      return 'bg-red-100 text-red-700 border border-red-200';
    case 'maintenance':
      return 'bg-orange-100 text-orange-700 border border-orange-200';
    case 'in-use':
      return 'bg-blue-100 text-blue-700 border border-blue-200';
    default:
      return 'bg-gray-100 text-gray-700 border border-gray-200';
  }
});

const dotClass = computed(() => {
  switch (props.status.toLowerCase()) {
    case 'active':
    case 'available':
      return 'bg-green-500 animate-pulse';
    case 'inactive':
      return 'bg-red-500';
    case 'maintenance':
      return 'bg-orange-500 animate-pulse';
    case 'in-use':
      return 'bg-blue-500 animate-pulse';
    default:
      return 'bg-gray-500';
  }
});
</script>