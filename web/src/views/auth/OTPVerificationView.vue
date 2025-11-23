<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-600 via-purple-600 to-indigo-700 p-4">
    <!-- Background Pattern -->
    <div class="absolute inset-0 overflow-hidden pointer-events-none">
      <div class="absolute -top-40 -right-40 w-80 h-80 bg-white opacity-10 rounded-full blur-3xl"></div>
      <div class="absolute -bottom-40 -left-40 w-80 h-80 bg-white opacity-10 rounded-full blur-3xl"></div>
    </div>

    <!-- OTP Card -->
    <div class="relative w-full max-w-md">
      <div class="bg-white/95 backdrop-blur-xl rounded-2xl shadow-2xl p-8 border border-white/20">
        <!-- Back Button -->
        <button
          @click="goBack"
          class="mb-6 flex items-center gap-2 text-gray-600 hover:text-gray-900 transition-colors"
        >
          <span class="material-symbols-outlined">
            arrow_back
          </span>
          <span class="text-sm font-medium">Volver</span>
        </button>

        <!-- Icon -->
        <div class="text-center mb-8">
          <div class="w-16 h-16 bg-gradient-to-br from-green-500 to-emerald-600 rounded-2xl mx-auto mb-4 flex items-center justify-center">
            <span class="material-symbols-outlined text-white text-3xl">
              lock
            </span>
          </div>
          <h1 class="text-3xl font-bold text-gray-900 mb-2">
            Verificación
          </h1>
          <p class="text-gray-600">
            Ingresa el código de 6 dígitos enviado a
          </p>
          <p class="text-gray-900 font-medium mt-1">
            {{ email }}
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

        <!-- OTP Input -->
        <form @submit.prevent="handleSubmit">
          <div class="mb-6">
            <label class="block text-sm font-medium text-gray-700 mb-3 text-center">
              Código OTP
            </label>
            <div class="flex gap-2 justify-center">
              <input
                v-for="(digit, index) in otpDigits"
                :key="index"
                :ref="(el) => setInputRef(el as HTMLInputElement, index)"
                v-model="otpDigits[index]"
                type="text"
                inputmode="numeric"
                maxlength="1"
                class="w-12 h-14 text-center text-2xl font-bold border-2 border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                :disabled="authStore.isLoading"
                @input="handleInput(index, $event)"
                @keydown="handleKeyDown(index, $event)"
                @paste="handlePaste"
              />
            </div>
          </div>

          <!-- Submit Button -->
          <button
            type="submit"
            :disabled="authStore.isLoading || !isOTPComplete"
            class="w-full bg-gradient-to-r from-green-500 to-emerald-600 text-white font-semibold py-3 rounded-xl hover:shadow-lg hover:scale-[1.02] transition-all disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100 flex items-center justify-center gap-2"
          >
            <span v-if="authStore.isLoading" class="material-symbols-outlined animate-spin">
              progress_activity
            </span>
            <span v-else class="material-symbols-outlined">
              check_circle
            </span>
            <span>{{ authStore.isLoading ? 'Verificando...' : 'Verificar código' }}</span>
          </button>
        </form>

        <!-- Resend Code -->
        <div class="mt-6 text-center">
          <button
            v-if="!showResendTimer"
            @click="handleResend"
            class="text-blue-600 hover:text-blue-800 font-medium text-sm transition-colors"
          >
            ¿No recibiste el código? Reenviar
          </button>
          <p v-else class="text-gray-600 text-sm">
            Reenviar código en {{ resendTimer }}s
          </p>
        </div>

        <!-- Footer Info -->
        <div class="mt-8 pt-6 border-t border-gray-200">
          <p class="text-center text-sm text-gray-600">
            <span class="material-symbols-outlined text-base align-middle mr-1">
              schedule
            </span>
            El código expira en 5 minutos
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../../stores/authStore'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const email = ref((route.query.email as string) || '')
const otpDigits = ref<string[]>(['', '', '', '', '', ''])
const inputRefs = ref<(HTMLInputElement | null)[]>([])
const showResendTimer = ref(false)
const resendTimer = ref(60)
let resendInterval: number | null = null

