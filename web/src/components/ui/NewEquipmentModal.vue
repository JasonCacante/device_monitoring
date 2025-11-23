<template>
  <BaseModal :show="show" @close="close" title="Crear Nuevo Equipo">
    <form @submit.prevent="submitForm" class="space-y-4">
      <div>
        <label for="name" class="block text-sm font-medium text-gray-700 mb-1">Nombre *</label>
        <input 
          type="text" 
          id="name" 
          v-model="form.name" 
          required
          class="w-full border border-gray-300 rounded-lg shadow-sm py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="Ej: Laptop Dell XPS 15"
        >
      </div>

      <div>
        <label for="serial" class="block text-sm font-medium text-gray-700 mb-1">Serial *</label>
        <input 
          type="text" 
          id="serial" 
          v-model="form.serial" 
          required
          class="w-full border border-gray-300 rounded-lg shadow-sm py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="Ej: SN123456789"
        >
      </div>

      <div>
        <label for="type" class="block text-sm font-medium text-gray-700 mb-1">Tipo *</label>
        <select 
          id="type" 
          v-model="form.type" 
          required
          class="w-full border border-gray-300 rounded-lg shadow-sm py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <option value="">Seleccionar tipo</option>
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
        <label for="location" class="block text-sm font-medium text-gray-700 mb-1">Ubicación *</label>
        <input 
          type="text" 
          id="location" 
          v-model="form.location" 
          required
          class="w-full border border-gray-300 rounded-lg shadow-sm py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="Ej: Oficina Principal - Piso 3"
        >
      </div>

      <div>
        <label for="status" class="block text-sm font-medium text-gray-700 mb-1">Estado *</label>
        <select 
          id="status" 
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
        <label for="image_url" class="block text-sm font-medium text-gray-700 mb-1">URL de Imagen (opcional)</label>
        <input 
          type="text" 
          id="image_url" 
          v-model="form.image_url" 
          class="w-full border border-gray-300 rounded-lg shadow-sm py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="https://ejemplo.com/imagen.jpg (opcional)"
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
          <span>{{ loading ? 'Creando...' : 'Crear Equipo' }}</span>
        </BaseButton>
      </div>
    </form>
  </BaseModal>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
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

async function submitForm() {
  if (!form.value.name || !form.value.serial || !form.value.type || !form.value.location) {
    toast.error('Por favor completa todos los campos requeridos');
    return;
  }

  loading.value = true;
  try {
    await store.createEquipment(form.value);
    toast.success('✅ Equipo creado exitosamente');
    resetForm();
    emit('success');
    close();
  } catch (error) {
    console.error('Error creating equipment:', error);
    toast.error(store.error || 'Error al crear el equipo');
  } finally {
    loading.value = false;
  }
}

function resetForm() {
  form.value = {
    name: '',
    serial: '',
    type: '',
    location: '',
    status: 'Operativo',
    image_url: '',
  };
}

function close() {
  if (!loading.value) {
    resetForm();
    emit('close');
  }
}
</script>