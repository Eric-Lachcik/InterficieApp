<template>
    <div class="page-container">
        <div class="q-pa-md">
            <div class="profile-container">
                <go-back-button />
                <profile-component />
            </div>
            <!-- Cabecera con datos de la store -->
            <div class="row items-center q-mb-md">
                <div class="logo-wrapper">
                    <img 
                    src="FITCOREV2.2.png" 
                    class="staff-logo"
                    alt="FITCORE Logo"
                    />
                </div>
                <h4 class="q-ma-none q-ml-md">
                Informes de {{ clientData.name }} {{ clientData.surname }}
                </h4>
            </div>

            <!-- Subida de archivos -->
            <q-card>
                <q-card-section>
                <q-file
                    v-model="newReport"
                    label="Subir nuevo informe"
                    accept=".pdf,.csv,.xlsx"
                    @update:model-value="uploadFile"
                />
                </q-card-section>
            </q-card>

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
                </q-item-section>
                </q-item>
            </q-list>
        </div>
    </div>
</template>

<script setup>
import GoBackButton from 'src/components/GoBackButton.vue'
import ProfileComponent from 'src/components/ProfileComponent.vue'
import { ref, onMounted } from 'vue'
import { useRoute} from 'vue-router'
import { api } from 'boot/axios'
import { useAuthStore } from 'stores/auth'

const route = useRoute()
const authStore = useAuthStore()

const clientData = ref({})
const reports = ref([])
const newReport = ref(null)

// Cargar datos iniciales
onMounted(async () => {
  try {
    const [clientRes, reportsRes] = await Promise.all([
      api.get(`/api/users/${route.params.clientId}/`),
      api.get(`/api/client-reports/?client=${route.params.clientId}`)
    ])
    
    clientData.value = clientRes.data
    reports.value = reportsRes.data
  } catch (error) {
    console.error('Error cargando datos:', error)
  }
})

// Subir archivo usando FormData
const uploadFile = async () => {
  if (!newReport.value) return
  console.log('Subiendo archivo:', authStore.user.id)
  const formData = new FormData()
  formData.append('file', newReport.value)
  formData.append('client', route.params.clientId)
  formData.append('uploaded_by', authStore.user.id)

  try {
    const response = await api.post('/api/client-reports/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    reports.value.push(response.data)
    newReport.value = null
  } catch (error) {
    console.error('Error subiendo archivo:', error)
  }
}

// Funciones auxiliares
const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('es-ES')
}

const downloadReport = (report) => {
  window.open(report.file, '_blank')
}
</script>
<style scoped>
.page-container{
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

.staff-logo {
  height: 200px;
  max-width: 80%;
}

.logo-wrapper {
  /* Margen extra si quieres empujar un poco más arriba */
  margin-top: 16px;
  display: flex;
  justify-content: center;
}
</style>