<template>

<h1>Cliente dashBoard</h1>
<h1>Cliente Dashboard</h1>
  <div v-if="authStore.userDetails">
    <h2>Bienvenido {{ authStore.userDetails.name }} {{ authStore.userDetails.surname }}</h2>
    <p>Email: {{ authStore.userDetails.email }}</p>
    <p>Peso: {{ authStore.userDetails.weight }} kg</p>
    <p>Altura: {{ authStore.userDetails.stature }} m</p>
    <p>Masa muscular: {{ authStore.userDetails.muscle_mass }}%</p>
    <p>Localidad: {{ authStore.userDetails.population }}</p>
</div>
<button @click="authStore.logout">Logout</button>
</template>

<script setup>
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