<template>
<div class="client-dashboard">
    <div class="client-dashboard-container">
      <div class="profile-container">
        <profile-component />
      </div>
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
          label="Citas"
          color="primary"
          class="q-my-md"
          @click="$router.push('/client-citas')"
        />
      </div>
    </div>
    <footer-bar />
</div>
</template>

<script setup>
import FooterBar from 'src/components/FooterBar.vue';
import ProfileComponent from 'src/components/ProfileComponent.vue';
import { useAuthStore } from 'stores/auth'
import { onMounted } from 'vue'
const authStore = useAuthStore()


onMounted(async () => {
  // Si ya tenemos user pero no los detalles
  console.log('user', authStore.user)
  if (authStore.user && !authStore.userDetails) {
    await authStore.fetchUserDetails(authStore.user.id)
    console.log('userDetails', authStore.userDetails)
  }
})
</script>
<style scoped>
.client-dashboard {
  display: flex;
  align-items: center;
  flex-direction: column;
  min-height: 100vh;
  background-color: #F0EEF8; /* Nuevo color de fondo */
  padding: 16px;
}

.client-dashboard-container {
  padding: 20px;
  max-width: 800px;
  margin: 0 auto;
}

.profile-container{
  width: 100%;
  display: flex;
  justify-content: flex-end;
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