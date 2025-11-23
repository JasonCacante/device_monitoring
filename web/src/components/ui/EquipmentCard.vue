<template>
  <div class="bg-white rounded-lg shadow-md p-4 flex flex-col justify-between">
    <div>
      <div class="flex justify-between items-start">
        <h3 class="text-lg font-semibold text-gray-800">{{ equipment.name }}</h3>
        <StatusBadge :status="equipment.status">{{ equipment.status }}</StatusBadge>
      </div>
      <p class="text-sm text-gray-500">{{ equipment.serial }}</p>
      <p class="text-sm text-gray-500 mt-2">{{ equipment.location }}</p>
    </div>
    <div class="mt-4 flex justify-end space-x-2">
      <router-link :to="`/equipment/${equipment.id}`" class="text-primary-dark hover:underline">Ver</router-link>
      <button class="text-blue-600 hover:underline">Editar</button>
      <button class="text-red-600 hover:underline">Eliminar</button>
    </div>
  </div>
</template>

<script lang="ts" setup>
import StatusBadge from './StatusBadge.vue';

defineProps({
  equipment: {
    type: Object,
    required: true,
  },
});
</script>