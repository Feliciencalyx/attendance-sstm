<template>
  <div class="glass-panel p-5 rounded-2xl border border-gray-800/80 shadow-xl space-y-4">
    <!-- Header -->
    <div class="flex items-center justify-between border-b border-gray-800 pb-3">
      <div class="flex items-center gap-3">
        <div class="p-2.5 rounded-xl bg-indigo-500/10 text-indigo-400 border border-indigo-500/20 animate-radar">
          <ScanFace class="w-5 h-5" />
        </div>
        <div>
          <h3 class="text-sm font-semibold text-white">Biometric Hardware Simulator</h3>
          <p class="text-xs text-gray-400">Test Facial Vector & Fingerprint Scan Flow</p>
        </div>
      </div>

      <!-- Trigger 9AM Cutoff Button -->
      <button
        @click="handleTriggerCutoff"
        :disabled="attendanceStore.isLoading"
        class="px-3 py-1.5 rounded-xl bg-amber-500/10 hover:bg-amber-500/20 text-amber-300 border border-amber-500/30 text-xs font-semibold flex items-center gap-2 transition-all disabled:opacity-50"
      >
        <Zap class="w-3.5 h-3.5 text-amber-400" />
        <span>Run 9:00 AM Cutoff Job</span>
      </button>
    </div>

    <!-- Simulator Inputs Grid -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <!-- Target User Selection -->
      <div>
        <label class="block text-xs font-medium text-gray-300 mb-1.5">Select Test User</label>
        <select
          v-model="selectedUserId"
          class="w-full bg-gray-900/90 border border-gray-700/80 rounded-xl px-3 py-2 text-xs text-gray-100 outline-none focus:border-indigo-500"
        >
          <option v-for="user in attendanceStore.registeredUsers" :key="user.id" :value="user.id">
            {{ user.full_name }} ({{ user.employee_id }})
          </option>
        </select>
      </div>

      <!-- Biometric Mode -->
      <div>
        <label class="block text-xs font-medium text-gray-300 mb-1.5">Biometric Sensor Type</label>
        <div class="grid grid-cols-2 gap-2">
          <button
            type="button"
            @click="sensorType = 'FACE'"
            :class="[
              sensorType === 'FACE' ? 'bg-indigo-600/30 border-indigo-500 text-white font-semibold' : 'bg-gray-900/60 border-gray-800 text-gray-400',
              'px-2.5 py-1.5 rounded-xl text-xs border flex items-center justify-center gap-1.5 transition-all'
            ]"
          >
            <ScanFace class="w-3.5 h-3.5" />
            Face (128-d)
          </button>
          <button
            type="button"
            @click="sensorType = 'FINGERPRINT'"
            :class="[
              sensorType === 'FINGERPRINT' ? 'bg-indigo-600/30 border-indigo-500 text-white font-semibold' : 'bg-gray-900/60 border-gray-800 text-gray-400',
              'px-2.5 py-1.5 rounded-xl text-xs border flex items-center justify-center gap-1.5 transition-all'
            ]"
          >
            <Fingerprint class="w-3.5 h-3.5" />
            Fingerprint
          </button>
        </div>
      </div>

      <!-- Scan Timing Simulation -->
      <div>
        <label class="block text-xs font-medium text-gray-300 mb-1.5">Simulate Scan Time</label>
        <div class="grid grid-cols-2 gap-2">
          <button
            type="button"
            @click="timePreset = 'BEFORE_9AM'"
            :class="[
              timePreset === 'BEFORE_9AM' ? 'bg-emerald-600/30 border-emerald-500 text-emerald-300 font-semibold' : 'bg-gray-900/60 border-gray-800 text-gray-400',
              'px-2 py-1.5 rounded-xl text-xs border flex items-center justify-center gap-1 transition-all'
            ]"
          >
            <Clock class="w-3.5 h-3.5" />
            08:45 AM (PRESENT)
          </button>
          <button
            type="button"
            @click="timePreset = 'AFTER_9AM'"
            :class="[
              timePreset === 'AFTER_9AM' ? 'bg-amber-600/30 border-amber-500 text-amber-300 font-semibold' : 'bg-gray-900/60 border-gray-800 text-gray-400',
              'px-2 py-1.5 rounded-xl text-xs border flex items-center justify-center gap-1 transition-all'
            ]"
          >
            <Clock class="w-3.5 h-3.5" />
            09:25 AM (LATE)
          </button>
        </div>
      </div>
    </div>

    <!-- Scan Execute Button -->
    <div class="pt-2 flex items-center justify-between">
      <div class="text-[11px] text-gray-400 flex items-center gap-1">
        <Sparkles class="w-3.5 h-3.5 text-indigo-400" />
        <span>Vector threshold algorithm set to <strong>0.80 Cosine Similarity</strong>.</span>
      </div>

      <button
        @click="executeScan"
        :disabled="isScanning"
        class="px-5 py-2.5 rounded-xl bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-semibold text-xs shadow-lg shadow-indigo-600/30 flex items-center gap-2 transition-all disabled:opacity-50"
      >
        <Loader2 v-if="isScanning" class="w-4 h-4 animate-spin" />
        <Scan v-else class="w-4 h-4" />
        <span>Simulate Biometric Scan</span>
      </button>
    </div>

    <!-- Notification Banner -->
    <div v-if="attendanceStore.scanNotification" :class="[
      attendanceStore.scanNotification.type === 'success' ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300' : 'bg-rose-500/10 border-rose-500/30 text-rose-300',
      'p-3.5 rounded-xl border text-xs flex items-start gap-3 transition-all'
    ]">
      <CheckCircle2 v-if="attendanceStore.scanNotification.type === 'success'" class="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />
      <AlertTriangle v-else class="w-5 h-5 text-rose-400 shrink-0 mt-0.5" />
      <div>
        <div class="font-semibold">{{ attendanceStore.scanNotification.message }}</div>
        <div v-if="attendanceStore.scanNotification.data" class="text-[11px] opacity-80 mt-0.5 font-mono">
          User: {{ attendanceStore.scanNotification.data.user_name }} | Status Assigned: {{ attendanceStore.scanNotification.data.status }}
        </div>
      </div>
    </div>

    <!-- Cutoff Notification Banner -->
    <div v-if="attendanceStore.cutoffNotification" class="bg-amber-500/10 border border-amber-500/30 text-amber-300 p-3.5 rounded-xl text-xs flex items-center gap-3">
      <Zap class="w-5 h-5 text-amber-400 shrink-0" />
      <div>
        <div class="font-semibold">{{ attendanceStore.cutoffNotification.message }}</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { 
  ScanFace, 
  Fingerprint, 
  Clock, 
  Zap, 
  Sparkles, 
  Scan, 
  Loader2, 
  CheckCircle2, 
  AlertTriangle 
} from 'lucide-vue-next'
import { useAttendanceStore } from '../stores/attendance'

