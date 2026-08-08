import { createRouter, createWebHistory } from 'vue-router'
import LandingView from '../views/LandingView.vue'
import UserKioskView from '../views/UserKioskView.vue'
import AdminDashboard from '../views/AdminDashboard.vue'

const routes = [
  {
    path: '/',
    name: 'Landing',
    component: LandingView,
    meta: {
      title: 'BioCheckPro - Biometric Attendance System',
      description: 'Enterprise Biometric Attendance Management System with 128-d face recognition, WebAuthn fingerprinting, and 9:00 AM cutoff rules.'
    }
  },
  {
    path: '/kiosk',
    name: 'UserKiosk',
    component: UserKioskView,
    meta: {
      title: 'Employee Kiosk Terminal | BioCheckPro',
      description: 'Employee biometric check-in kiosk terminal supporting WebCam face recognition and WebAuthn fingerprint readers.'
    }
  },
  {
    path: '/admin',
    name: 'AdminDashboard',
    component: AdminDashboard,
    meta: {
      title: 'Admin Dashboard | BioCheckPro',
      description: 'Real-time biometric attendance monitoring, automated 9:00 AM cutoff rules, and admin manual override portal.'
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
