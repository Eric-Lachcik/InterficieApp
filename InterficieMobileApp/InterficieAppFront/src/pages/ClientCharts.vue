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
            <div>
                <div class="q-pa-md">
                    <!-- Gráfico de Peso -->
                    <div class="q-mb-xl">
                        <h6 class="q-my-md">Evolución de Peso (kg)</h6>
                        <div v-if="weightData.labels.length" class="chart-container">
                            <LineChart :data="weightData" :options="chartOptions"/>
                        </div>
                        <div v-else class="text-grey-7">
                            No hay datos de peso disponibles
                        </div>
                    </div>

                    <!-- Gráfico de Masa Muscular -->
                    <div class="q-mb-xl">
                        <h6 class="q-my-md">Evolución de Masa Muscular (%)</h6>
                        <div v-if="muscleData.labels.length" class="chart-container">
                            <LineChart :data="muscleData" :options="chartOptions"/>
                        </div>
                        <div v-else class="text-grey-7">
                            No hay datos de masa muscular disponibles
                        </div>
                    </div>
                    <!-- Mensajes de estado -->
                    <div v-if="loading" class="text-center">
                        <q-spinner color="primary" size="3em"/>
                        <p>Cargando datos...</p>
                    </div>
                    <div v-if="error" class="text-negative">{{ error }}</div>
                </div>
            </div>
        </div>
        <footer-bar ></footer-bar>
    </div>
</template>

<script setup>
import LineChart from 'src/components/LineChart.vue'
import FooterBar from 'src/components/FooterBar.vue'
import GoBackButton from 'src/components/GoBackButton.vue'
import ProfileComponent from 'src/components/ProfileComponent.vue'
import { ref, onMounted, computed} from 'vue'
import { api } from 'boot/axios'
import { useAuthStore } from 'stores/auth'

const authStore = useAuthStore()

/// Estado del componente
const evolutionData = ref([])
const loading = ref(false)
const error = ref(null)

// Configuración común de gráficos
const chartOptions = ref({
  responsive: true,
  maintainAspectRatio: false,
  scales: {
    y: { beginAtZero: true }
  }
})

// Procesar datos para peso
const weightData = computed(() => ({
  labels: evolutionData.value.map(d => new Date(d.date).toLocaleDateString('es-ES')),
  datasets: [{
    label: 'Peso (kg)',
    data: evolutionData.value.map(d => d.weight),
    borderColor: '#2A5C8D',
    backgroundColor: 'rgba(42, 92, 141, 0.2)',
    tension: 0.4
  }]
}))

// Procesar datos para masa muscular
const muscleData = computed(() => ({
  labels: evolutionData.value.map(d => new Date(d.date).toLocaleDateString('es-ES')),
  datasets: [{
    label: 'Masa Muscular (%)',
    data: evolutionData.value.map(d => d.muscle_mass),
    borderColor: '#8D2A5C',
    backgroundColor: 'rgba(141, 42, 92, 0.2)',
    tension: 0.4
  }]
}))

// Obtener datos
const fetchData = async () => {
  try {
    loading.value = true
    const response = await api.get(`/api/evolution/${authStore.user.id}/`)
    console.log('Datos de evolución:', response.data)
    evolutionData.value = response.data.sort((a, b) => new Date(a.date) - new Date(b.date))
  } catch (err) {
    error.value = 'Error cargando datos: ' + err.message
  } finally {
    loading.value = false
  }
}

onMounted(fetchData)
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

.chart-container {
  height: 400px;
  position: relative;
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


</style>