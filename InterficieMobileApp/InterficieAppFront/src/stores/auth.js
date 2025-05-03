import { defineStore } from 'pinia'
import { api } from 'boot/axios'

export const useAuthStore = defineStore('auth', {
  actions: {
    async login(credentials) {
      try {
        const response = await api.post('/api/auth/login/', credentials);
        
        localStorage.setItem('auth_token', response.data.access);

        this.user = {
          id: response.data.user_id,
          username: response.data.username,
          name: response.data.name,
          surname: response.data.surname,
          role: response.data.role,
          isStaff: response.data.is_staff // Asegúrate de que viene del backend
        };
        console.log(this.user)
        // Redirección basada en staff
        if (this.user.isStaff) {
          this.router.push('/staff-dashboard');
        } else {
          this.router.push('/client-dashboard');
        }
        
        return true;
      } catch (error) {
        // Manejo de errores mejorado
        if (error.response?.status === 401) {
          throw new Error('Credenciales incorrectas')
        }
        throw new Error('Error de conexión')
      }
    }
  }
})