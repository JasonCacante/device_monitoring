<template>
  <div class="flex h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 font-sans">
    <!-- Sidebar -->
    <aside class="w-72 bg-white/80 backdrop-blur-xl border-r border-blue-100 shadow-xl flex-shrink-0">
      <div class="h-24 flex items-center justify-center px-6 border-b border-blue-100">
        <div class="flex items-center">
          <div class="w-12 h-12 bg-gradient-to-br from-blue-600 to-indigo-600 text-white rounded-2xl flex items-center justify-center mr-3 shadow-lg">
            <span class="material-symbols-outlined text-2xl">directions_car</span>
          </div>
          <div>
            <p class="text-lg font-bold text-text-primary">Machine Fleet</p>
            <p class="text-xs text-text-secondary font-medium">Management System</p>
          </div>
        </div>
      </div>
      <nav class="mt-6 px-4 space-y-2">
        <router-link to="/" class="flex items-center py-3.5 px-4 text-text-secondary hover:bg-gradient-to-r hover:from-blue-50 hover:to-indigo-50 hover:text-blue-600 rounded-xl transition-all duration-200 group" active-class="bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-lg">
          <span class="material-symbols-outlined mr-3 text-xl group-hover:scale-110 transition-transform">dashboard</span>
          <span class="font-semibold">Dashboard</span>
        </router-link>
        <router-link to="/equipos" class="flex items-center py-3.5 px-4 text-text-secondary hover:bg-gradient-to-r hover:from-blue-50 hover:to-indigo-50 hover:text-blue-600 rounded-xl transition-all duration-200 group" active-class="bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-lg">
          <span class="material-symbols-outlined mr-3 text-xl group-hover:scale-110 transition-transform">precision_manufacturing</span>
          <span class="font-semibold">Machines</span>
        </router-link>
        <router-link to="/users" class="flex items-center py-3.5 px-4 text-text-secondary hover:bg-gradient-to-r hover:from-blue-50 hover:to-indigo-50 hover:text-blue-600 rounded-xl transition-all duration-200 group" active-class="bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-lg">
          <span class="material-symbols-outlined mr-3 text-xl group-hover:scale-110 transition-transform">group</span>
          <span class="font-semibold">Users</span>
        </router-link>
        <button class="flex items-center py-3.5 px-4 text-text-secondary hover:bg-gradient-to-r hover:from-blue-50 hover:to-indigo-50 hover:text-blue-600 rounded-xl transition-all duration-200 group w-full text-left opacity-50 cursor-not-allowed" disabled>
          <span class="material-symbols-outlined mr-3 text-xl">settings</span>
          <span class="font-semibold">Settings</span>
          <span class="ml-auto text-xs">(Soon)</span>
        </button>
      </nav>
      <div class="absolute bottom-0 w-72 p-6 border-t border-blue-100">
        <button class="flex items-center py-3.5 px-4 text-text-secondary hover:bg-red-50 hover:text-red-600 w-full rounded-xl transition-all duration-200 group">
          <span class="material-symbols-outlined mr-3 text-xl group-hover:scale-110 transition-transform">logout</span>
          <span class="font-semibold">Logout</span>
        </button>
      </div>
    </aside>

    <div class="flex-1 flex flex-col overflow-hidden">
      <!-- Header is now a separate component -->
      <slot name="header"></slot>

      <!-- Main Content -->
      <main class="flex-1 overflow-x-hidden overflow-y-auto">
        <slot></slot>
      </main>
    </div>
  </div>
</template>

<script lang="ts" setup>
// No specific logic for a main layout, it just provides structure.
</script>