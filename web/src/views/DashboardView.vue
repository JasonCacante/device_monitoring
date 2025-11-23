<template>
  <MainLayout>
    <template #header>
      <Header />
    </template>
    <div class="dashboard-view bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 min-h-screen">
      <div class="p-8 max-w-7xl mx-auto">
        <div class="mb-8">
          <h1 class="text-text-primary text-4xl font-bold mb-2 bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">Dashboard Overview</h1>
          <p class="text-text-secondary text-base">Monitor and manage your machine fleet</p>
        </div>
        <!-- Stats -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
          <div class="group flex flex-col gap-3 rounded-2xl p-6 bg-white shadow-md hover:shadow-xl transition-all duration-300 border border-blue-100 hover:border-blue-300 hover:-translate-y-1">
              <div class="flex items-center justify-between">
                <p class="text-text-secondary text-sm font-semibold uppercase tracking-wide">Total Machines</p>
                <div class="p-2 bg-blue-100 rounded-lg group-hover:bg-blue-200 transition-colors">
                  <span class="material-symbols-outlined text-blue-600 text-xl">precision_manufacturing</span>
                </div>
              </div>
              <p class="text-text-primary text-4xl font-bold">{{ store.dashboardStats.total_equipments }}</p>
              <div class="flex items-center text-success text-sm font-semibold">
                <span class="mr-1">+5.2%</span>
                <svg width="10" height="7" viewBox="0 0 10 7" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M0.833374 5.83333L4.16671 2.5L6.66671 5L9.16671 0.833333" stroke="#10B981" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <span class="ml-1 text-text-secondary font-normal">vs last month</span>
              </div>
          </div>
          <div class="group flex flex-col gap-3 rounded-2xl p-6 bg-white shadow-md hover:shadow-xl transition-all duration-300 border border-green-100 hover:border-green-300 hover:-translate-y-1">
              <div class="flex items-center justify-between">
                <p class="text-text-secondary text-sm font-semibold uppercase tracking-wide">Available</p>
                <div class="p-2 bg-green-100 rounded-lg group-hover:bg-green-200 transition-colors">
                  <span class="material-symbols-outlined text-green-600 text-xl">check_circle</span>
                </div>
              </div>
              <p class="text-text-primary text-4xl font-bold">{{ store.dashboardStats.active_equipments }}</p>
              <div class="flex items-center text-error text-sm font-semibold">
                <span class="mr-1">-1.1%</span>
                <svg width="10" height="7" viewBox="0 0 10 7" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M9.16663 1.16667L5.83329 4.5L3.33329 2L0.833293 6.16667" stroke="#EF4444" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <span class="ml-1 text-text-secondary font-normal">vs last month</span>
              </div>
          </div>
          <div class="group flex flex-col gap-3 rounded-2xl p-6 bg-white shadow-md hover:shadow-xl transition-all duration-300 border border-purple-100 hover:border-purple-300 hover:-translate-y-1">
              <div class="flex items-center justify-between">
                <p class="text-text-secondary text-sm font-semibold uppercase tracking-wide">Active Users</p>
                <div class="p-2 bg-purple-100 rounded-lg group-hover:bg-purple-200 transition-colors">
                  <span class="material-symbols-outlined text-purple-600 text-xl">group</span>
                </div>
              </div>
              <p class="text-text-primary text-4xl font-bold">45</p>
              <div class="flex items-center text-success text-sm font-semibold">
                <span class="mr-1">+2.8%</span>
                 <svg width="10" height="7" viewBox="0 0 10 7" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M0.833374 5.83333L4.16671 2.5L6.66671 5L9.16671 0.833333" stroke="#10B981" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <span class="ml-1 text-text-secondary font-normal">vs last month</span>
              </div>
          </div>
          <div class="group flex flex-col gap-3 rounded-2xl p-6 bg-white shadow-md hover:shadow-xl transition-all duration-300 border border-orange-100 hover:border-orange-300 hover:-translate-y-1">
              <div class="flex items-center justify-between">
                <p class="text-text-secondary text-sm font-semibold uppercase tracking-wide">Pending</p>
                <div class="p-2 bg-orange-100 rounded-lg group-hover:bg-orange-200 transition-colors">
                  <span class="material-symbols-outlined text-orange-600 text-xl">pending_actions</span>
                </div>
              </div>
              <p class="text-text-primary text-4xl font-bold">3</p>
              <div class="flex items-center text-success text-sm font-semibold">
                <span class="mr-1">+1.0%</span>
                 <svg width="10" height="7" viewBox="0 0 10 7" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M0.833374 5.83333L4.16671 2.5L6.66671 5L9.16671 0.833333" stroke="#10B981" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                <span class="ml-1 text-text-secondary font-normal">vs last month</span>
              </div>
          </div>
        </div>

        <!-- Charts and Analytics Section -->
        <div class="mb-10">
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <!-- Doughnut Chart -->
            <div class="lg:col-span-1">
              <DoughnutChart v-if="store.chartData && Object.keys(store.chartData).length > 0" :chart-data="formattedChartData" />
              <div v-else class="bg-white rounded-2xl p-8 shadow-xl border border-blue-100 h-full flex items-center justify-center">
                <div class="text-center">
                  <span class="material-symbols-outlined text-6xl text-gray-300 mb-4">pie_chart</span>
                  <p class="text-text-secondary">Loading chart data...</p>
                </div>
              </div>
            </div>
            
            <!-- Additional stats or info cards -->
            <div class="lg:col-span-2 grid grid-cols-1 md:grid-cols-2 gap-6">
              <!-- Recent Activity Card -->
              <div class="bg-white rounded-2xl p-6 shadow-xl border border-blue-100">
                <div class="flex items-center justify-between mb-4">
                  <h3 class="text-lg font-bold text-text-primary">Recent Activity</h3>
                  <span class="material-symbols-outlined text-blue-600">schedule</span>
                </div>
                <div class="space-y-3">
                  <div class="flex items-start gap-3 pb-3 border-b border-gray-100">
                    <div class="w-2 h-2 bg-green-500 rounded-full mt-2"></div>
                    <div class="flex-1">
                      <p class="text-sm font-semibold text-text-primary">Laptop A - Status Updated</p>
                      <p class="text-xs text-text-secondary">2 hours ago</p>
                    </div>
                  </div>
                  <div class="flex items-start gap-3 pb-3 border-b border-gray-100">
                    <div class="w-2 h-2 bg-orange-500 rounded-full mt-2"></div>
                    <div class="flex-1">
                      <p class="text-sm font-semibold text-text-primary">Servidor A - Maintenance</p>
                      <p class="text-xs text-text-secondary">5 hours ago</p>
                    </div>
                  </div>
                  <div class="flex items-start gap-3">
                    <div class="w-2 h-2 bg-green-500 rounded-full mt-2"></div>
                    <div class="flex-1">
                      <p class="text-sm font-semibold text-text-primary">Laptop B - Back Online</p>
                      <p class="text-xs text-text-secondary">1 day ago</p>
                    </div>
                  </div>
                </div>
              </div>

              <!-- System Health Card -->
              <div class="bg-white rounded-2xl p-6 shadow-xl border border-blue-100">
                <div class="flex items-center justify-between mb-4">
                  <h3 class="text-lg font-bold text-text-primary">System Health</h3>
                  <span class="material-symbols-outlined text-green-600">health_and_safety</span>
                </div>
                <div class="space-y-4">
                  <div>
                    <div class="flex items-center justify-between mb-2">
                      <span class="text-sm font-semibold text-text-primary">Uptime</span>
                      <span class="text-sm font-bold text-green-600">99.8%</span>
                    </div>
                    <div class="w-full bg-gray-200 rounded-full h-2">
                      <div class="bg-green-500 h-2 rounded-full" style="width: 99.8%"></div>
                    </div>
                  </div>
                  <div>
                    <div class="flex items-center justify-between mb-2">
                      <span class="text-sm font-semibold text-text-primary">Performance</span>
                      <span class="text-sm font-bold text-blue-600">95.2%</span>
                    </div>
                    <div class="w-full bg-gray-200 rounded-full h-2">
                      <div class="bg-blue-500 h-2 rounded-full" style="width: 95.2%"></div>
                    </div>
                  </div>
                  <div>
                    <div class="flex items-center justify-between mb-2">
                      <span class="text-sm font-semibold text-text-primary">Response Time</span>
                      <span class="text-sm font-bold text-indigo-600">92.5%</span>
                    </div>
                    <div class="w-full bg-gray-200 rounded-full h-2">
                      <div class="bg-indigo-500 h-2 rounded-full" style="width: 92.5%"></div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Tabs -->
        <div class="mb-8">
          <div class="bg-white rounded-2xl shadow-md p-2 inline-flex gap-2">
            <button @click="activeTab = 'machine-management'"
                 :class="[activeTab === 'machine-management' ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-lg' : 'text-text-secondary hover:bg-gray-100', 'px-6 py-3 rounded-xl font-semibold text-sm transition-all duration-300 flex items-center gap-2']">
                <span class="material-symbols-outlined text-lg">settings</span>
                Machine Management
            </button>
            <button @click="activeTab = 'user-management'"
                 :class="[activeTab === 'user-management' ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-lg' : 'text-text-secondary hover:bg-gray-100', 'px-6 py-3 rounded-xl font-semibold text-sm transition-all duration-300 flex items-center gap-2']">
                <span class="material-symbols-outlined text-lg">group</span>
                User Management
            </button>
          </div>
          <div class="mt-6">
            <div v-if="activeTab === 'machine-management'">
              <MachineManagementTable :equipments="store.equipments" @refresh="refreshData" />
            </div>
            <div v-else-if="activeTab === 'user-management'">
              <div class="bg-white rounded-2xl p-8 shadow-xl border border-blue-100 text-center">
                <span class="material-symbols-outlined text-6xl text-gray-300 mb-4">group</span>
                <h2 class="text-xl font-semibold text-text-primary mb-2">User Management</h2>
                <p class="text-text-secondary">Coming Soon</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </MainLayout>
