<template>
<div class="staff-dashboard">
  <!-- Contenedor principal -->
    <div class="profile-container">
      <profile-component />
    </div>
    <div class="staff-dashboard-container">
      <!-- Logo + título -->
      <div class="logo-wrapper">
        <img 
          src="FITCOREV2.2.png" 
          class="staff-logo"
          alt="FITCORE Logo"
        />
      </div>

      <div class="buttons">
        <!-- Botones -->
        <q-btn
        label="Buscador Clientes"
        color="primary"
        class="q-my-md"
        @click="$router.push('/ClientSearch')"
        />
        <q-btn
          label="Notificaciones"
          color="primary"
          class="q-my-md"
          @click="$router.push('/StaffNotifications')"
        />
      </div>
    </div>
</div>
</template>


<script setup>
import ProfileComponent from 'src/components/ProfileComponent.vue';

// import { useAuthStore } from 'stores/auth'
// import { useRouter } from 'vue-router'

// const router = useRouter()
// const authStore = useAuthStore()

// Opcional: Cargar usuario desde localStorage al montar el componente
// onMounted(() => {
//   const savedUser = localStorage.getItem('user')
//   if (savedUser) {
//     authStore.user = JSON.parse(savedUser)
//   }
// })
</script>
<style scoped>
.staff-dashboard {
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
  justify-content: flex-end;
}
.staff-dashboard-container {
  display: flex;
  flex-direction: column;
  width: 100%;
  /* max-width: 500px; */
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

.buttons {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
   /* Tarjeta más ancha */
  background: #F0EEF8;
  border-radius: 15px;
  padding-top: 50px;
}

</style>