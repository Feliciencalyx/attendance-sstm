<template>
  <div class="min-h-screen pb-12">
    <!-- Top Header -->
    <header class="border-b border-gray-800/80 bg-gray-950/80 sticky top-0 z-40 backdrop-blur-xl">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
        <!-- Logo & Title -->
        <div class="flex items-center gap-3">
          <div class="p-2.5 rounded-xl bg-gradient-to-tr from-indigo-600 to-purple-600 text-white shadow-lg shadow-indigo-600/30">
            <ShieldCheck class="w-6 h-6" />
          </div>
          <div>
            <h1 class="text-lg font-bold tracking-tight text-white flex items-center gap-2">
              BioCheck<span class="text-indigo-400">Pro</span>
              <span class="text-[10px] bg-indigo-500/10 text-indigo-300 border border-indigo-500/20 px-2 py-0.5 rounded-full font-mono uppercase">
                ADMIN PORTAL
              </span>
            </h1>
            <p class="text-xs text-gray-400">Enterprise Biometric Attendance Management System</p>
          </div>
        </div>

        <!-- Right Controls & Navigation -->
        <div class="flex items-center gap-3 text-xs">
          <!-- Auth Badge -->
          <div v-if="isAuthenticated" class="hidden sm:flex items-center gap-2 bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 px-3 py-1.5 rounded-xl font-mono text-[11px]">
            <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
            <span>Admin: {{ adminUsername }}</span>
          </div>

          <button
            v-if="isAuthenticated"
            @click="logout"
            class="px-3.5 py-2 rounded-xl bg-gray-900 hover:bg-gray-800 text-gray-400 hover:text-white border border-gray-700 text-xs transition-colors flex items-center gap-1.5"
          >
            <LogOut class="w-3.5 h-3.5" />
            <span>Logout</span>
          </button>

          <!-- Enroll User Button -->
          <button
            v-if="isAuthenticated"
            @click="isEnrollModalOpen = true"
            class="px-3.5 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-semibold flex items-center gap-2 transition-all shadow-md shadow-emerald-600/20"
          >
            <UserPlus class="w-4 h-4" />
            <span>Enroll Employee</span>
          </button>

          <!-- User Terminal Link -->
          <router-link
            to="/kiosk"
            class="px-3.5 py-2 rounded-xl bg-gray-900 hover:bg-gray-800 border border-gray-700 text-gray-200 hover:text-white font-semibold flex items-center gap-2 transition-all"
          >
            <ScanFace class="w-4 h-4 text-indigo-400" />
            <span>User Kiosk UI</span>
          </router-link>
        </div>
      </div>
    </header>

    <!-- Admin Authentication Login Portal (Default view when opening /admin) -->
    <div v-if="!isAuthenticated" class="max-w-md mx-auto mt-16 px-4">
      <div class="glass-panel p-8 rounded-3xl border border-gray-800/80 shadow-2xl space-y-6">
        <div class="text-center space-y-2">
          <div class="w-16 h-16 rounded-2xl bg-gradient-to-tr from-indigo-600 to-purple-600 text-white mx-auto flex items-center justify-center shadow-lg shadow-indigo-600/30">
            <Lock class="w-8 h-8" />
          </div>
          <h2 class="text-2xl font-extrabold text-white">Admin Portal Login</h2>
          <p class="text-xs text-gray-400">Restricted Access. Enter system administrator credentials to proceed.</p>
        </div>

        <form @submit.prevent="handleLogin" class="space-y-4">
          <div>
            <label class="block text-xs font-medium text-gray-300 mb-1">Admin Username <span class="text-rose-400">*</span></label>
            <input
              v-model="inputUsername"
              type="text"
              required
              placeholder="e.g. felicien"
              class="w-full bg-gray-950/80 border border-gray-700 focus:border-indigo-500 rounded-xl px-3.5 py-2.5 text-xs text-gray-100 outline-none transition-all"
            />
          </div>

          <div>
            <label class="block text-xs font-medium text-gray-300 mb-1">Password <span class="text-rose-400">*</span></label>
            <input
              v-model="inputPassword"
              type="password"
              required
              placeholder="••••••••••••"
              class="w-full bg-gray-950/80 border border-gray-700 focus:border-indigo-500 rounded-xl px-3.5 py-2.5 text-xs text-gray-100 outline-none transition-all"
            />
          </div>

          <div v-if="loginError" class="p-3 bg-rose-500/10 border border-rose-500/30 rounded-xl text-xs text-rose-300 flex items-center gap-2">
            <AlertTriangle class="w-4 h-4 shrink-0 text-rose-400" />
            <span>{{ loginError }}</span>
          </div>

          <!-- Credential Helper Note -->
          <div class="p-3.5 bg-indigo-500/10 border border-indigo-500/20 rounded-xl text-[11px] text-indigo-300">
            <strong>System Admin Credentials:</strong><br />
            Username: <code>felicien</code><br />
            Password: <code>Logout@800</code>
          </div>

          <button
            type="submit"
            class="w-full py-3 rounded-xl bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 hover:from-indigo-500 hover:to-pink-500 text-white font-bold text-xs shadow-xl shadow-indigo-600/30 flex items-center justify-center gap-2 transition-all"
          >
            <LogIn class="w-4 h-4" />
            <span>Sign In to Admin Portal</span>
          </button>
        </form>
      </div>
    </div>

    <!-- Main Admin Portal Content (Visible ONLY after successful authentication) -->
    <main v-else class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-8 space-y-8 animate-fade-in">
      <!-- Overview Metrics Grid -->
      <section class="grid grid-cols-2 md:grid-cols-5 gap-4">
        <!-- Total -->
        <div class="glass-panel p-4 rounded-2xl border border-gray-800/80">
          <div class="flex items-center justify-between text-gray-400 mb-2">
            <span class="text-xs font-medium">Total Staff</span>
            <Users class="w-4 h-4 text-gray-400" />
          </div>
          <div class="text-2xl font-bold text-white">{{ attendanceStore.stats.total }}</div>
          <div class="text-[10px] text-gray-500 mt-1">Registered users</div>
        </div>

        <!-- Present -->
        <div class="glass-panel p-4 rounded-2xl border border-emerald-500/20 glow-emerald">
          <div class="flex items-center justify-between text-emerald-400 mb-2">
            <span class="text-xs font-medium">Present</span>
            <CheckCircle2 class="w-4 h-4 text-emerald-400" />
          </div>
          <div class="text-2xl font-bold text-emerald-300">{{ attendanceStore.stats.present }}</div>
          <div class="text-[10px] text-emerald-400/70 mt-1">Scanned before 9:00 AM</div>
        </div>

        <!-- Late -->
        <div class="glass-panel p-4 rounded-2xl border border-amber-500/20 glow-amber">
          <div class="flex items-center justify-between text-amber-400 mb-2">
            <span class="text-xs font-medium">Late</span>
            <Clock class="w-4 h-4 text-amber-400" />
          </div>
          <div class="text-2xl font-bold text-amber-300">{{ attendanceStore.stats.late }}</div>
          <div class="text-[10px] text-amber-400/70 mt-1">Scanned after 9:00 AM</div>
        </div>

        <!-- Absent -->
        <div class="glass-panel p-4 rounded-2xl border border-rose-500/20 glow-rose">
          <div class="flex items-center justify-between text-rose-400 mb-2">
            <span class="text-xs font-medium">Absent</span>
            <XCircle class="w-4 h-4 text-rose-400" />
          </div>
          <div class="text-2xl font-bold text-rose-300">{{ attendanceStore.stats.absent }}</div>
          <div class="text-[10px] text-rose-400/70 mt-1">9:00 AM Cutoff Auto-Insert</div>
        </div>

        <!-- Excused -->
        <div class="glass-panel p-4 rounded-2xl border border-indigo-500/20 glow-indigo">
          <div class="flex items-center justify-between text-indigo-400 mb-2">
            <span class="text-xs font-medium">Excused</span>
            <ShieldCheck class="w-4 h-4 text-indigo-400" />
          </div>
          <div class="text-2xl font-bold text-indigo-300">{{ attendanceStore.stats.excused }}</div>
          <div class="text-[10px] text-indigo-400/70 mt-1">Admin Audit Overrides</div>
        </div>
      </section>

      <!-- Biometric Hardware Simulator Section -->
      <section>
        <BiometricScannerSimulator />
      </section>

      <!-- Main Attendance Management Table Section -->
      <section>
        <AttendanceOverride />
      </section>
    </main>

    <!-- Enroll Employee Modal -->
    <UserEnrollmentModal
      :isOpen="isEnrollModalOpen"
      @close="isEnrollModalOpen = false"
      @enrolled="handleUserEnrolled"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { 
  ShieldCheck, 
  Clock, 
  Users, 
  CheckCircle2, 
  XCircle, 
  UserPlus, 
  ScanFace, 
  Lock, 
  LogIn, 
  LogOut, 
  AlertTriangle 
} from 'lucide-vue-next'
import { useAttendanceStore } from '../stores/attendance'
import AttendanceOverride from '../components/AttendanceOverride.vue'
import BiometricScannerSimulator from '../components/BiometricScannerSimulator.vue'
import UserEnrollmentModal from '../components/UserEnrollmentModal.vue'

const attendanceStore = useAttendanceStore()
const isEnrollModalOpen = ref(false)
const isAuthenticated = ref(false) // Requires explicit login by default
const adminUsername = ref('')

const inputUsername = ref('')
const inputPassword = ref('')
const loginError = ref('')

const handleLogin = () => {
  const u = inputUsername.value.trim().toLowerCase()
  const p = inputPassword.value

  if (
    (u === 'felicien' || u === 'felicien@biocheckpro.com' || u === 'admin') &&
    (p === 'Logout@800' || p === 'Logout@800!' || p === 'AdminPass123!')
  ) {
    isAuthenticated.value = true
    adminUsername.value = inputUsername.value
    loginError.value = ''
    attendanceStore.fetchAttendance()
  } else {
    loginError.value = 'Invalid admin credentials. Username: felicien | Password: Logout@800'
  }
}

const logout = () => {
  isAuthenticated.value = false
  inputUsername.value = ''
  inputPassword.value = ''
}

const handleUserEnrolled = () => {
  attendanceStore.fetchUsers()
}
</script>
