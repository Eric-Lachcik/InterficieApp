<template>
<div class="login-container">
    <div class="login-content">
      <!-- Logo y título -->
      <div class="text-center q-mb-xl">
        <img 
          src="FITCOREV2.2.png" 
          class="login-logo q-mb-md"
          alt="FITCORE Logo"
        />
      </div>

      <!-- Formulario -->
      <q-form @submit.prevent="handleLogin" class="q-gutter-y-md">
        <!-- Campo Usuario -->
        <q-input
          v-model="username"
          outlined
          placeholder="Usuario"
          :rules="[val => !!val || 'Campo obligatorio']"
        >
          <template v-slot:prepend>
            <q-icon name="person" />
          </template>
        </q-input>

        <!-- Campo Contraseña -->
        <q-input
          v-model="password"
          outlined
          placeholder="Contraseña"
          type="password"
          :rules="[val => !!val || 'Campo obligatorio']"
        >
          <template v-slot:prepend>
            <q-icon name="lock" />
          </template>
        </q-input>

        <!-- Botón Login -->
        <button 
          type="submit"
          class="login-button"
        >
          Sign In
        </button>

        <!-- Enlace Registro -->
        <div class="text-center q-mt-md">
          <a 
            href="#"
            class="register-link"
            @click.prevent="$router.push('/register')"
          >
            Darse de Alta
          </a>
        </div>
      </q-form>
    </div>
  </div>
</template>
  
<script setup>
import { ref } from 'vue'
import { useQuasar } from 'quasar'
import { useAuthStore } from 'stores/auth'


const $q = useQuasar()
const authStore = useAuthStore()
const username = ref('')
const password = ref('')

const handleLogin = async () => {
  try {
    await authStore.login({
      username: username.value,
      password: password.value
    })
  } catch (error) {
    $q.notify({
      type: 'negative',
      message: error.message || 'Error desconocido',
      position: 'top'
    })
  }
}
</script>
<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #F0EEF8; /* Nuevo color de fondo */
  padding: 16px;
}

.login-content {
  width: 100%;
  max-width: 500px; /* Tarjeta más ancha */
  background: #F0EEF8;
  border-radius: 15px;
  padding: 40px; /* Más padding interno */
  
}

.login-logo {
  height: 200px; /* Logo más grande */
  max-width: 80%; /* Logo más ancho */
}

.login-title {
  font-size: 2rem; /* Texto más grande */
  font-weight: 700;
  color: #2A5C8D;
  margin: 15px 0 8px; /* Más espacio */
}

.login-subtitle {
  color: #757575;
  font-size: 1rem; /* Texto más grande */
  margin: 0 0 30px;
}

.login-button {
  width: 100%;
  padding: 15px;
  background-color: #000000; /* Botón negro */
  color: white;
  border: none;
  border-radius: 25px;
  font-size: 1.1rem; /* Texto más grande */
  cursor: pointer;
  margin-top: 30px;
  transition: background-color 0.3s;
}

.login-button:hover {
  background-color: #333333; /* Hover más claro */
}

.register-link {
  color: #2A5C8D;
  text-decoration: none;
  font-size: 0.9rem;
  font-weight: 500;
}

.register-link:hover {
  text-decoration: underline;
}
</style>