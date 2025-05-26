<template>
  <div class="bottom-nav">
    <div class="nav-container">
      <!-- Botón Web -->
      <router-link 
        to="/client-dashboard" 
        class="nav-item"
        active-class="active"
      >
        <div class="nav-label">Inicio</div>
      </router-link>

      <!-- Botón Nutricaders -->
      <router-link 
        to="/notifications" 
        class="nav-item"
        active-class="active"
      >
        <div class="nav-label">Notificaciones</div>
      </router-link>

      <!-- Botón Informes -->
      <router-link 
        to="/client-charts" 
        class="nav-item"
        active-class="active"
      >
        <div class="nav-label">Informe</div>
      </router-link>

    </div>
  </div>
</template>

<script setup>

</script>

<style lang="scss" scoped>
.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: #e9deee;
  border: 2px solid #c34ad3;
  box-shadow: 0 -2px 8px rgba(42, 92, 141, 0.1);
  z-index: 1000;
  border-radius: 15px;
}

.nav-container {
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding: 8px 0;
  height: 64px;
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 8px 12px;
  cursor: pointer;
  text-decoration: none;
  color: #c34ad3;
  transition: all 0.3s ease;
}

.nav-item:hover {
  transform: translateY(-2px);
}

.nav-item.active {
  color: #1a3a5a;
  font-weight: 500;
}

.nav-icon {
  font-size: 24px;
  margin-bottom: 4px;
}

.nav-label {
  font-size: 12px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

</style>