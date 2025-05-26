<template>
    <div class="page-container">
        <div class="citas-container">
            <div class="profile-container">
                <GoBackButton />
                <profile-component />
            </div>
            <div class="logo-wrapper">
                <img src="FITCOREV2.2.png" class="staff-logo" alt="FITCORE Logo" />
            </div>
            
        </div>
        <footer-bar ></footer-bar>
    </div>
</template>

<script setup>
import FooterBar from 'src/components/FooterBar.vue'
import GoBackButton from 'src/components/GoBackButton.vue'
import ProfileComponent from 'src/components/ProfileComponent.vue'
// import { ref, onMounted } from 'vue'
// import { api } from 'boot/axios'
// import { useAuthStore } from 'stores/auth'

// const authStore = useAuthStore()



</script>

<style scoped>
.page-container {
    display: flex;
    align-items: center;
    flex-direction: column;
    min-height: 100vh;
    background-color: #F0EEF8;
    /* Nuevo color de fondo */
    padding: 16px;
}

.citas-container {
    padding: 20px;
    max-width: 800px;
    margin: 0 auto;
}

.profile-container {
    width: 100%;
    display: flex;
    justify-content: space-between;
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


</style>