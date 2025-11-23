<template>
  <div class="bg-white rounded-2xl border border-blue-100 shadow-xl overflow-hidden">
    <div class="p-8">
      <div class="flex flex-col gap-6">
        <div class="flex justify-between items-center">
          <div>
            <h2 class="text-2xl font-bold text-text-primary mb-1">Manage Machines</h2>
            <p class="text-sm text-text-secondary">View and manage all your machines in one place</p>
          </div>
          <div class="flex items-center gap-4">
            <InputSearch v-model="searchQuery" placeholder="Search machine..." />
            <BaseButton theme="primary" @click="openNewEquipmentModal" class="rounded-xl shadow-lg hover:shadow-xl transition-shadow">
              <span class="material-symbols-outlined text-base">add_circle</span>
              Add Machine
            </BaseButton>
          </div>
        </div>
        <div class="overflow-x-auto rounded-xl border border-slate-200">
          <table class="w-full text-left">
            <thead class="bg-gradient-to-r from-slate-50 to-blue-50 text-xs text-text-primary uppercase font-bold">
              <tr>
                <th class="px-6 py-4" scope="col"><input class="form-checkbox rounded-md border-slate-300 text-blue-600 focus:ring-blue-500 focus:ring-2 cursor-pointer" type="checkbox"/></th>
                <th class="px-6 py-4 font-bold text-left" scope="col">Serial</th>
                <th class="px-6 py-4 font-bold text-left" scope="col">Machine Name</th>
                <th class="px-6 py-4 font-bold text-left" scope="col">Status</th>
                <th class="px-6 py-4 font-bold text-left" scope="col">Location</th>
                <th class="px-6 py-4 font-bold text-left" scope="col">Last Checkin</th>
                <th class="px-6 py-4 font-bold text-left" scope="col">Actions</th>
              </tr>
            </thead>
            <tbody class="text-sm text-text-secondary">
              <tr v-for="equipment in filteredEquipments" :key="equipment.id" class="border-b border-slate-100 hover:bg-blue-50/50 transition-colors">
                <td class="px-6 py-5"><input class="form-checkbox rounded-md border-slate-300 text-blue-600 focus:ring-blue-500 focus:ring-2 cursor-pointer" type="checkbox"/></td>
                <td class="px-6 py-5 font-mono text-sm font-semibold text-slate-600">{{ equipment.serial }}</td>
                <td class="px-6 py-5 font-semibold text-text-primary">{{ equipment.name }}</td>
                <td class="px-6 py-5"><StatusBadge :status="equipment.status">{{ equipment.status }}</StatusBadge></td>
                <td class="px-6 py-5 text-text-primary">{{ equipment.location || '-' }}</td>
                <td class="px-6 py-5 text-text-primary">{{ formatDate(equipment.last_checkin) }}</td>
                <td class="px-6 py-5 flex gap-2">
                  <button class="p-2 text-text-secondary hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-all" @click.prevent="openEditModal(equipment)"><span class="material-symbols-outlined text-xl">edit</span></button>
                  <button class="p-2 text-text-secondary hover:text-red-600 hover:bg-red-50 rounded-lg transition-all" @click.prevent="openDeleteModal(equipment)"><span class="material-symbols-outlined text-xl">delete</span></button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- Modals -->
    <NewEquipmentModal 
      :show="isNewModalOpen" 
      @close="isNewModalOpen = false"
      @success="handleSuccess"
    />
    <EditEquipmentModal 
      :show="isEditModalOpen" 
      :equipment="selectedEquipment"
      @close="isEditModalOpen = false"
      @success="handleSuccess"
    />
    <DeleteConfirmModal 
      :show="isDeleteModalOpen" 
      :equipment="selectedEquipment"
      @close="isDeleteModalOpen = false"
      @success="handleSuccess"
    />
  </div>
</template>

<script lang="ts" setup>
import { ref, computed } from 'vue';
import { useEquipmentStore } from '../../stores/equipmentStore';
import StatusBadge from '../ui/StatusBadge.vue';
import BaseButton from '../ui/BaseButton.vue';
import InputSearch from '../ui/InputSearch.vue';
import NewEquipmentModal from '../ui/NewEquipmentModal.vue';
import EditEquipmentModal from '../ui/EditEquipmentModal.vue';
import DeleteConfirmModal from '../ui/DeleteConfirmModal.vue';

const props = defineProps<{
  equipments: any[];
}>();

const emit = defineEmits(['refresh']);

const store = useEquipmentStore();

const searchQuery = ref('');
const isNewModalOpen = ref(false);
const isEditModalOpen = ref(false);
const isDeleteModalOpen = ref(false);
const selectedEquipment = ref<any>(null);

const filteredEquipments = computed(() => {
  if (!searchQuery.value) {
    return props.equipments;
  }
  const query = searchQuery.value.toLowerCase();
  return props.equipments.filter(equipment =>
    equipment.name?.toLowerCase().includes(query) ||
    equipment.type?.toLowerCase().includes(query) ||
    equipment.location?.toLowerCase().includes(query) ||
    equipment.serial?.toLowerCase().includes(query)
  );
});

function formatDate(date: string | null): string {
  if (!date) return 'Never';
  return new Date(date).toLocaleDateString('en-US', { 
    month: '2-digit', 
    day: '2-digit', 
    year: 'numeric' 
  });
}

function openNewEquipmentModal() {
  isNewModalOpen.value = true;
}

function openEditModal(equipment: any) {
  selectedEquipment.value = equipment;
  isEditModalOpen.value = true;
}

function openDeleteModal(equipment: any) {
  selectedEquipment.value = equipment;
  isDeleteModalOpen.value = true;
}

function handleSuccess() {
  emit('refresh');
}
</script>