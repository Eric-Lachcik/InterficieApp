import { defineRouter } from '#q-app/wrappers'
import { createRouter, createMemoryHistory, createWebHistory, createWebHashHistory } from 'vue-router'
import routes from './routes'
import { useAuthStore } from 'stores/auth'

export default defineRouter(function (/* { store, ssrContext } */) {
  const createHistory = process.env.SERVER
    ? createMemoryHistory
    : (process.env.VUE_ROUTER_MODE === 'history' ? createWebHistory : createWebHashHistory)

  const Router = createRouter({
    scrollBehavior: () => ({ left: 0, top: 0 }),
    routes,
    history: createHistory(process.env.VUE_ROUTER_BASE)
  })

  // Añadir el guardia de navegación aquí
  Router.beforeEach((to, from, next) => {
    const authStore = useAuthStore();
    
    if (to.path === '/login' && authStore.user) {
      // Redirigir según tipo de usuario
      authStore.user.isStaff 
        ? next('/staff-dashboard')
        : next('/client-dashboard');
    } else {
      next();
    }
  });

  return Router
})