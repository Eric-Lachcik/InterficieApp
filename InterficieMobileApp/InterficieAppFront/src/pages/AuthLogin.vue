<template>
    <q-page class="flex flex-center bg-grey-2">
      <q-card class="q-pa-md" style="width: 100%; max-width: 400px">
        <q-form @submit.prevent="handleLogin" class="q-gutter-md">
          <q-input
            v-model="username"
            label="Usuario"
            outlined
            :rules="[val => !!val || 'Campo obligatorio']"
          />
  
          <q-input
            v-model="password"
            label="Contraseña"
            type="password"
            outlined
            :rules="[val => !!val || 'Campo obligatorio']"
          />
  
          <q-btn
            label="Entrar"
            type="submit"
            color="primary"
            class="full-width"
          />
        </q-form>
      </q-card>
    </q-page>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { useAuthStore } from 'stores/auth'
  import { useRouter } from 'vue-router'
  
  const authStore = useAuthStore()
  const router = useRouter()
  const username = ref('')
  const password = ref('')
  
  const handleLogin = async () => {
    try {
      await authStore.login({
        username: username.value,
        password: password.value
      })
      router.push(authStore.user.role === 'cliente' ? '/cliente' : '/staff')
    } catch (error) {
      console.error('Error de login:', error)
    }
  }
  </script>