<template>
  <BaseModal :show="show" @close="close" title="Editar Equipo">
    <form @submit.prevent="submitForm" class="space-y-4">
      <div>
        <label for="edit-name" class="block text-sm font-medium text-gray-700 mb-1">Nombre *</label>
        <input 
          type="text" 
          id="edit-name" 
          v-model="form.name" 
          required
          class="w-full border border-gray-300 rounded-lg shadow-sm py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
      </div>

      <div>
        <label for="edit-serial" class="block text-sm font-medium text-gray-700 mb-1">Serial *</label>
        <input 
          type="text" 
          id="edit-serial" 
          v-model="form.serial" 
          required
          disabled
          class="w-full border border-gray-300 rounded-lg shadow-sm py-2 px-3 bg-gray-50 text-gray-500 cursor-not-allowed"
          title="El serial no se puede modificar"
        >
      </div>

      <div>
        <label for="edit-type" class="block text-sm font-medium text-gray-700 mb-1">Tipo *</label>
        <select 
          id="edit-type" 
          v-model="form.type" 
          required
          class="w-full border border-gray-300 rounded-lg shadow-sm py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <option value="Laptop">Laptop</option>
          <option value="Desktop">Desktop</option>
          <option value="Servidor">Servidor</option>
          <option value="Impresora">Impresora</option>
          <option value="Proyector">Proyector</option>
          <option value="Router">Router</option>
          <option value="Switch">Switch</option>
        </select>
      </div>

      <div>
        <label for="edit-location" class="block text-sm font-medium text-gray-700 mb-1">Ubicación *</label>
        <input 
          type="text" 
          id="edit-location" 
          v-model="form.location" 
          required
          class="w-full border border-gray-300 rounded-lg shadow-sm py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
      </div>

      <div>
        <label for="edit-status" class="block text-sm font-medium text-gray-700 mb-1">Estado *</label>
        <select 
          id="edit-status" 
          v-model="form.status" 
          required
          class="w-full border border-gray-300 rounded-lg shadow-sm py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <option value="Operativo">Operativo</option>
          <option value="Mantenimiento">Mantenimiento</option>
          <option value="Fuera de Servicio">Fuera de Servicio</option>
        </select>
      </div>

      <div>
        <label for="edit-image_url" class="block text-sm font-medium text-gray-700 mb-1">URL de Imagen (opcional)</label>
        <input 
          type="text" 
          id="edit-image_url" 
          v-model="form.image_url" 
          placeholder="https://ejemplo.com/imagen.jpg (opcional)"
          class="w-full border border-gray-300 rounded-lg shadow-sm py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
        <p class="text-xs text-gray-500 mt-1">Puedes dejarlo vacío si no tienes una imagen</p>
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
          <span>{{ loading ? 'Guardando...' : 'Guardar Cambios' }}</span>
        </BaseButton>
      </div>
    </form>
  </BaseModal>
</template>

<script lang="ts" setup>
import { ref, watch } from 'vue';
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
  name: '',
  serial: '',
  type: '',
  location: '',
  status: 'Operativo',
  image_url: '',
});

// Watch for equipment prop changes and populate form
watch(() => props.equipment, (newEquipment) => {
  if (newEquipment) {
    form.value = {
      name: newEquipment.name || '',
      serial: newEquipment.serial || '',
      type: newEquipment.type || '',
      location: newEquipment.location || '',
      status: newEquipment.status || 'Operativo',
      image_url: newEquipment.image_url || '',
    };
  }
}, { immediate: true });

async function submitForm() {
  if (!props.equipment?.id) {
    toast.error('Error: No se encontró el ID del equipo');
    return;
  }

  loading.value = true;
  try {
    await store.updateEquipment(props.equipment.id, form.value);
    toast.success('✅ Equipo actualizado exitosamente');
    emit('success');
    close();
  } catch (error) {
    console.error('Error updating equipment:', error);
    toast.error(store.error || 'Error al actualizar el equipo');
  } finally {
    loading.value = false;
  }
}

function close() {
  if (!loading.value) {
    emit('close');
  }
}
</script>
