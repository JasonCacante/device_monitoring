<template>
  <div class="relative rounded-xl shadow-md hover:shadow-lg transition-shadow">
    <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
      <span class="material-symbols-outlined text-blue-600 text-xl">search</span>
    </div>
    <input
      type="text"
      :value="modelValue"
      @input="$emit('update:modelValue', ($event.target as HTMLInputElement).value)"
      class="focus:ring-2 focus:ring-blue-500 focus:border-blue-500 block w-full pl-12 pr-4 py-3 border-2 border-slate-200 rounded-xl leading-5 bg-white placeholder-slate-400 focus:placeholder-slate-300 text-sm font-medium hover:border-blue-300 transition-all"
      :placeholder="placeholder"
    />
  </div>
</template>

<script lang="ts" setup>
defineProps({
  modelValue: {
    type: String,
    default: '',
  },
  placeholder: {
    type: String,
    default: 'Search...',
  },
});

defineEmits(['update:modelValue']);
</script>