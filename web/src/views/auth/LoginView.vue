<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-600 via-purple-600 to-indigo-700 p-4">
    <!-- Background Pattern -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute -top-40 -right-40 w-80 h-80 bg-white opacity-10 rounded-full blur-3xl"></div>
      <div class="absolute -bottom-40 -left-40 w-80 h-80 bg-white opacity-10 rounded-full blur-3xl"></div>
    </div>

    <!-- Login Card -->
    <div class="relative w-full max-w-md">
      <div class="bg-white/95 backdrop-blur-xl rounded-2xl shadow-2xl p-8 border border-white/20">
        <!-- Logo/Title -->
        <div class="text-center mb-8">
          <div class="w-16 h-16 bg-gradient-to-br from-blue-600 to-purple-600 rounded-2xl mx-auto mb-4 flex items-center justify-center">
            <span class="material-symbols-outlined text-white text-3xl">
              monitor_heart
            </span>
          </div>
          <h1 class="text-3xl font-bold text-gray-900 mb-2">
            Device Monitoring
          </h1>
          <p class="text-gray-600">
            Ingresa tu correo para continuar
          </p>
        </div>

        <!-- Error Message -->
        <div 
          v-if="authStore.error" 
          class="mb-6 p-4 bg-red-50 border border-red-200 rounded-xl flex items-start gap-3"
        >
          <span class="material-symbols-outlined text-red-600 text-xl">
            error
          </span>
          <p class="text-red-800 text-sm">{{ authStore.error }}</p>
        </div>

        <!-- Success Message -->
        <div 
          v-if="showSuccess" 
          class="mb-6 p-4 bg-green-50 border border-green-200 rounded-xl flex items-start gap-3"
        >
          <span class="material-symbols-outlined text-green-600 text-xl">
            check_circle
          </span>
          <p class="text-green-800 text-sm">
            Código enviado a <strong>{{ email }}</strong>
          </p>
        </div>

        <!-- Login Form -->
        <form @submit.prevent="handleSubmit">
          <div class="mb-6">
            <label 
              for="email" 
              class="block text-sm font-medium text-gray-700 mb-2"
            >
              Correo electrónico
            </label>
            <div class="relative">
              <span class="absolute left-4 top-1/2 -translate-y-1/2 material-symbols-outlined text-gray-400">
                mail
              </span>
              <input
                id="email"
                v-model="email"
                type="email"
                required
                placeholder="tu@email.com"
                class="w-full pl-12 pr-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                :disabled="authStore.isLoading"
              />
            </div>
          </div>

          <!-- Submit Button -->
          <button
            type="submit"
            :disabled="authStore.isLoading || !email"
            class="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white font-semibold py-3 rounded-xl hover:shadow-lg hover:scale-[1.02] transition-all disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100 flex items-center justify-center gap-2"
          >
            <span v-if="authStore.isLoading" class="material-symbols-outlined animate-spin">
              progress_activity
            </span>
            <span v-else class="material-symbols-outlined">
              send
            </span>
            <span>{{ authStore.isLoading ? 'Enviando...' : 'Enviar código OTP' }}</span>
          </button>
        </form>

        <!-- Footer Info -->
        <div class="mt-8 pt-6 border-t border-gray-200">
          <p class="text-center text-sm text-gray-600">
            <span class="material-symbols-outlined text-base align-middle mr-1">
              info
            </span>
            Recibirás un código de 6 dígitos por correo
          </p>
        </div>
      </div>

      <!-- Bottom Info -->
      <div class="text-center mt-6 text-white/80 text-sm">
        <p>Sistema de Monitoreo de Equipos</p>
        <p class="mt-1">© 2024 Device Monitoring. Todos los derechos reservados.</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../stores/authStore'

const router = useRouter()
const authStore = useAuthStore()

const email = ref('')
const showSuccess = ref(false)

async function handleSubmit() {
  if (!email.value) return

  try {
    await authStore.requestOTP(email.value)
    showSuccess.value = true
    
    // Redirect to OTP verification after 1 second
    setTimeout(() => {
      router.push({ 
        name: 'otp-verification', 
        query: { email: email.value } 
      })
    }, 1000)
  } catch (error) {
    console.error('Error requesting OTP:', error)
    showSuccess.value = false
  }
}
</script>
