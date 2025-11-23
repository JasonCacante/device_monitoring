<template>
  <header class="flex items-center justify-between whitespace-nowrap border-b border-border-light/50 px-10 py-5 bg-white/80 backdrop-blur-lg shadow-sm">
    <div class="flex items-center gap-8">
      <label class="relative flex flex-col min-w-40 w-96">
        <div class="flex w-full flex-1 items-stretch rounded-xl h-11 bg-slate-100 hover:bg-slate-200 transition-colors shadow-sm">
          <div class="text-text-secondary flex items-center justify-center pl-4">
            <span class="material-symbols-outlined text-blue-600">search</span>
          </div>
          <input class="form-input flex w-full min-w-0 flex-1 resize-none overflow-hidden rounded-xl text-text-primary focus:outline-none focus:ring-2 focus:ring-blue-500 border-none bg-transparent h-full placeholder:text-text-secondary pl-2 text-sm font-medium leading-normal" placeholder="Search for machines or users...">
        </div>
      </label>
    </div>
    <div class="flex flex-1 justify-end gap-4 items-center">
        <button class="relative p-2 text-text-secondary hover:text-blue-600 hover:bg-blue-50 rounded-xl transition-all duration-200">
          <span class="material-symbols-outlined">notifications</span>
          <span class="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
        </button>
        <div class="flex items-center gap-3 pl-4 border-l border-border-light relative">
          <div class="text-right">
            <p class="text-sm font-semibold text-text-primary">{{ authStore.currentUser?.name || 'Usuario' }}</p>
            <p class="text-xs text-text-secondary capitalize">{{ getRoleDisplay(authStore.currentUser?.role) }}</p>
          </div>
          <button @click="toggleDropdown" class="relative">
            <div 
              class="bg-center bg-no-repeat aspect-square bg-cover rounded-full size-11 ring-2 ring-blue-200 hover:ring-blue-400 transition-all cursor-pointer" 
              :style="`background-image: url('${authStore.currentUser?.avatar_url || 'https://randomuser.me/api/portraits/lego/1.jpg'}')`"
            ></div>
          </button>
          
          <!-- Dropdown Menu -->
          <div 
            v-if="showDropdown" 
            class="absolute top-full right-0 mt-2 w-56 bg-white rounded-xl shadow-lg border border-gray-200 py-2 z-50"
          >
            <div class="px-4 py-3 border-b border-gray-200">
              <p class="text-sm font-semibold text-gray-900">{{ authStore.currentUser?.email }}</p>
              <p class="text-xs text-gray-500 mt-1 capitalize">{{ getRoleDisplay(authStore.currentUser?.role) }}</p>
            </div>
            
            <button
              @click="handleLogout"
              class="w-full px-4 py-2.5 text-left text-sm text-red-600 hover:bg-red-50 transition-colors flex items-center gap-2"
            >
              <span class="material-symbols-outlined text-lg">logout</span>
              <span>Cerrar sesión</span>
            </button>
          </div>
        </div>
    </div>
  </header>
</template>

<script lang="ts" setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../../stores/authStore';

const router = useRouter();
const authStore = useAuthStore();
const showDropdown = ref(false);

function toggleDropdown() {
  showDropdown.value = !showDropdown.value;
}

function getRoleDisplay(role: string | undefined): string {
  if (!role) return 'Usuario';
  
  const roleMap: Record<string, string> = {
    admin: 'Administrador',
    staff: 'Personal',
    customer: 'Cliente'
  };
  
  return roleMap[role] || role;
}

function handleLogout() {
  authStore.logout();
  router.push({ name: 'login' });
}

// Close dropdown when clicking outside
function handleClickOutside(event: MouseEvent) {
  const target = event.target as HTMLElement;
  if (!target.closest('.relative')) {
    showDropdown.value = false;
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside);
});

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside);
});
</script>