<template>
  <div padding class="profile-page">
    <!-- Encabezado -->
    <div class="header">
        <GoBackButton />
        <h2 class="text-h4">Tu Perfil</h2>
        <q-btn 
            label="Ver Informes" 
            color="primary"
            @click="$router.push('/client-reports-page')"
        />
    </div>

    <!-- Formulario de Edición -->
    <q-form @submit="updateProfile" class="profile-form">
      <div class="form-section">
        <q-input
          v-model="formData.name"
          label="Nombre"
          outlined
          class="q-mb-md"
          :rules="[val => !!val || 'Campo obligatorio']"
        />

        <q-input
          v-model="formData.surname"
          label="Apellidos"
          outlined
          class="q-mb-md"
          :rules="[val => !!val || 'Campo obligatorio']"
        />

        <div class="row q-col-gutter-md">
          <div class="col-6">
            <q-input
              v-model="formData.weight"
              label="Peso (kg)"
              type="number"
              outlined
              suffix="kg"
              :rules="[val => val > 0 || 'Peso inválido']"
            />
          </div>
          
          <div class="col-6">
            <q-input
              v-model="formData.muscle_mass"
              label="Masa Muscular (%)"
              type="number"
              step="0.01"
              outlined
              suffix="%"
              :rules="[val => val > 0 || 'Masa Muscular inválida']"
            />
          </div>
        </div>
      </div>

      <q-btn 
        type="submit" 
        label="Actualizar Datos" 
        color="primary" 
        class="submit-button"
        :loading="loading"
      />
    </q-form>
  </div>
</template>

<script setup>
import GoBackButton from 'src/components/GoBackButton.vue'
import { ref, onMounted } from 'vue'
import { useAuthStore } from 'stores/auth'
import { api } from 'boot/axios'
import { useQuasar } from 'quasar'
const $q = useQuasar()
const authStore = useAuthStore()
const loading = ref(false)

// Datos del formulario
const formData = ref({
  name: '',
  surname: '',
  weight: null,
  muscle_mass: null
})

// Cargar datos iniciales
onMounted(() => {
  formData.value = {
    name: authStore.userDetails.name,
    surname: authStore.userDetails.surname,
    weight: authStore.userDetails.weight,
    muscle_mass: authStore.userDetails.muscle_mass
  }
})

// Actualizar perfil
const updateProfile = async () => {
  try {
    loading.value = true
    const response = await api.patch(`/api/users/${authStore.user.id}/`, formData.value)
    
    // Actualizar store local
    authStore.userDetails = {
      ...authStore.userDetails,
      ...response.data
    }
    
    // Mostrar notificación
    $q.notify({
      type: 'positive',
      message: 'Datos actualizados correctamente'
    })
  } catch (error) {
    console.error('Error actualizando perfil:', error)
    $q.notify({
      type: 'negative',
      message: 'Error al actualizar los datos'
    })
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.profile-page {
  display: flex;
  align-items: center;
  flex-direction: column;
  min-height: 100vh;
  background-color: #F0EEF8; /* Nuevo color de fondo */
  padding: 16px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.form-section {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.submit-button {
  margin-top: 20px;
  width: 100%;
}
</style>