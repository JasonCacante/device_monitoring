<template>
  <BaseModal :show="show" @close="close" title="Añadir Nuevo Mantenimiento">
    <form @submit.prevent="submitForm">
      <div class="mb-4">
        <label for="description" class="block text-sm font-medium text-gray-700">Descripción</label>
        <textarea id="description" v-model="form.description" rows="3" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary focus:border-primary sm:text-sm"></textarea>
      </div>
      <div class="mb-4">
        <label for="technician" class="block text-sm font-medium text-gray-700">Técnico</label>
        <input type="text" id="technician" v-model="form.technician" class="mt-1 block w-full border border-gray-300 rounded-md shadow-sm py-2 px-3 focus:outline-none focus:ring-primary focus:border-primary sm:text-sm">
      </div>
      <div class="flex justify-end">
        <BaseButton type="submit">Añadir</BaseButton>
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
  equipmentId: {
    type: Number,
    required: true,
  },
});

const emit = defineEmits(['close']);

const form = ref({
  description: '',
  technician: '',
});

async function submitForm() {
  // TODO: Add proper validation
  // await store.createMaintenance(props.equipmentId, form.value);
  // if (store.error) {
  //   toast.error(store.error);
  // } else {
  //   toast.success('Mantenimiento añadido con éxito');
  //   close();
  // }
  console.log("Form submitted", form.value)
  close()
}

function close() {
  emit('close');
}
</script>