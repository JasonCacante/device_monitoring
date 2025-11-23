<template>
  <MainLayout>
    <div class="equipment-detail-view p-4">
      <div v-if="store.loading" class="text-center">
        <p>Cargando...</p>
      </div>
      <div v-else-if="store.selectedEquipment" class="space-y-6">
        <div class="bg-white shadow rounded-lg p-6">
          <div class="flex flex-col md:flex-row md:space-x-6">
            <div class="md:w-1/3">
              <img :src="store.selectedEquipment.image_url || 'https://via.placeholder.com/300'" alt="Equipment Image" class="rounded-lg shadow-md">
            </div>
            <div class="md:w-2/3 mt-4 md:mt-0">
              <h2 class="text-3xl font-bold text-gray-800">{{ store.selectedEquipment.name }}</h2>
              <p class="text-lg text-gray-500">{{ store.selectedEquipment.serial }}</p>
              <div class="mt-4 flex items-center">
                <StatusBadge :status="store.selectedEquipment.status" class="mr-4">{{ store.selectedEquipment.status }}</StatusBadge>
                <span class="text-gray-600">{{ store.selectedEquipment.location }}</span>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-white shadow rounded-lg p-6">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-2xl font-semibold text-gray-700">Historial de Mantenimiento</h3>
            <BaseButton @click="showNewMaintenanceModal = true">Añadir Mantenimiento</BaseButton>
          </div>
          <div v-if="store.selectedEquipment.maintenances && store.selectedEquipment.maintenances.length > 0">
            <ul class="divide-y divide-gray-200">
              <li v-for="maintenance in store.selectedEquipment.maintenances" :key="maintenance.id" class="py-4">
                <p class="text-gray-900 font-medium">{{ maintenance.description }}</p>
                <p class="text-gray-600 text-sm">Fecha: {{ new Date(maintenance.date).toLocaleDateString() }}</p>
                <p class="text-gray-600 text-sm">Técnico: {{ maintenance.technician }}</p>
              </li>
            </ul>
          </div>
          <div v-else class="text-gray-500">
            No hay historial de mantenimiento para este equipo.
          </div>
        </div>

        <div class="bg-white shadow rounded-lg p-6">
          <h3 class="text-2xl font-semibold text-gray-700 mb-4">Notas</h3>
          <div class="text-gray-500">
            <!-- Notes section can be implemented here -->
            No hay notas para este equipo.
          </div>
        </div>

      </div>
      <div v-else class="text-center text-gray-500">
        Equipo no encontrado.
      </div>
    </div>
    <NewMaintenanceModal :show="showNewMaintenanceModal" :equipment-id="store.selectedEquipment?.id" @close="showNewMaintenanceModal = false" />
  </MainLayout>
</template>

<script lang="ts" setup>
import { onMounted, ref } from 'vue';
import { useRoute } from 'vue-router';
import { useEquipmentStore } from '../stores/equipmentStore';
import MainLayout from '../layouts/MainLayout.vue';
import StatusBadge from '../components/ui/StatusBadge.vue';
import BaseButton from '../components/ui/BaseButton.vue';
import NewMaintenanceModal from '../components/ui/NewMaintenanceModal.vue';
import { useToast } from 'vue-toastification';

const store = useEquipmentStore();
const route = useRoute();
const toast = useToast();
const showNewMaintenanceModal = ref(false);

onMounted(async () => {
  const equipmentId = Number(route.params.id);
  await store.fetchEquipmentById(equipmentId);
  if (store.error) {
    toast.error(store.error);
  }
});
</script>