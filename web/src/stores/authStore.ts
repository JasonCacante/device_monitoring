import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import api from '../services/api'

export interface User {
  id: number
  email: string
  name: string
  avatar_url: string | null
  role: 'admin' | 'staff' | 'customer'
  created_at: string
}

export interface OTPResponse {
  otp_code: string
  email: string
  expires_in_minutes: number
}

export interface AuthResponse {
  access_token: string
  token_type: string
  user: User
}

export const useAuthStore = defineStore('auth', () => {
  // State
  const currentUser = ref<User | null>(null)
  const token = ref<string | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // Computed
  const isAuthenticated = computed(() => !!token.value && !!currentUser.value)
  const userRole = computed(() => currentUser.value?.role || null)

  // Actions
  async function requestOTP(email: string): Promise<OTPResponse> {
    isLoading.value = true
    error.value = null
    try {
      const response = await api.post<OTPResponse>('/auth/request-otp', { email })
      return response.data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Error al solicitar OTP'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function verifyOTP(email: string, otp_code: string): Promise<void> {
    isLoading.value = true
    error.value = null
    try {
      const response = await api.post<AuthResponse>('/auth/verify-otp', { 
        email, 
        otp_code 
      })
      
      // Store token and user data
      token.value = response.data.access_token
      currentUser.value = response.data.user
      
      // Store token in localStorage for persistence
      localStorage.setItem('auth_token', response.data.access_token)
      localStorage.setItem('user', JSON.stringify(response.data.user))
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Código OTP inválido o expirado'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function fetchCurrentUser(): Promise<void> {
    isLoading.value = true
    error.value = null
    try {
      const response = await api.get<User>('/auth/me')
      currentUser.value = response.data
      
      // Update user in localStorage
      localStorage.setItem('user', JSON.stringify(response.data))
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Error al obtener usuario'
      // If token is invalid, clear auth state
      if (err.response?.status === 401) {
        logout()
      }
      throw err
    } finally {
      isLoading.value = false
    }
  }

  function logout(): void {
    token.value = null
    currentUser.value = null
    error.value = null
    
    // Clear localStorage
    localStorage.removeItem('auth_token')
    localStorage.removeItem('user')
  }

  function restoreSession(): void {
    // Restore from localStorage on app initialization
    const storedToken = localStorage.getItem('auth_token')
    const storedUser = localStorage.getItem('user')
    
    if (storedToken && storedUser) {
      token.value = storedToken
      try {
        currentUser.value = JSON.parse(storedUser)
      } catch (err) {
        console.error('Error parsing stored user:', err)
        logout()
      }
    }
  }

  function hasRole(allowedRoles: string[]): boolean {
    if (!currentUser.value) return false
    return allowedRoles.includes(currentUser.value.role)
  }

  return {
    // State
    currentUser,
    token,
    isLoading,
    error,
    
    // Computed
    isAuthenticated,
    userRole,
    
    // Actions
    requestOTP,
    verifyOTP,
    fetchCurrentUser,
    logout,
    restoreSession,
    hasRole
  }
})