</template>

<script lang="ts" setup>
import { onMounted, ref, computed } from 'vue';
import { useEquipmentStore } from '../stores/equipmentStore';
import MainLayout from '../layouts/MainLayout.vue';
import Header from '../components/layout/Header.vue';
import MachineManagementTable from '../components/dashboard/MachineManagementTable.vue';
import DoughnutChart from '../components/charts/DoughnutChart.vue';
import { useToast } from 'vue-toastification';

const store = useEquipmentStore();
const toast = useToast();
const activeTab = ref('machine-management'); // Set default active tab

const formattedChartData = computed(() => {
  const chartDataFromStore = store.chartData;
  if (!chartDataFromStore || Object.keys(chartDataFromStore).length === 0) {
    return { labels: [], datasets: [] };
  }

  const labels = Object.keys(chartDataFromStore).map(key => {
    // Capitalize the first letter for display
    return key.charAt(0).toUpperCase() + key.slice(1);
  });
  const data = Object.values(chartDataFromStore);

  return {
    labels: labels,
    datasets: [
      {
        backgroundColor: ['#10B981', '#F59E0B', '#EF4444'], // success, warning, error
        data: data,
      },
    ],
  };
});

async function refreshData() {
  await store.fetchDashboardStats();
  await store.fetchEquipments();
  await store.fetchChartData();
}

onMounted(async () => {
  await refreshData();
  if (store.error) {
    toast.error(store.error);
  }
});
</script>