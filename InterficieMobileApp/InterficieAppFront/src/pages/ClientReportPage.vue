<template>
  <div class="reports-container">
    <div class="reports-header">
      <GoBackButton />
      <h2>Informes Cargados</h2>
    </div>

    <div v-if="reports.length === 0" class="empty-state">
      <span class="icon">📁</span>
      <p>No hay informes disponibles</p>
    </div>

   <!-- Lista de informes -->
    <q-list bordered class="q-mt-md">
        <q-item v-for="report in reports" :key="report.id">
        <q-item-section>
            <q-item-label>{{ report.file_name }}</q-item-label>
            <q-item-label caption>
            Subido el: {{ formatDate(report.upload_date) }}
            </q-item-label>
        </q-item-section>
        
        <q-item-section side>
            <q-btn 
            icon="download"
            @click="downloadReport(report)"
            color="primary"
            flat
            />
            <q-btn 
            icon="delete"
            @click="confirmDelete(report)"
            color="negative"
            flat
            />
        </q-item-section>
        </q-item>
    </q-list>
  </div>
</template>

<script setup>
import GoBackButton from 'src/components/GoBackButton.vue'
import { ref, onMounted } from 'vue'
import { api } from 'boot/axios'
import { useAuthStore } from 'stores/auth'

const authStore = useAuthStore()
const reports = ref([])


const confirmDelete = async (report) => {
  const confirmar = window.confirm('¿Estás seguro de eliminar este informe?')
  
  if (confirmar) {
    try {
      await api.delete(`/api/client-reports/${report.id}/`)
      reports.value = reports.value.filter(r => r.id !== report.id)
      alert('Informe eliminado correctamente') // O usa tu sistema de notificaciones
    } catch {
      alert('Error al eliminar el informe')
    }
  }
}
// Cargar informes
onMounted(async () => {
  try {
    const response = await api.get('/api/client-reports/', {
      params: {
        client: authStore.user.id
      }
    })
    reports.value = response.data
    console.log('Informes cargados:', reports.value)
  } catch (error) {
    console.error('Error cargando informes:', error)
  }
})

// Formatear fecha
const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('es-ES')
}

// Descargar informe
const downloadReport = (report) => {
  window.open(report.file, '_blank')
}
</script>

<style scoped>
.reports-container {
  display: flex;
  align-items: center;
  flex-direction: column;
  min-height: 100vh;
  background-color: #F0EEF8; /* Nuevo color de fondo */
  padding: 16px;
}

.reports-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 30px;
}


.empty-state {
  text-align: center;
  padding: 40px;
  color: #666;
}

.empty-state .icon {
  font-size: 48px;
  display: block;
  margin-bottom: 10px;
}

.reports-list {
  
}

.report-card {
  background: white;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  transition: transform 0.2s;
}

.report-card:hover {
  transform: translateY(-2px);
}

.report-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.report-info h3 {
  margin: 0 0 5px 0;
  color: #2A5C8D;
}

.report-info p {
  margin: 0;
  color: #666;
  font-size: 0.9em;
}

.download-button {
  background: #2A5C8D;
  color: white;
  border: none;
  padding: 8px 15px;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.3s;
}

.download-button:hover {
  background: #1a3a5a;
}
</style>