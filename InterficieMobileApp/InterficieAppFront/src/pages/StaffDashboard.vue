<template>
<h1>Staff Dashboard</h1>
  <div v-if="authStore.user">
    <h2>Bienvenido {{ authStore.user.name }} {{ authStore.user.surname }}</h2>
    
  </div>
</template>


<script setup>
import { useAuthStore } from 'stores/auth'
// import { onMounted } from 'vue'

const authStore = useAuthStore()

// Opcional: Cargar usuario desde localStorage al montar el componente
// onMounted(() => {
//   const savedUser = localStorage.getItem('user')
//   if (savedUser) {
//     authStore.user = JSON.parse(savedUser)
//   }
// })
</script>