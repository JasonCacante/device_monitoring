import { defineStore } from 'pinia';
import { ref } from 'vue';
import apiClient from '../services/api'; // Import the apiClient

// Mapeo de estados frontend <-> backend
function mapStatusToBackend(status: string): string {
  const statusMap: { [key: string]: string } = {
    'Operativo': 'active',
    'Mantenimiento': 'maintenance',
    'Fuera de Servicio': 'inactive'
  };
  return statusMap[status] || status.toLowerCase();
}

function mapStatusToFrontend(status: string): string {
  const statusMap: { [key: string]: string } = {
    'active': 'Operativo',
    'maintenance': 'Mantenimiento',
    'inactive': 'Fuera de Servicio'
  };
  return statusMap[status] || status;
}

export const useEquipmentStore = defineStore('equipment', () => {
  const equipments = ref<any[]>([]); // To store the list of equipments
  const selectedEquipment = ref<any | null>(null); // To store details of a selected equipment
  const dashboardStats = ref<any>({}); // To store dashboard statistics
  const chartData = ref<any>({}); // To store chart data
  const loading = ref(false); // To indicate loading state
  const error = ref<string | null>(null); // To store any error messages

  // Actions
  async function fetchEquipments() {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.get('/equipos');
      equipments.value = response.data;
    } catch (err: any) {
      error.value = err.message;
    } finally {
      loading.value = false;
    }
  }

  async function fetchEquipmentById(id: number) {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.get(`/equipos/${id}`);
      selectedEquipment.value = response.data;
    } catch (err: any) {
      error.value = err.message;
    } finally {
      loading.value = false;
    }
  }

  async function fetchDashboardStats() {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.get('/dashboard/stats');
      dashboardStats.value = response.data;
    } catch (err: any) {
      error.value = err.message;
    } finally {
      loading.value = false;
    }
  }

  async function fetchChartData() {
    loading.value = true;
    error.value = null;
    try {
      const response = await apiClient.get('/dashboard/chart-data');
      chartData.value = response.data;
    } catch (err: any) {
      error.value = err.message;
    } finally {
      loading.value = false;
    }
  }

  async function createEquipment(equipmentData: any) {
    loading.value = true;
    error.value = null;
    try {
      // Mapear estado del frontend al backend
      const mappedData = {
        ...equipmentData,
        status: mapStatusToBackend(equipmentData.status)
      };
      const response = await apiClient.post('/equipos', mappedData);
      equipments.value.push(response.data);
      return response.data;
    } catch (err: any) {
      error.value = err.response?.data?.detail || err.message;
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function updateEquipment(id: number, equipmentData: any) {
    loading.value = true;
    error.value = null;
    try {
      // Mapear estado del frontend al backend
      const mappedData = {
        ...equipmentData,
        status: mapStatusToBackend(equipmentData.status)
      };
      const response = await apiClient.patch(`/equipos/${id}`, mappedData);
      const index = equipments.value.findIndex(eq => eq.id === id);
      if (index !== -1) {
        equipments.value[index] = response.data;
      }
      if (selectedEquipment.value?.id === id) {
        selectedEquipment.value = response.data;
      }
      return response.data;
    } catch (err: any) {
      error.value = err.response?.data?.detail || err.message;
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function deleteEquipment(id: number) {
    loading.value = true;
    error.value = null;
    try {
      await apiClient.delete(`/equipos/${id}`);
      equipments.value = equipments.value.filter(eq => eq.id !== id);
      if (selectedEquipment.value?.id === id) {
        selectedEquipment.value = null;
      }
    } catch (err: any) {
      error.value = err.response?.data?.detail || err.message;
      throw err;
    } finally {
      loading.value = false;
    }
  }

  async function createMaintenance(equipmentId: number, maintenanceData: any) {
    loading.value = true;
    error.value = null;
    try {
      // Mapear datos del frontend al formato del backend
      const backendData = {
        description: `${maintenanceData.maintenance_type || 'Mantenimiento'}: ${maintenanceData.description}`,
        date: maintenanceData.scheduled_date,
        technician: 'Por asignar' // El backend requiere este campo
      };
      const response = await apiClient.post(`/equipos/${equipmentId}/maintenances/`, backendData);
      return response.data;
    } catch (err: any) {
      error.value = err.response?.data?.detail || err.message;
      throw err;
    } finally {
      loading.value = false;
    }
  }

  return {
    equipments,
    selectedEquipment,
    dashboardStats,
    chartData,
    loading,
    error,
    fetchEquipments,
    fetchEquipmentById,
    fetchDashboardStats,
    fetchChartData,
    createEquipment,
    updateEquipment,
    deleteEquipment,
    createMaintenance,
  };
});