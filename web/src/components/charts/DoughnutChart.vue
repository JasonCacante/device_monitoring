<template>
  <div class="bg-white rounded-2xl p-8 shadow-xl border border-blue-100 h-full">
    <div class="mb-6">
      <h3 class="text-2xl font-bold text-text-primary mb-2">Equipment Status</h3>
      <p class="text-sm text-text-secondary">Current distribution of machines by status</p>
    </div>
    <div class="flex items-center justify-center" style="height: 320px;">
      <Doughnut :data="chartData" :options="chartOptions" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import { Doughnut } from 'vue-chartjs';
import type { PropType } from 'vue';

ChartJS.register(ArcElement, Tooltip, Legend);

defineProps({
  chartData: {
    type: Object as PropType<{
      labels: string[];
      datasets: {
        backgroundColor: string[];
        data: number[];
      }[];
    }>,
    required: true,
  },
});

const chartOptions = {
  responsive: true,
  maintainAspectRatio: true,
  plugins: {
    legend: {
      position: 'bottom' as const,
      labels: {
        color: '#2D3748',
        boxWidth: 16,
        padding: 15,
        font: {
          size: 13,
          weight: '600' as const,
        },
        usePointStyle: true,
        pointStyle: 'circle',
      },
    },
    tooltip: {
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      padding: 12,
      titleFont: {
        size: 14,
        weight: 'bold' as const,
      },
      bodyFont: {
        size: 13,
      },
      borderColor: '#e5e7eb',
      borderWidth: 1,
    },
  },
};
</script>
