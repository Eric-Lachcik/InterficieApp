import AuthLogin from 'pages/AuthLogin.vue'
import ClienteDashboard from 'pages/ClienteDashboard.vue'
import StaffDashboard from 'pages/StaffDashboard.vue'

const routes = [
  { path: '/login', component: AuthLogin },
  { path: '/cliente', component: ClienteDashboard },
  { path: '/staff', component: StaffDashboard },
  { path: '/', redirect: '/login' }
]

export default routes