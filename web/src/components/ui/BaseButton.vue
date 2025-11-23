<template>
  <button class="px-6 py-3 font-bold text-white bg-gradient-to-r from-blue-600 to-indigo-600 rounded-xl hover:from-blue-700 hover:to-indigo-700 focus:outline-none focus:ring-4 focus:ring-blue-300 shadow-lg hover:shadow-xl transition-all duration-200 transform hover:-translate-y-0.5 flex items-center gap-2">
    <slot></slot>
  </button>
</template>

<script lang="ts" setup>
// No specific logic for a base button, it just renders its slot content.
</script>