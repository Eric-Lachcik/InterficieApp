import { defineStore } from 'pinia'
import { api } from 'boot/axios'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    returnUrl: null
  }),

  actions: {
    async login(credentials) {
      try {
        const response = await api.post('/api/auth/login/', credentials)
        localStorage.setItem('auth_token', response.data.access)
        this.user = {
          id: response.data.user_id,
          username: response.data.username,
          role: response.data.role
        }
        return true
      } catch (error) {
        console.error('Login error:', error.response?.data)
        throw error
      }
    },

    logout() {
      localStorage.removeItem('auth_token')
      this.user = null
    }
  }
})