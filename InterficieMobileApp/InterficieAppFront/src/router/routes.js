
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
  { 
    path: '/ClientSearch', 
    component: () => import('src/pages/StaffSearch.vue'),
  },
  { 
    path: '/client-reports/:clientId',
    name: 'ClientReports',
    component: () => import('pages/StaffReview.vue'),
  },
  { 
    path: '/client-reports-page',
    name: 'ClientReportsPage',
    component: () => import('pages/ClientReportPage.vue'),
  },
  { 
    path: '/client-profile',
    name: 'ClientProfile',
    component: () => import('pages/ClientProfile.vue'),
  },
  { 
    path: '/client-citas',
    name: 'ClientCitas',
    component: () => import('pages/ClientCitas.vue'),
  },
  { 
    path: '/client-register-cita',
    name: 'ClientRegisterCita',
    component: () => import('pages/ClientRegisterCita.vue'),
  },
  { 
    path: '/notifications',
    name: 'NotificationsPage',
    component: () => import('pages/NotificationPage.vue'),
  }
]

export default routes