const isOTPComplete = computed(() => 
  otpDigits.value.every(digit => digit !== '')
)

const otpCode = computed(() => otpDigits.value.join(''))

function setInputRef(el: HTMLInputElement | null, index: number) {
  if (el) {
    inputRefs.value[index] = el
  }
}

function handleInput(index: number, event: Event) {
  const input = event.target as HTMLInputElement
  const value = input.value

  // Only allow digits
  if (!/^\d*$/.test(value)) {
    otpDigits.value[index] = ''
    return
  }

  // Move to next input if filled
  if (value && index < 5) {
    inputRefs.value[index + 1]?.focus()
  }
}

function handleKeyDown(index: number, event: KeyboardEvent) {
  // Move to previous input on backspace if empty
  if (event.key === 'Backspace' && !otpDigits.value[index] && index > 0) {
    inputRefs.value[index - 1]?.focus()
  }
  
  // Move to next input on arrow right
  if (event.key === 'ArrowRight' && index < 5) {
    inputRefs.value[index + 1]?.focus()
  }
  
  // Move to previous input on arrow left
  if (event.key === 'ArrowLeft' && index > 0) {
    inputRefs.value[index - 1]?.focus()
  }
}

function handlePaste(event: ClipboardEvent) {
  event.preventDefault()
  const pastedData = event.clipboardData?.getData('text')
  
  if (pastedData && /^\d{6}$/.test(pastedData)) {
    otpDigits.value = pastedData.split('')
    inputRefs.value[5]?.focus()
  }
}

async function handleSubmit() {
  if (!isOTPComplete.value || !email.value) return

  try {
    console.log('🔄 Verificando OTP...', { email: email.value, otp: otpCode.value })
    await authStore.verifyOTP(email.value, otpCode.value)
    
    console.log('✅ OTP verificado exitosamente')
    console.log('👤 Usuario:', authStore.currentUser)
    console.log('🔑 Token:', authStore.token ? 'Presente' : 'Ausente')
    console.log('🔐 Autenticado:', authStore.isAuthenticated)
    
    // Redirect based on user role
    const role = authStore.currentUser?.role
    console.log('🎯 Rol detectado:', role)
    
    if (role === 'admin') {
      console.log('➡️  Redirigiendo a dashboard admin')
      router.push({ name: 'dashboard' })
    } else if (role === 'staff') {
      console.log('➡️  Redirigiendo a dashboard staff')
      router.push({ name: 'staff-dashboard' })
    } else if (role === 'customer') {
      console.log('➡️  Redirigiendo a dashboard customer')
      router.push({ name: 'customer-dashboard' })
    } else {
      console.log('➡️  Redirigiendo a dashboard por defecto')
      router.push({ name: 'dashboard' })
    }
  } catch (error) {
    console.error('❌ Error verifying OTP:', error)
    // Clear OTP inputs on error
    otpDigits.value = ['', '', '', '', '', '']
    inputRefs.value[0]?.focus()
  }
}

async function handleResend() {
  try {
    await authStore.requestOTP(email.value)
    
    // Clear current OTP
    otpDigits.value = ['', '', '', '', '', '']
    inputRefs.value[0]?.focus()
    
    // Start resend timer
    startResendTimer()
  } catch (error) {
    console.error('Error resending OTP:', error)
  }
}

function startResendTimer() {
  showResendTimer.value = true
  resendTimer.value = 60
  
  resendInterval = window.setInterval(() => {
    resendTimer.value--
    if (resendTimer.value <= 0) {
      showResendTimer.value = false
      if (resendInterval) {
        clearInterval(resendInterval)
      }
    }
  }, 1000)
}

function goBack() {
  router.push({ name: 'login' })
}

onMounted(() => {
  // Redirect to login if no email
  if (!email.value) {
    router.push({ name: 'login' })
    return
  }
  
  // Focus first input
  inputRefs.value[0]?.focus()
  
  // Start resend timer
  startResendTimer()
})

onUnmounted(() => {
  if (resendInterval) {
    clearInterval(resendInterval)
  }
})
</script>
