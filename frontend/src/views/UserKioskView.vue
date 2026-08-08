<template>
  <div class="min-h-screen bg-[#0b0f17] text-gray-100 flex flex-col justify-between">
    <!-- Top Kiosk Header -->
    <header class="border-b border-gray-800/80 bg-gray-950/90 backdrop-blur-xl sticky top-0 z-40 px-6 py-4">
      <div class="max-w-7xl mx-auto flex items-center justify-between">
        <!-- Logo -->
        <div class="flex items-center gap-3">
          <div class="p-3 rounded-2xl bg-gradient-to-tr from-indigo-600 to-purple-600 text-white shadow-xl shadow-indigo-600/30">
            <ScanFace class="w-7 h-7" />
          </div>
          <div>
            <h1 class="text-xl font-extrabold text-white tracking-tight flex items-center gap-2">
              BioCheck<span class="text-indigo-400">Terminal</span>
              <span class="text-[10px] bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-2.5 py-0.5 rounded-full font-mono">
                LIVE HARDWARE KIOSK
              </span>
            </h1>
            <p class="text-xs text-gray-400">Biometric Attendance Verification Terminal</p>
          </div>
        </div>

        <!-- Clock & Admin Link -->
        <div class="flex items-center gap-4">
          <div class="hidden sm:flex flex-col items-end">
            <span class="text-xs text-gray-400 font-medium">{{ currentDateString }}</span>
            <span class="text-lg font-mono font-bold text-indigo-300">{{ currentTimeString }}</span>
          </div>

          <router-link
            to="/admin"
            class="px-4 py-2.5 rounded-xl bg-gray-900 hover:bg-gray-800 border border-gray-700 text-gray-200 hover:text-white text-xs font-semibold flex items-center gap-2 transition-all shadow-md"
          >
            <ShieldCheck class="w-4 h-4 text-indigo-400" />
            <span>Admin Portal</span>
          </router-link>
        </div>
      </div>
    </header>

    <!-- Main Kiosk Body -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 w-full space-y-8 flex-1">
      <!-- Cutoff Banner Info -->
      <div class="p-4 rounded-2xl bg-gradient-to-r from-indigo-900/40 via-purple-900/30 to-gray-900 border border-indigo-500/30 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <Clock class="w-6 h-6 text-indigo-400 shrink-0" />
          <div>
            <div class="text-xs font-bold text-indigo-200">Daily Attendance Threshold Rules</div>
            <div class="text-[11px] text-gray-300 mt-0.5">
              Check-ins completed <strong>at or before 09:00 AM</strong> are recorded as <span class="text-emerald-400 font-semibold">PRESENT</span>. Check-ins after 09:00 AM are flagged as <span class="text-amber-400 font-semibold">LATE</span>.
            </div>
          </div>
        </div>
      </div>

      <!-- Scanner Options Grid (Live WebCam vs WebAuthn Fingerprint) -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <!-- WebCam Live Face Scanner -->
        <LiveCameraScanner />

        <!-- WebAuthn Hardware Fingerprint Scanner -->
        <WebAuthnFingerprintScanner />
      </div>

      <!-- Live Scan Notification Result -->
      <div v-if="attendanceStore.scanNotification" :class="[
        attendanceStore.scanNotification.type === 'success' ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300' : 'bg-rose-500/10 border-rose-500/30 text-rose-300',
        'p-5 rounded-2xl border text-sm flex items-start gap-4 transition-all shadow-xl animate-fade-in'
      ]">
        <CheckCircle2 v-if="attendanceStore.scanNotification.type === 'success'" class="w-6 h-6 text-emerald-400 shrink-0 mt-0.5" />
        <AlertTriangle v-else class="w-6 h-6 text-rose-400 shrink-0 mt-0.5" />
        <div class="space-y-1">
          <div class="font-bold text-base">{{ attendanceStore.scanNotification.message }}</div>
          <div v-if="attendanceStore.scanNotification.data" class="text-xs font-mono text-gray-300">
            Employee: <strong>{{ attendanceStore.scanNotification.data.user_name }}</strong> ({{ attendanceStore.scanNotification.data.employee_id }}) | 
            Status: <span class="font-bold text-indigo-400">{{ attendanceStore.scanNotification.data.status }}</span> | 
            Checked-in: {{ formatTime(attendanceStore.scanNotification.data.check_in_time) }}
          </div>
        </div>
      </div>
    </main>

    <!-- Footer -->
    <footer class="border-t border-gray-900 py-4 text-center text-xs text-gray-500">
      Biometric Attendance Management System &copy; 2026. Connected to Supabase pgvector backend.
    </footer>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { ScanFace, ShieldCheck, Clock, CheckCircle2, AlertTriangle } from 'lucide-vue-next'
import { useAttendanceStore } from '../stores/attendance'
import LiveCameraScanner from '../components/LiveCameraScanner.vue'
import WebAuthnFingerprintScanner from '../components/WebAuthnFingerprintScanner.vue'

const attendanceStore = useAttendanceStore()

const currentTimeString = ref('')
const currentDateString = ref('')
let timer = null

const updateClock = () => {
  const now = new Date()
  currentTimeString.value = now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })
  currentDateString.value = now.toLocaleDateString([], { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })
}

const formatTime = (isoStr) => {
  if (!isoStr) return ''
  return new Date(isoStr).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })
}

onMounted(() => {
  updateClock()
  timer = setInterval(updateClock, 1000)
  attendanceStore.fetchUsers()
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})
</script>
