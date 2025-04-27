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
    const authStore = useAuthStore()
    const publicPages = ['/login']
    const authRequired = !publicPages.includes(to.path)

    // Si la ruta requiere autenticación y no hay usuario logueado
    if (authRequired && !authStore.user) {
      authStore.returnUrl = to.fullPath
      next('/login')
    } else {
      // Si está logueado y trata de acceder al login, redirigir a dashboard
      if (to.path === '/login' && authStore.user) {
        next(authStore.user.role === 'cliente' ? '/cliente' : '/staff')
      } else {
        next()
      }
    }
  })

  return Router
})