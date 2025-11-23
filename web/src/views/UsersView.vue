<template>
  <div class="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
    <!-- Header -->
    <Header />

    <div class="flex">
      <!-- Sidebar -->
      <aside class="w-64 min-h-screen bg-white border-r border-gray-200 p-6">
        <div class="flex items-center gap-3 mb-8">
          <div class="w-12 h-12 bg-gradient-to-br from-blue-600 to-purple-600 rounded-xl flex items-center justify-center">
            <span class="material-symbols-outlined text-white text-2xl">directions_car</span>
          </div>
          <div>
            <p class="font-bold text-gray-900">Machine Fleet</p>
            <p class="text-sm text-gray-500">Management System</p>
          </div>
        </div>

        <nav class="space-y-2">
          <router-link to="/" class="flex items-center gap-3 px-4 py-3 text-gray-600 hover:bg-blue-50 hover:text-blue-600 rounded-xl transition-colors">
            <span class="material-symbols-outlined">dashboard</span>
            <span class="font-medium">Dashboard</span>
          </router-link>
          <router-link to="/equipos" class="flex items-center gap-3 px-4 py-3 text-gray-600 hover:bg-blue-50 hover:text-blue-600 rounded-xl transition-colors">
            <span class="material-symbols-outlined">precision_manufacturing</span>
            <span class="font-medium">Machines</span>
          </router-link>
          <router-link to="/users" class="flex items-center gap-3 px-4 py-3 bg-blue-50 text-blue-600 rounded-xl transition-colors">
            <span class="material-symbols-outlined">group</span>
            <span class="font-medium">Users</span>
          </router-link>
          <button disabled class="flex items-center gap-3 px-4 py-3 text-gray-400 rounded-xl w-full cursor-not-allowed">
            <span class="material-symbols-outlined">settings</span>
            <span class="font-medium">Settings</span>
            <span class="ml-auto text-xs">(Soon)</span>
          </button>
        </nav>

        <button @click="handleLogout" class="flex items-center gap-3 px-4 py-3 text-red-600 hover:bg-red-50 rounded-xl transition-colors w-full mt-auto absolute bottom-6">
          <span class="material-symbols-outlined">logout</span>
          <span class="font-medium">Logout</span>
        </button>
      </aside>

      <!-- Main Content -->
      <main class="flex-1 p-8">
        <!-- Header Section -->
        <div class="mb-8">
          <h1 class="text-4xl font-bold text-gray-900 mb-2">Gestión de Usuarios 👥</h1>
          <p class="text-gray-600">Administra los usuarios del sistema y sus roles</p>
        </div>

        <!-- Actions Bar -->
        <div class="flex justify-between items-center mb-6">
          <div class="flex-1 max-w-md">
            <InputSearch v-model="searchQuery" placeholder="Buscar por nombre o email..." />
          </div>
          <button
            @click="showNewUserModal = true"
            class="flex items-center gap-2 px-4 py-2 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl hover:shadow-lg transition-all"
          >
            <span class="material-symbols-outlined">person_add</span>
            <span class="font-medium">Nuevo Usuario</span>
          </button>
        </div>

        <!-- Users Table -->
        <div class="bg-white rounded-2xl shadow-sm border border-gray-200 overflow-hidden">
          <div v-if="loading" class="p-12 text-center">
            <span class="material-symbols-outlined animate-spin text-4xl text-blue-600">progress_activity</span>
            <p class="text-gray-600 mt-4">Cargando usuarios...</p>
          </div>

          <div v-else-if="error" class="p-12 text-center">
            <span class="material-symbols-outlined text-4xl text-red-600">error</span>
            <p class="text-red-600 mt-4">{{ error }}</p>
          </div>

          <table v-else class="w-full">
            <thead class="bg-gray-50 border-b border-gray-200">
              <tr>
                <th class="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase">Usuario</th>
                <th class="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase">Email</th>
                <th class="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase">Rol</th>
                <th class="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase">Creado</th>
                <th class="px-6 py-4 text-right text-xs font-semibold text-gray-600 uppercase">Acciones</th>
              </tr>
            </thead>
            <tbody class="divide-y divide-gray-200">
              <tr v-for="user in filteredUsers" :key="user.id" class="hover:bg-gray-50 transition-colors">
                <td class="px-6 py-4">
                  <div class="flex items-center gap-3">
                    <img 
                      :src="user.avatar_url || `https://ui-avatars.com/api/?name=${user.name}&background=random`" 
                      :alt="user.name"
                      class="w-10 h-10 rounded-full ring-2 ring-gray-200"
                    >
                    <span class="font-medium text-gray-900">{{ user.name }}</span>
                  </div>
                </td>
                <td class="px-6 py-4 text-gray-600">{{ user.email }}</td>
                <td class="px-6 py-4">
                  <span :class="getRoleBadgeClass(user.role)" class="px-3 py-1 rounded-full text-xs font-medium">
                    {{ getRoleDisplay(user.role) }}
                  </span>
                </td>
                <td class="px-6 py-4 text-gray-600 text-sm">
                  {{ formatDate(user.created_at) }}
                </td>
                <td class="px-6 py-4 text-right">
                  <button
                    v-if="user.id !== currentUser?.id"
                    @click="deleteUser(user)"
                    class="text-red-600 hover:bg-red-50 p-2 rounded-lg transition-colors"
                    title="Eliminar usuario"
                  >
                    <span class="material-symbols-outlined">delete</span>
                  </button>
                  <span v-else class="text-gray-400 text-sm">
                    (Tú)
                  </span>
                </td>
              </tr>
            </tbody>
          </table>

          <div v-if="!loading && filteredUsers.length === 0" class="p-12 text-center">
            <span class="material-symbols-outlined text-4xl text-gray-400">group_off</span>
            <p class="text-gray-600 mt-4">No se encontraron usuarios</p>
          </div>
        </div>
      </main>
    </div>

    <!-- New User Modal -->
    <NewUserModal :show="showNewUserModal" @close="showNewUserModal = false" @success="handleUserCreated" />
  </div>
