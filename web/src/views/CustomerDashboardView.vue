<template>
  <MainLayout>
    <div class="p-8">
      <!-- Welcome Section -->
      <div class="mb-8 bg-gradient-to-r from-purple-500 to-pink-600 rounded-2xl p-8 text-white shadow-lg">
        <h1 class="text-3xl font-bold mb-2">
          ¡Bienvenido, {{ authStore.currentUser?.name }}! 🎯
        </h1>
        <p class="text-purple-100">
          Panel de Cliente - Visualiza tus equipos
        </p>
      </div>

      <!-- Stats Cards -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div class="bg-white rounded-xl shadow-md p-6 border border-gray-200">
          <div class="flex items-center justify-between mb-4">
            <span class="material-symbols-outlined text-purple-600 text-3xl">
              inventory_2
            </span>
            <span class="text-sm font-medium text-gray-500">Total</span>
          </div>
          <p class="text-3xl font-bold text-gray-900">{{ ownedCount }}</p>
          <p class="text-sm text-gray-600 mt-1">Equipos contratados</p>
        </div>

        <div class="bg-white rounded-xl shadow-md p-6 border border-gray-200">
          <div class="flex items-center justify-between mb-4">
            <span class="material-symbols-outlined text-green-600 text-3xl">
              check_circle
            </span>
            <span class="text-sm font-medium text-gray-500">Activos</span>
          </div>
          <p class="text-3xl font-bold text-gray-900">{{ activeCount }}</p>
          <p class="text-sm text-gray-600 mt-1">En funcionamiento</p>
        </div>

        <div class="bg-white rounded-xl shadow-md p-6 border border-gray-200">
          <div class="flex items-center justify-between mb-4">
            <span class="material-symbols-outlined text-blue-600 text-3xl">
              support_agent
            </span>
            <span class="text-sm font-medium text-gray-500">Soporte</span>
          </div>
          <p class="text-3xl font-bold text-gray-900">24/7</p>
          <p class="text-sm text-gray-600 mt-1">Disponible para ti</p>
        </div>
      </div>

      <!-- Equipment List -->
      <div class="bg-white rounded-xl shadow-md p-6 border border-gray-200">
        <div class="flex items-center justify-between mb-6">
          <h2 class="text-xl font-bold text-gray-900 flex items-center gap-2">
            <span class="material-symbols-outlined text-purple-600">
              devices
            </span>
            Mis Equipos
          </h2>
          
          <button 
            @click="requestMaintenance"
            class="px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors flex items-center gap-2"
          >
            <span class="material-symbols-outlined">
              support_agent
            </span>
            <span>Solicitar Soporte</span>
          </button>
        </div>

        <div v-if="isLoading" class="text-center py-12">
          <span class="material-symbols-outlined text-4xl text-gray-400 animate-spin">
            progress_activity
          </span>
          <p class="text-gray-600 mt-2">Cargando equipos...</p>
        </div>

        <div v-else-if="ownedEquipment.length === 0" class="text-center py-12">
          <span class="material-symbols-outlined text-6xl text-gray-300">
            devices_off
          </span>
          <p class="text-gray-600 mt-4">No tienes equipos contratados</p>
        </div>

        <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div 
            v-for="equipment in ownedEquipment" 
            :key="equipment.id"
            class="border border-gray-200 rounded-xl p-6 hover:shadow-lg transition-all"
          >
            <div class="flex items-start justify-between mb-4">
              <div class="flex-1 cursor-pointer" @click="viewDetails(equipment.id)">
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
            
            <div class="space-y-2 text-sm mb-4">
              <div class="flex items-center gap-2 text-gray-600">
                <span class="material-symbols-outlined text-base">location_on</span>
                <span>{{ equipment.location || 'Sin ubicación' }}</span>
              </div>
              <div class="flex items-center gap-2 text-gray-600">
                <span class="material-symbols-outlined text-base">calendar_today</span>
                <span>{{ formatDate(equipment.last_checkin) }}</span>
              </div>
              <div class="flex items-center gap-2 text-gray-600">
                <span class="material-symbols-outlined text-base">build</span>
                <span>{{ formatDate(equipment.last_maintenance) }}</span>
              </div>
            </div>

            <button
              @click="openMaintenanceModal(equipment)"
              class="w-full py-2 px-4 bg-purple-600 text-white rounded-lg hover:bg-purple-700 transition-colors flex items-center justify-center gap-2 text-sm font-medium"
            >
              <span class="material-symbols-outlined text-base">build_circle</span>
              <span>Solicitar Mantenimiento</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Maintenance Request Modal -->
    <MaintenanceRequestModal 
      :show="showMaintenanceModal" 
      :equipment="selectedEquipment"
      @close="showMaintenanceModal = false"
      @success="handleMaintenanceSuccess"
    />
  </MainLayout>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/authStore';
import { useEquipmentStore } from '../stores/equipmentStore';
import MainLayout from '../layouts/MainLayout.vue';
import MaintenanceRequestModal from '../components/ui/MaintenanceRequestModal.vue';
import { useToast } from 'vue-toastification';

const router = useRouter();
const authStore = useAuthStore();
const equipmentStore = useEquipmentStore();
const toast = useToast();

const isLoading = ref(true);
const showMaintenanceModal = ref(false);
const selectedEquipment = ref<any>(null);

// Backend already filters equipment by customer_id for customers
const ownedEquipment = computed(() => equipmentStore.equipments);

const ownedCount = computed(() => ownedEquipment.value.length);
const activeCount = computed(() => 
  ownedEquipment.value.filter((eq: any) => eq.status === 'Operativo').length
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

function requestMaintenance() {
  if (ownedEquipment.value.length === 0) {
    toast.warning('No tienes equipos para solicitar mantenimiento');
    return;
  }
  selectedEquipment.value = ownedEquipment.value[0];
  showMaintenanceModal.value = true;
}

function openMaintenanceModal(equipment: any) {
  selectedEquipment.value = equipment;
  showMaintenanceModal.value = true;
}

function handleMaintenanceSuccess() {
  toast.success('Tu solicitud ha sido enviada. Te contactaremos pronto.');
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
