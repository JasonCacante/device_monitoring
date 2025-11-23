<template>
  <MainLayout>
    <div class="equipment-list-view p-4">
      <h2 class="text-3xl font-bold mb-6 text-gray-800">Equipos</h2>

      <!-- Filters Section -->
      <div class="flex flex-col sm:flex-row justify-between items-center mb-6 space-y-4 sm:space-y-0">
        <InputSearch placeholder="Buscar equipos..." class="w-full sm:w-1/3" />
        <div class="flex space-x-4">
          <!-- Advanced Filter Components could go here -->
          <BaseButton>Filtrar</BaseButton>
        </div>
      </div>

      <!-- Equipment Grid -->
      <div v-if="store.loading" class="text-center">
        <p>Cargando...</p>
      </div>
      <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        <EquipmentCard v-for="equipment in store.equipments" :key="equipment.id" :equipment="equipment" />
      </div>
    </div>
  </MainLayout>
</template>

<script lang="ts" setup>
import { onMounted } from 'vue';
import { useEquipmentStore } from '../stores/equipmentStore';
import MainLayout from '../layouts/MainLayout.vue';
import InputSearch from '../components/ui/InputSearch.vue';
import BaseButton from '../components/ui/BaseButton.vue';
import EquipmentCard from '../components/ui/EquipmentCard.vue';
import { useToast } from 'vue-toastification';

const store = useEquipmentStore();
const toast = useToast();

onMounted(async () => {
  await store.fetchEquipments();
  if (store.error) {
    toast.error(store.error);
  }
});
</script>