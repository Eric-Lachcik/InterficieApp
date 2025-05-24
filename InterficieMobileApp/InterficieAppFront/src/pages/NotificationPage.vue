<template>
  <div class="notifications-container">
    <div class="notification-header">
      <h2>Notificaciones</h2>
      <button @click="markAllAsRead" class="mark-read-btn">
        Marcar todas como leídas
      </button>
    </div>
    
    <div class="notification-list">
      <div 
        v-for="notification in notifications"
        :key="notification.id"
        class="notification-item"
        :class="{ unread: !notification.read }"
      >
        <div class="notification-content">
          {{ notification.message }}
          <small>{{ formatDate(notification.created_at) }}</small>
        </div>
        <button 
          v-if="!notification.read"
          @click="markAsRead(notification.id)"
          class="read-btn"
        >
          ✓
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from 'boot/axios'

const notifications = ref([])

onMounted(async () => {
  await fetchNotifications()
  setInterval(fetchNotifications, 30000) // Actualizar cada 30 segundos
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
}

const markAllAsRead = async () => {
  await api.post('/api/notifications/mark_all_read/')
  await fetchNotifications()
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleString('es-ES', {
    day: 'numeric',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit'
  })
}
</script>

<style scoped>
.notifications-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
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