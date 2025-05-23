<template>
    <div class="page-container">
        <div class="citas-container">
            <div class="profile-container">
                <GoBackButton />
                <profile-component />
            </div>
            <div class="logo-wrapper">
                <img src="FITCOREV2.2.png" class="staff-logo" alt="FITCORE Logo" />
            </div>
            <div class="header">
                <h3>Mis Citas</h3>
                <button class="create-button" @click="$router.push('/client-register-cita')">
                    Nueva Cita
                </button>
            </div>
            <div v-if="appointments.length === 0" class="empty-state">
                <span class="icon">📁</span>
                <p>No hay citas disponibles</p>
            </div>

            <div class="appointments-list">
                <div v-for="appointment in appointments" :key="appointment.id" class="appointment-card">
                    <div class="appointment-info">
                        <h4>{{ formatType(appointment.type, appointment.class_type) }}</h4>
                        <p class="datetime">{{ formatDateTime(appointment.datetime) }}</p>
                    </div>
                    <button class="delete-button" @click="confirmDelete(appointment)">
                        Eliminar
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import GoBackButton from 'src/components/GoBackButton.vue'
import ProfileComponent from 'src/components/ProfileComponent.vue'
import { ref, onMounted } from 'vue'
import { api } from 'boot/axios'
import { useAuthStore } from 'stores/auth'

const authStore = useAuthStore()
const appointments = ref([])

onMounted(async () => {
    try {
        const response = await api.get(`/api/appointments/?user=${authStore.user.id}`)
        appointments.value = response.data
        console.log('appointments', appointments.value)
    } catch {
        alert('Error cargando citas')
    }
})

const formatType = (type, classType) => {
    const types = {
        nutricionista: 'Nutricionista',
        entrenador: 'Entrenador Personal',
        clase: `Clase de ${classType}`
    }
    return types[type]
}

const formatDateTime = (datetime) => {
    return new Date(datetime).toLocaleString('es-ES', {
        weekday: 'short',
        day: 'numeric',
        month: 'short',
        hour: '2-digit',
        minute: '2-digit'
    })
}

const confirmDelete = async (appointment) => {
    const confirmar = window.confirm('¿Estás seguro de eliminar esta cita?')

    if (confirmar) {
        try {
            await api.delete(`/api/appointments/${appointment.id}/`)
            appointments.value = appointments.value.filter(a => a.id !== appointment.id)
            alert('✓ Cita eliminada correctamente')
        } catch {
            alert('✗ Error eliminando la cita')
        }
    }
}
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

.citas-container {
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

.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
}

.create-button {
    background: #2A5C8D;
    color: white;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
}

.appointments-list {
    display: grid;
    gap: 15px;
}

.appointment-card {
    background: white;
    border: 1px solid #ddd;
    border-radius: 8px;
    padding: 15px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.appointment-info h4 {
    margin: 0 0 5px 0;
    color: #2A5C8D;
}

.datetime {
    color: #666;
    margin: 0;
}

.delete-button {
    background: #dc3545;
    color: white;
    padding: 8px 15px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}
</style>