<template>
  <BaseModal :show="show" @close="close" title="Solicitar Mantenimiento">
    <form @submit.prevent="submitForm" class="space-y-4">
      <div class="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-4">
        <div class="flex items-start gap-3">
          <span class="material-symbols-outlined text-blue-600 text-2xl">
            info
          </span>
          <div>
            <h4 class="font-semibold text-blue-900 mb-1">Equipo Seleccionado</h4>
            <p class="text-blue-700 text-sm"><strong>{{ equipment?.name }}</strong></p>
            <p class="text-blue-600 text-sm">Serial: {{ equipment?.serial }}</p>
          </div>
        </div>
      </div>

      <div>
        <label for="maintenance-type" class="block text-sm font-medium text-gray-700 mb-1">Tipo de Mantenimiento *</label>
        <select 
          id="maintenance-type" 
          v-model="form.maintenance_type" 
          required
          class="w-full border border-gray-300 rounded-lg shadow-sm py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <option value="">Seleccionar tipo</option>
          <option value="Preventivo">Preventivo</option>
          <option value="Correctivo">Correctivo</option>
          <option value="Inspección">Inspección</option>
          <option value="Actualización">Actualización</option>
        </select>
      </div>

      <div>
        <label for="scheduled_date" class="block text-sm font-medium text-gray-700 mb-1">Fecha Preferida *</label>
        <input 
          type="date" 
          id="scheduled_date" 
          v-model="form.scheduled_date" 
          required
          :min="minDate"
          class="w-full border border-gray-300 rounded-lg shadow-sm py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
      </div>

      <div>
        <label for="description" class="block text-sm font-medium text-gray-700 mb-1">Descripción del Problema *</label>
        <textarea 
          id="description" 
          v-model="form.description" 
          required
          rows="4"
          class="w-full border border-gray-300 rounded-lg shadow-sm py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
          placeholder="Describe el problema o la razón del mantenimiento..."
        ></textarea>
      </div>

      <div>
        <label for="priority" class="block text-sm font-medium text-gray-700 mb-1">Prioridad *</label>
        <select 
          id="priority" 
          v-model="form.priority" 
          required
          class="w-full border border-gray-300 rounded-lg shadow-sm py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <option value="Baja">Baja</option>
          <option value="Media">Media</option>
          <option value="Alta">Alta</option>
          <option value="Urgente">Urgente</option>
        </select>
      </div>

      <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-3">
        <p class="text-yellow-800 text-sm">
          <span class="material-symbols-outlined text-base align-middle mr-1">schedule</span>
          Nuestro equipo revisará tu solicitud y te contactará en las próximas 24 horas.
        </p>
      </div>

      <div class="flex justify-end gap-3 pt-4 border-t">
        <button
          type="button"
          @click="close"
          class="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
          :disabled="loading"
        >
          Cancelar
        </button>
        <BaseButton 
          type="submit" 
          :disabled="loading"
          class="flex items-center gap-2"
        >
          <span v-if="loading" class="material-symbols-outlined animate-spin text-sm">
            progress_activity
          </span>
          <span class="material-symbols-outlined text-lg">
            send
          </span>
          <span>{{ loading ? 'Enviando...' : 'Enviar Solicitud' }}</span>
        </BaseButton>
      </div>
    </form>
  </BaseModal>
</template>

<script lang="ts" setup>
import { ref, computed } from 'vue';
import BaseModal from './BaseModal.vue';
import BaseButton from './BaseButton.vue';
import { useEquipmentStore } from '../../stores/equipmentStore';
import { useToast } from 'vue-toastification';

const store = useEquipmentStore();
const toast = useToast();

const props = defineProps({
  show: {
    type: Boolean,
    required: true,
  },
  equipment: {
    type: Object as () => any,
    default: null,
  },
});

const emit = defineEmits(['close', 'success']);

const loading = ref(false);

const form = ref({
  maintenance_type: '',
  scheduled_date: '',
  description: '',
  priority: 'Media',
  status: 'Pendiente',
});

const minDate = computed(() => {
  const tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1);
  return tomorrow.toISOString().split('T')[0];
});

async function submitForm() {
  if (!props.equipment?.id) {
    toast.error('Error: No se encontró el ID del equipo');
    return;
  }

  loading.value = true;
  try {
    await store.createMaintenance(props.equipment.id, form.value);
    toast.success('✅ Solicitud de mantenimiento enviada exitosamente');
    resetForm();
    emit('success');
    close();
  } catch (error) {
    console.error('Error creating maintenance request:', error);
    toast.error(store.error || 'Error al enviar la solicitud');
  } finally {
    loading.value = false;
  }
}

function resetForm() {
  form.value = {
    maintenance_type: '',
    scheduled_date: '',
    description: '',
    priority: 'Media',
    status: 'Pendiente',
  };
}

function close() {
  if (!loading.value) {
    resetForm();
    emit('close');
  }
}
</script>
