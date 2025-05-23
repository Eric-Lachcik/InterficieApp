<template>
  <div class="page-container">
    <div class="citas-register">
      <div class="profile-container">
        <GoBackButton />
        <profile-component />
      </div>
      <div class="logo-wrapper">
        <img src="FITCOREV2.2.png" class="staff-logo" alt="FITCORE Logo" />
      </div>
      <div class="form-container">
        <h2>Nueva Cita</h2>

        <form @submit.prevent="createAppointment">
          <div class="form-group">
            <label>Tipo de cita:</label>
            <select v-model="form.type" class="form-input">
              <option value="nutricionista">Nutricionista</option>
              <option value="entrenador">Entrenador Personal</option>
              <option value="clase">Clase Dirigida</option>
            </select>
          </div>

          <div class="form-group" v-if="form.type === 'clase'">
            <label>Tipo de clase:</label>
            <select v-model="form.class_type" class="form-input">
              <option value="step">Step</option>
              <option value="bodypump">Bodypump</option>
              <option value="spinning">Spinning</option>
              <option value="zumba">Zumba</option>
              <option value="crossfit">Crossfit</option>
              <option value="pilates">Pilates</option>
              <option value="yoga">Yoga</option>
            </select>
          </div>

          <div class="form-group" v-if="form.type && form.type !== 'clase'">
            <p class="assigned-professional">
              Será atendido por: {{ assignedProfessionalName }}
            </p>

            <ProfessionalCalendar 
              v-if="assignedProfessionalId"
              :professional-id="assignedProfessionalId"
              @slot-selected="handleSlotSelected"
            />
          </div>

          <div class="form-group">
            <label>Fecha y Hora:</label>
            <input v-model="form.datetime" type="datetime-local" class="form-input" :min="minDateTime">
            <small>Horario disponible: 9:00 - 21:00 en bloques de 1 hora</small>
          </div>

          <button type="submit" class="submit-button">
            Crear Cita
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import ProfessionalCalendar from 'src/components/ProfessionalCalendar.vue'
import GoBackButton from 'src/components/GoBackButton.vue'
import ProfileComponent from 'src/components/ProfileComponent.vue'
import { ref, watch } from 'vue'
import { api } from 'boot/axios'
import { useAuthStore } from 'stores/auth'

const authStore = useAuthStore()
console.log('user', authStore.userDetails)
// Versión reactiva del nombre del profesional
const assignedProfessionalName = ref('')
const assignedProfessionalId = ref(null)

const form = ref({
  type: null,
  class_type: null,
  professional: null,
  datetime: null
})
watch(() => form.value.type, async (newType) => {
  if (newType && newType !== 'clase') {
    assignedProfessionalId.value = newType === 'nutricionista' 
      ? authStore.userDetails.nutricionista 
      : authStore.userDetails.entrenador
    
    if (assignedProfessionalId.value) {
      assignedProfessionalName.value = await getAssignedProfessional(newType)
    }
  }
})

const handleSlotSelected = (formattedDateTime) => {
  form.value.datetime = formattedDateTime
  
  // Forzar actualización del input
  const input = document.querySelector('input[type="datetime-local"]')
  if (input) {
    input.value = formattedDateTime
  }
}

// Función para obtener el nombre del profesional asignado
const getAssignedProfessional = async (type) => {
  try {
    const professionalId = type === 'nutricionista'
      ? authStore.userDetails.nutricionista
      : authStore.userDetails.entrenador

    if (!professionalId) return 'No asignado'

    const response = await api.get(`/api/users/${professionalId}/`)
    return response.data.name
  } catch (error) {
    console.error('Error obteniendo profesional:', error)
    return 'No disponible'
  }
}


const createAppointment = async () => {
  try {
    const payload = {
      ...form.value,
      user: authStore.user.id,
      datetime: new Date(form.value.datetime).toISOString()
    }

    await api.post('/api/appointments/', payload)
    alert('Cita creada exitosamente!')
    window.location.href = '/client-citas'
  } catch (error) {
    alert(error.response?.data?.detail || 'Error creando cita')
  }
}

const minDateTime = ref('')
// Calcular mínimo 24h de antelación
const updateMinDateTime = () => {
  const now = new Date()
  const minDate = new Date(now.getTime() + (24 * 60 * 60 * 1000))
  minDateTime.value = minDate.toISOString().slice(0, 16)
}

// Actualizar al cargar el componente
updateMinDateTime()
setInterval(updateMinDateTime, 60000)  // Actualizar cada minuto
</script>

<style scoped>
.page-container {
  display: flex;
  align-items: center;
  flex-direction: column;
  min-height: 100vh;
  background-color: #F0EEF8;
  /* Nuevo color de fondo */
  padding: 16px;
}

.citas-register {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.profile-container {
  width: 100%;
  display: flex;
  justify-content: space-between;
}

.logo-wrapper {
  /* Margen extra si quieres empujar un poco más arriba */
  margin-top: 16px;
  display: flex;
  justify-content: center;
}

.staff-logo {
  height: 200px;
  max-width: 80%;
}

.assigned-professional {
  color: #2A5C8D;
  font-weight: 500;
  padding: 10px;
  background: #f0f4f8;
  border-radius: 4px;
}

.form-container {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
}

.form-group {
  margin-bottom: 20px;
}

.form-input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-top: 5px;
}

.submit-button {
  background: #28a745;
  color: white;
  padding: 12px 25px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  width: 100%;
}
.calendar-container {
  margin: 20px 0;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
}

.time-slot {
  margin: 5px;
  padding: 10px;
  border: 1px solid #2A5C8D;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.time-slot:hover {
  background-color: #2A5C8D;
  color: white;
}

.selected-slot {
  background-color: #2A5C8D;
  color: white;
}
</style>