<template>
  <MainLayout>
    <div class="p-8">
      <!-- Welcome Section -->
      <div class="mb-8 bg-gradient-to-r from-blue-500 to-purple-600 rounded-2xl p-8 text-white shadow-lg">
        <h1 class="text-3xl font-bold mb-2">
          ¡Bienvenido, {{ authStore.currentUser?.name }}! 👋
        </h1>
        <p class="text-blue-100">
          Panel de Personal - Visualiza tus equipos asignados
        </p>
      </div>

      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div class="bg-white rounded-xl shadow-md p-6 border border-gray-200">
          <div class="flex items-center justify-between mb-4">
            <span class="material-symbols-outlined text-blue-600 text-3xl">
              devices
            </span>
            <span class="text-sm font-medium text-gray-500">Asignados</span>
          </div>
          <p class="text-3xl font-bold text-gray-900">{{ assignedCount }}</p>
          <p class="text-sm text-gray-600 mt-1">Equipos a tu cargo</p>
        </div>

        <div class="bg-white rounded-xl shadow-md p-6 border border-gray-200">
          <div class="flex items-center justify-between mb-4">
            <span class="material-symbols-outlined text-green-600 text-3xl">
              check_circle
            </span>
            <span class="text-sm font-medium text-gray-500">Estado</span>
          </div>
          <p class="text-3xl font-bold text-gray-900">{{ onlineCount }}</p>
          <p class="text-sm text-gray-600 mt-1">Equipos en línea</p>
        </div>

        <div class="bg-white rounded-xl shadow-md p-6 border border-gray-200">
          <div class="flex items-center justify-between mb-4">
            <span class="material-symbols-outlined text-orange-600 text-3xl">
              build
            </span>
            <span class="text-sm font-medium text-gray-500">Mantenimiento</span>
          </div>
          <p class="text-3xl font-bold text-gray-900">{{ maintenanceCount }}</p>
          <p class="text-sm text-gray-600 mt-1">Próximos servicios</p>
        </div>
      </div>

      <!-- Equipment List -->
      <div class="bg-white rounded-xl shadow-md p-6 border border-gray-200">
        <h2 class="text-xl font-bold text-gray-900 mb-6 flex items-center gap-2">
          <span class="material-symbols-outlined text-blue-600">
            assignment
          </span>
          Mis Equipos Asignados
        </h2>

        <div v-if="isLoading" class="text-center py-12">
          <span class="material-symbols-outlined text-4xl text-gray-400 animate-spin">
            progress_activity
          </span>
          <p class="text-gray-600 mt-2">Cargando equipos...</p>
        </div>

        <div v-else-if="assignedEquipment.length === 0" class="text-center py-12">
          <span class="material-symbols-outlined text-6xl text-gray-300">
            devices_off
          </span>
          <p class="text-gray-600 mt-4">No tienes equipos asignados</p>
        </div>

        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div 
            v-for="equipment in assignedEquipment" 
            :key="equipment.id"
            class="border border-gray-200 rounded-xl p-6 hover:shadow-lg transition-all cursor-pointer"
            @click="viewDetails(equipment.id)"
          >
            <div class="flex items-start justify-between mb-4">
              <div>
                <h3 class="text-lg font-semibold text-gray-900">{{ equipment.name }}</h3>
                <p class="text-sm text-gray-500">{{ equipment.type }}</p>
              </div>
              <span 
                :class="getStatusClass(equipment.status)"
                class="px-3 py-1 text-xs font-medium rounded-full"
              >
                {{ equipment.status }}
              </span>
            </div>
            
            <div class="space-y-2 text-sm">
              <div class="flex items-center gap-2 text-gray-600">
                <span class="material-symbols-outlined text-base">location_on</span>
                <span>{{ equipment.location || 'Sin ubicación' }}</span>
              </div>
              <div class="flex items-center gap-2 text-gray-600">
                <span class="material-symbols-outlined text-base">calendar_today</span>
                <span>{{ formatDate(equipment.last_checkin) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </MainLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/authStore';
import { useEquipmentStore } from '../stores/equipmentStore';
import MainLayout from '../layouts/MainLayout.vue';

const router = useRouter();
const authStore = useAuthStore();
const equipmentStore = useEquipmentStore();

const isLoading = ref(true);

// Backend already filters equipment by assigned_to_id for staff
const assignedEquipment = computed(() => equipmentStore.equipments);

const assignedCount = computed(() => assignedEquipment.value.length);
const onlineCount = computed(() => 
  assignedEquipment.value.filter((eq: any) => eq.status === 'Operativo').length
);
const maintenanceCount = computed(() => 
  assignedEquipment.value.filter((eq: any) => eq.status === 'Mantenimiento').length
);

function getStatusClass(status: string): string {
  const classes: Record<string, string> = {
    'Operativo': 'bg-green-100 text-green-800',
    'Fuera de Servicio': 'bg-red-100 text-red-800',
    'Mantenimiento': 'bg-orange-100 text-orange-800',
  };
  return classes[status] || 'bg-gray-100 text-gray-800';
}

function formatDate(date: string | null): string {
  if (!date) return 'Sin registro';
  return new Date(date).toLocaleDateString('es-ES', {
    day: '2-digit',
    month: 'short',
    year: 'numeric'
  });
}

function viewDetails(id: number) {
  router.push({ name: 'equipment-detail', params: { id } });
}

onMounted(async () => {
  try {
    await equipmentStore.fetchEquipments();
  } catch (error) {
    console.error('Error loading equipment:', error);
  } finally {
    isLoading.value = false;
  }
});
</script>
