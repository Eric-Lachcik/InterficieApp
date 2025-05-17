<template>
  <q-btn
    flat
    round
    class="q-mb-md back-button"
    @click="goBack"
    aria-label="Volver atrás"
  >
    <q-icon name="arrow_back" />
    <q-tooltip>Volver atrás</q-tooltip>
  </q-btn>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const goBack = () => {
  router.go(-1)
}
</script>

<style scoped>
.back-button {
  /* position: fixed;
  top: 20px;
  left: 20px; */
  z-index: 1000;
  background-color: rgba(255, 255, 255, 0.8);
  border-radius: 50%;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.back-button:hover {
  background-color: rgba(245, 245, 245, 0.9);
  transform: scale(1.1);
}

.back-button:active {
  transform: scale(0.95);
}

/* Para modo oscuro */
.body--dark .back-button {
  background-color: rgba(30, 30, 30, 0.8);
}

.body--dark .back-button:hover {
  background-color: rgba(50, 50, 50, 0.9);
}
</style>