const attendanceStore = useAttendanceStore()

const selectedUserId = ref('')
const sensorType = ref('FACE')
const timePreset = ref('BEFORE_9AM')
const isScanning = ref(false)

onMounted(async () => {
  await attendanceStore.fetchUsers()
  if (attendanceStore.registeredUsers.length > 0) {
    selectedUserId.value = attendanceStore.registeredUsers[0].id
  }
})

const executeScan = async () => {
  isScanning.value = true
  
  const user = attendanceStore.registeredUsers.find(u => u.id === selectedUserId.value)
  const targetDate = attendanceStore.selectedDate
  const timeStr = timePreset.value === 'BEFORE_9AM' ? '08:45:00' : '09:25:00'
  const scanTime = `${targetDate}T${timeStr}Z`

  let payload = {
    scan_time: scanTime
  }

  if (sensorType.value === 'FACE') {
    // Generate sample 128-d face embedding matched or slightly perturbed
    let baseVal = 0.05
    if (user) {
      if (user.employee_id === 'EMP-101') baseVal = 0.05
      else if (user.employee_id === 'EMP-102') baseVal = 0.1
      else if (user.employee_id === 'EMP-103') baseVal = 0.03
      else if (user.employee_id === 'EMP-104') baseVal = 0.08
      else baseVal = 0.12
    }
    payload.face_embedding = Array.from({ length: 128 }, (_, i) => baseVal * (i % 5))
  } else {
    payload.fingerprint_template = user?.fingerprint_template || `FP_TEMPLATE_${user?.employee_id}`
  }

  try {
    await attendanceStore.sendBiometricScan(payload)
  } catch (err) {
    console.error('Scan error:', err)
  } finally {
    isScanning.value = false
  }
}

const handleTriggerCutoff = async () => {
  await attendanceStore.triggerCutoff()
}
</script>
