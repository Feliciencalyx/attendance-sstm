import { createRouter, createWebHistory } from 'vue-router'
import UserKioskView from '../views/UserKioskView.vue'
import AdminDashboard from '../views/AdminDashboard.vue'

const routes = [
  {
    path: '/',
    name: 'UserKiosk',
    component: UserKioskView,
    meta: {
      title: 'Biometric Attendance Kiosk Terminal',
      description: 'Employee biometric check-in kiosk terminal supporting WebCam face recognition and WebAuthn fingerprint readers.'
    }
  },
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: AdminDashboard,
    meta: {
      title: 'Admin Dashboard | Biometric Attendance Management',
      description: 'Real-time biometric attendance monitoring, automated 9:00 AM cutoff rules, and admin manual override portal.'
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
