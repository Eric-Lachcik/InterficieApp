
const routes = [
  { 
    path: '/', 
    redirect: '/login'  // Redirige a login si no hay ruta
  },
  { 
    path: '/login', 
    component: () => import('pages/AuthLogin.vue') 
  },
  { 
    path: '/staff-dashboard', 
    component: () => import('pages/StaffDashboard.vue'),
    meta: { requiresStaff: true }
  },
  { 
    path: '/client-dashboard', 
    component: () => import('pages/ClientDashboard.vue'),
    meta: { requiresClient: true }
  },
  { 
    path: '/register', 
    component: () => import('pages/RegisterPage.vue'),
  },
]

export default routes