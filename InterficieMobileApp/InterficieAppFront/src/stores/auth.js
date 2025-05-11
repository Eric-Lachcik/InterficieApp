import { defineStore } from 'pinia'
import { api } from 'boot/axios'


export const useAuthStore = defineStore('auth', {
  actions: {
    state: () => ({
      user: JSON.parse(localStorage.getItem('user') || null), // Estado para el usuario
      userDetails: JSON.parse(localStorage.getItem('userDetails') || null)// Nuevo estado para datos adicionales
    }),
    async login(credentials) {
      try {
        const response = await api.post('/api/auth/login/', credentials);
        
        
        this.user = {
          id: response.data.user_id,
          username: response.data.username,
          name: response.data.name,
          surname: response.data.surname,
          role: response.data.role,
          isStaff: response.data.is_staff,
          email: response.data.email,
          phone: response.data.phone,
          dni: response.data.dni,
          address: response.data.address,
        };
        localStorage.setItem('user', JSON.stringify(this.user));
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
    },

    async fetchUserDetails(userId) {
      try {
        const response = await api.get(`/api/users/${userId}/`);
        this.userDetails = {
          name: response.data.name,
          surname: response.data.surname,
          dni: response.data.dni,
          phone: response.data.phone,
          address: response.data.address,
          population: response.data.population,
          username: response.data.username,
          email: response.data.email,
          weight: response.data.weight,
          muscle_mass: response.data.muscle_mass,
          stature: response.data.stature,
          fecha_registro: response.data.fecha_registro,
          isStaff: response.data.staff,
          role: response.data.role,
          entrenador: response.data.entrenador,
          nutricionista: response.data.nutricionista
        };
        localStorage.setItem('userDetails', JSON.stringify(this.userDetails));
      } catch (error) {
        console.error('Error fetching user details:', error);
        throw error;
      }
    },
    logout() {
      this.user = null
      this.userDetails = null
      localStorage.clear();
      this.router.push('/login')
    }
  },
})