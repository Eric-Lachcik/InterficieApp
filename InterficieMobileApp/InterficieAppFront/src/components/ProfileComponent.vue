<template>
  <div class="user-menu-wrapper">
    <!-- Botón del menú -->
    <q-btn flat round @click.stop="toggleMenu" class="menu-trigger">
      <q-avatar :class="userIconColor" size="40px">
        <q-icon name="person" />
      </q-avatar>
    </q-btn>
    <!-- Menú desplegable con control manual -->
    <div v-show="menuOpen" class="custom-menu" v-click-outside="closeMenu">
      <q-list class="menu-content">
        <q-item v-if="!authStore.user.isStaff" clickable @click="goToProfile">
          <q-item-section avatar>
            <q-icon name="account_circle" />
          </q-item-section>
          <q-item-section>Mi Perfil</q-item-section>
        </q-item>

        <q-separator />

        <q-item clickable @click="logout">
          <q-item-section avatar>
            <q-icon name="logout" color="negative" />
          </q-item-section>
          <q-item-section class="text-negative">Cerrar Sesión</q-item-section>
        </q-item>
      </q-list>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from 'stores/auth'


const router = useRouter()
const authStore = useAuthStore()
const menuOpen = ref(false)

const toggleMenu = (event) => {
  event.stopPropagation()
  menuOpen.value = !menuOpen.value
  console.log('Menu state:', menuOpen.value)
}

const closeMenu = () => {
  if (menuOpen.value) {
    menuOpen.value = false
    console.log('Closing menu')
  }
}

// Color del icono según el tipo de usuario
const userIconColor = computed(() => {
  return authStore.user.isStaff ? 'bg-indigo-4 text-white' : 'bg-blue-4 text-white'
})

const goToProfile = () => {
  router.push('/client-profile')
}

const logout = () => {
  authStore.logout()
}

// Configuración directiva para detectar clics externos
const vClickOutside = {
  beforeMount(el, binding) {
    el.clickOutsideEvent = function (event) {
      if (!(el === event.target || el.contains(event.target))) {
        binding.value(event)
      }
    }
    document.body.addEventListener('click', el.clickOutsideEvent)
  },
  unmounted(el) {
    document.body.removeEventListener('click', el.clickOutsideEvent)
  }
}

</script>
<style scoped>
.user-menu-container {
  position: relative;
  z-index: 9999;
}

.custom-menu {
  position: absolute;
  right: 0;
  top: 50px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  z-index: 10000;
  min-width: 200px;
}

.menu-trigger {
  transition: transform 0.2s ease;
}

.menu-trigger:hover {
  transform: scale(1.1);
}

.q-item {
  padding: 12px 16px;
  cursor: pointer;
}

.q-item:hover {
  background-color: #f5f5f5;
}
</style>