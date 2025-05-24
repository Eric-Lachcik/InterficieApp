<template>
  <div class="page-container">
    <div class="notifications-container">
      <div class="profile-container">
        <GoBackButton />
        <profile-component />
      </div>
      <div class="logo-wrapper">
        <img src="FITCOREV2.2.png" class="staff-logo" alt="FITCORE Logo" />
      </div>

      <div class="notification-header">
        <h4>Notificaciones</h4>
        <button @click="markAllAsRead" class="mark-read-btn">
          Marcar todas como leídas
        </button>
      </div>

      <div v-if="notifications.length === 0" class="empty-state">
        <span class="icon">📁</span>
        <p>No hay informes disponibles</p>
      </div>

      <div class="notification-list">
        <div v-for="notification in notifications" :key="notification.id" class="notification-item"
          :class="{ unread: !notification.read }">
          <div class="notification-content">
            {{ notification.message }}
            <small>{{ formatDate(notification.created_at) }}</small>
          </div>
          <button v-if="!notification.read" @click="markAsRead(notification.id)" class="read-btn">
            ✓
          </button>
        </div>
      </div>
    </div>
    <footer-bar v-if="!authStore.user.isStaff"></footer-bar>
  </div>
</template>

<script setup>
import FooterBar from 'src/components/FooterBar.vue'
import GoBackButton from 'src/components/GoBackButton.vue'
import ProfileComponent from 'src/components/ProfileComponent.vue'
import { ref, onMounted } from 'vue'
import { api } from 'boot/axios'
import { useAuthStore } from 'stores/auth'

const notifications = ref([])
const authStore = useAuthStore()
onMounted(async () => {
  await fetchNotifications()
  // setInterval(fetchNotifications, 60000) // Actualizar cada 30 segundos
})

// Ejemplo de llamada para obtener notificaciones
const fetchNotifications = async () => {
  try {
    const response = await api.get('/api/notifications/', {
      headers: {
        'X-User-ID': authStore.user.id // Enviar ID desde el store
      }
    })
    notifications.value = response.data
    console.log('Notificaciones obtenidas:', notifications.value)
  } catch (error) {
    console.error('Error obteniendo notificaciones:', error)
  }
}

// Ejemplo de marcar como leída
const markAsRead = async (notificationId) => {
  await api.patch(`/api/notifications/${notificationId}/mark-read/`, null, {
    headers: {
      'X-User-ID': authStore.user.id
    }
  })
  await fetchNotifications()
}

const markAllAsRead = async () => {
  await api.post(
    '/api/notifications/mark-all-read/',
    null, // Body vacío
    {
      headers: {
        'X-User-ID': authStore.user.id // <- Añadir header
      }
    }
  )
  await fetchNotifications()
}

const formatDate = (dateString) => {
  const date = new Date(dateString);
  
  return date.toLocaleString('es-ES', {
    day: 'numeric',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit',
    timeZoneName: 'shortOffset'
  });
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

.notifications-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.notification-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.notification-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px;
  margin-bottom: 10px;
  background: #f8f9fa;
  border-radius: 8px;
}

.unread {
  background: #e3f2fd;
  border-left: 4px solid #2A5C8D;
}

.read-btn {
  background: none;
  border: none;
  color: #2A5C8D;
  cursor: pointer;
  font-size: 1.2em;
}

.mark-read-btn {
  background: #2A5C8D;
  color: white;
  padding: 8px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
</style>