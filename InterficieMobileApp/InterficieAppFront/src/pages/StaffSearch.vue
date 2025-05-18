<template>
  <div class="client-search">
    <div class="client-search-container">
        <div class="profile-container">
            <go-back-button />
            <profile-component />
        </div>
        <div class="logo-wrapper">
            <img 
            src="FITCOREV2.2.png" 
            class="staff-logo"
            alt="FITCORE Logo"
            />
        </div>
        <div class="search-box">
            <input 
                v-model="searchQuery"
                type="text"
                placeholder="Buscar cliente..."
                class="search-input"/>
            <span class="search-icon">🔍</span>
        </div>

        <div class="client-list">
        <div 
            v-for="client in filteredClients" 
            :key="client.id"
            class="client-item">
            <div class="client-info">
                <div class="client-name">{{ client.name }} {{ client.surname }}</div>
                <div class="client-email">{{ client.email }}</div>
            </div>
            <q-btn 
              class="view-button"
              label="Ver informes"
              @click="navigateToReports(client.id)"
            />
        </div>
        <div v-if="filteredClients.length === 0" class="client-item">
            <div class="client-info">
                <div class="client-name">No se encontraron clientes</div>
            </div>
        </div>
        </div>
    </div>
  </div>
</template>

<script setup>
import GoBackButton from 'src/components/GoBackButton.vue'
import ProfileComponent from 'src/components/ProfileComponent.vue'
import { ref, onMounted, computed } from 'vue'
import { api } from 'boot/axios'
import { useAuthStore } from 'stores/auth'
import { useRouter } from 'vue-router'
const router = useRouter()


const authStore = useAuthStore()
const clients = ref([])
const searchQuery = ref('')
const user = authStore.user
const userDetails = authStore.userDetails
const userId = user.id
const userRole = userDetails.role

onMounted(async () => {
  try {
    const response = await api.get('/api/my-clients/', {
      headers: {
        'X-User-ID': userId,
        'X-User-Role': userRole
      }
    })
    clients.value = response.data
    console.log('Clientes cargados:', clients.value)
  } catch (error) {
    console.error('Error cargando clientes:', error)
  }
})

const navigateToReports = (clientId) => {
  router.push(`/client-reports/${clientId}`)
}

const filteredClients = computed(() => {
  return clients.value.filter(client => 
    `${client.name} ${client.surname}`.toLowerCase().includes(searchQuery.value.toLowerCase()))
})
</script>

<style scoped>
.client-search{
  display: flex;
  align-items: center;
  flex-direction: column;
  min-height: 100vh;
  background-color: #F0EEF8; /* Nuevo color de fondo */
  padding: 16px;
}

.profile-container{
  width: 100%;
  display: flex;
  justify-content: space-between;
}
.client-search-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
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

.search-box {
  position: relative;
  margin-bottom: 20px;
}

.search-input {
  width: 100%;
  padding: 12px 40px 12px 15px;
  border: 2px solid #ddd;
  border-radius: 8px;
  font-size: 16px;
  transition: border-color 0.3s ease;
}

.search-input:focus {
  outline: none;
  border-color: #2A5C8D;
}

.search-icon {
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%);
  color: #666;
}

.client-list {
  border: 1px solid #eee;
  border-radius: 8px;
  overflow: hidden;
}
.view-button {
  margin-left: auto;
  background-color: #2A5C8D;
  color: white;
  padding: 8px 16px;
  border-radius: 4px;
}

.client-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 15px;
  border-bottom: 1px solid #eee;
  transition: background-color 0.2s ease;
  cursor: pointer;
}

.client-item:last-child {
  border-bottom: none;
}

.client-item:hover {
  background-color: #f8f9fa;
}

.client-name {
  font-weight: 500;
  color: #333;
  margin-bottom: 4px;
}

.client-email {
  color: #666;
  font-size: 0.9em;
}

@media (max-width: 600px) {
  .client-search-container {
    padding: 15px;
  }
  
  .search-input {
    padding: 10px 35px 10px 12px;
    font-size: 14px;
  }
  
  .client-item {
    padding: 12px;
  }
}
</style>