<template>
  <BaseModal :show="show" @close="close" title="Crear Nuevo Usuario">
    <form @submit.prevent="submitForm" class="space-y-4">
      <div>
        <label for="email" class="block text-sm font-medium text-gray-700 mb-1">Email *</label>
        <input 
          type="email" 
          id="email" 
          v-model="form.email" 
          required
          class="w-full border border-gray-300 rounded-lg shadow-sm py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="usuario@ejemplo.com"
        >
      </div>

      <div>
        <label for="name" class="block text-sm font-medium text-gray-700 mb-1">Nombre Completo *</label>
        <input 
          type="text" 
          id="name" 
          v-model="form.name" 
          required
          class="w-full border border-gray-300 rounded-lg shadow-sm py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="Juan Pérez"
        >
      </div>

      <div>
        <label for="role" class="block text-sm font-medium text-gray-700 mb-1">Rol *</label>
        <select 
          id="role" 
          v-model="form.role" 
          required
          class="w-full border border-gray-300 rounded-lg shadow-sm py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        >
          <option value="admin">Administrador</option>
          <option value="staff">Personal</option>
          <option value="customer">Cliente</option>
        </select>
      </div>

      <div>
        <label for="avatar_url" class="block text-sm font-medium text-gray-700 mb-1">URL de Avatar (opcional)</label>
        <input 
          type="text" 
          id="avatar_url" 
          v-model="form.avatar_url" 
          class="w-full border border-gray-300 rounded-lg shadow-sm py-2 px-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="https://ejemplo.com/avatar.jpg"
        >
        <p class="text-xs text-gray-500 mt-1">Si no se proporciona, se usará un avatar predeterminado</p>
      </div>

      <div class="bg-blue-50 border border-blue-200 rounded-lg p-3 flex items-start gap-2">
        <span class="material-symbols-outlined text-blue-600 text-lg">info</span>
        <p class="text-sm text-blue-800">
          El usuario recibirá un código OTP en su email para poder iniciar sesión por primera vez.
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
          <span>{{ loading ? 'Creando...' : 'Crear Usuario' }}</span>
        </BaseButton>
      </div>
    </form>
  </BaseModal>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import BaseModal from './BaseModal.vue';
import BaseButton from './BaseButton.vue';
import { useToast } from 'vue-toastification';
import apiClient from '../../services/api';

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
  email: '',
  name: '',
  role: 'staff',
  avatar_url: '',
});

async function submitForm() {
  loading.value = true;
  try {
    await apiClient.post('/users', form.value);
    toast.success('✅ Usuario creado exitosamente');
    resetForm();
    emit('success');
    close();
  } catch (error: any) {
    console.error('Error creating user:', error);
    toast.error(error.response?.data?.detail || 'Error al crear el usuario');
  } finally {
    loading.value = false;
  }
}

function resetForm() {
  form.value = {
    email: '',
    name: '',
    role: 'staff',
    avatar_url: '',
  };
}

function close() {
  if (!loading.value) {
    resetForm();
    emit('close');
  }
}
</script>
