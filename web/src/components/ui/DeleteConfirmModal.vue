<template>
  <BaseModal :show="show" @close="close" title="Confirmar Eliminación">
    <div class="space-y-4">
      <div class="flex items-start gap-4">
        <div class="flex-shrink-0 w-12 h-12 rounded-full bg-red-100 flex items-center justify-center">
          <span class="material-symbols-outlined text-red-600 text-2xl">
            warning
          </span>
        </div>
        <div class="flex-1">
          <h3 class="text-lg font-semibold text-gray-900 mb-2">
            ¿Estás seguro de eliminar este equipo?
          </h3>
          <p class="text-gray-600 mb-4">
            Esta acción no se puede deshacer. El equipo <strong>{{ equipment?.name }}</strong> será eliminado permanentemente del sistema.
          </p>
          <div class="bg-gray-50 rounded-lg p-3 border border-gray-200">
            <div class="text-sm text-gray-600">
              <p><strong>Serial:</strong> {{ equipment?.serial }}</p>
              <p><strong>Ubicación:</strong> {{ equipment?.location }}</p>
            </div>
          </div>
        </div>
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
        <button
          @click="confirmDelete"
          :disabled="loading"
          class="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span v-if="loading" class="material-symbols-outlined animate-spin text-sm">
            progress_activity
          </span>
          <span class="material-symbols-outlined text-lg">
            delete
          </span>
          <span>{{ loading ? 'Eliminando...' : 'Eliminar Equipo' }}</span>
        </button>
      </div>
    </div>
  </BaseModal>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import BaseModal from './BaseModal.vue';
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

async function confirmDelete() {
  if (!props.equipment?.id) {
    toast.error('Error: No se encontró el ID del equipo');
    return;
  }

  loading.value = true;
  try {
    await store.deleteEquipment(props.equipment.id);
    toast.success('✅ Equipo eliminado exitosamente');
    emit('success');
    close();
  } catch (error) {
    console.error('Error deleting equipment:', error);
    toast.error(store.error || 'Error al eliminar el equipo');
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