</template>

<script lang="ts" setup>
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/authStore';
import { useToast } from 'vue-toastification';
import Header from '../components/layout/Header.vue';
import InputSearch from '../components/ui/InputSearch.vue';
import NewUserModal from '../components/ui/NewUserModal.vue';
import apiClient from '../services/api';

const router = useRouter();
const authStore = useAuthStore();
const toast = useToast();

const users = ref<any[]>([]);
const loading = ref(false);
const error = ref<string | null>(null);
const searchQuery = ref('');
const showNewUserModal = ref(false);

const currentUser = computed(() => authStore.currentUser);

const filteredUsers = computed(() => {
  if (!searchQuery.value) return users.value;
  const query = searchQuery.value.toLowerCase();
  return users.value.filter(
    user => 
      user.name.toLowerCase().includes(query) || 
      user.email.toLowerCase().includes(query)
  );
});

function getRoleDisplay(role: string): string {
  const roleMap: Record<string, string> = {
    admin: 'Administrador',
    staff: 'Personal',
    customer: 'Cliente'
  };
  return roleMap[role] || role;
}

function getRoleBadgeClass(role: string): string {
  const classMap: Record<string, string> = {
    admin: 'bg-purple-100 text-purple-700',
    staff: 'bg-blue-100 text-blue-700',
    customer: 'bg-green-100 text-green-700'
  };
  return classMap[role] || 'bg-gray-100 text-gray-700';
}

function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return date.toLocaleDateString('es-ES', { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric' 
  });
}

async function fetchUsers() {
  loading.value = true;
  error.value = null;
  try {
    const response = await apiClient.get('/users');
    users.value = response.data;
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Error al cargar los usuarios';
    toast.error(error.value);
  } finally {
    loading.value = false;
  }
}

async function deleteUser(user: any) {
  if (!confirm(`¿Estás seguro de eliminar al usuario ${user.name}?`)) return;

  try {
    await apiClient.delete(`/users/${user.id}`);
    toast.success('✅ Usuario eliminado exitosamente');
    await fetchUsers();
  } catch (err: any) {
    toast.error(err.response?.data?.detail || 'Error al eliminar el usuario');
  }
}

function handleUserCreated() {
  fetchUsers();
}

function handleLogout() {
  authStore.logout();
  router.push({ name: 'login' });
}

onMounted(() => {
  fetchUsers();
});
</script>
