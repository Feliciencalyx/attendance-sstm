<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/75 backdrop-blur-sm">
    <div class="glass-modal w-full max-w-lg rounded-2xl border border-gray-700/60 p-6 shadow-2xl relative">
      <!-- Header -->
      <div class="flex items-center justify-between border-b border-gray-800 pb-4 mb-5">
        <div class="flex items-center gap-3">
          <div class="p-2.5 rounded-xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
            <UserPlus class="w-6 h-6" />
          </div>
          <div>
            <h3 class="text-lg font-semibold text-white">Enroll New Employee</h3>
            <p class="text-xs text-gray-400">Register profile & capture biometric embeddings</p>
          </div>
        </div>
        <button @click="close" class="p-2 rounded-lg text-gray-400 hover:text-white hover:bg-gray-800 transition-colors">
          <X class="w-5 h-5" />
        </button>
      </div>

      <!-- Form -->
      <form @submit.prevent="handleSubmit" class="space-y-4">
        <div>
          <label class="block text-xs font-medium text-gray-300 mb-1">Employee Full Name <span class="text-rose-400">*</span></label>
          <input
            v-model="fullName"
            type="text"
            placeholder="e.g. Michael Scott"
            required
            class="w-full bg-gray-950/80 border border-gray-700 focus:border-indigo-500 rounded-xl px-3 py-2 text-xs text-gray-100 outline-none"
          />
        </div>

        <div class="grid grid-cols-2 gap-3">
          <div>
            <label class="block text-xs font-medium text-gray-300 mb-1">Employee ID <span class="text-rose-400">*</span></label>
            <input
              v-model="employeeId"
              type="text"
              placeholder="EMP-106"
              required
              class="w-full bg-gray-950/80 border border-gray-700 focus:border-indigo-500 rounded-xl px-3 py-2 text-xs font-mono text-gray-100 outline-none"
            />
          </div>
          <div>
            <label class="block text-xs font-medium text-gray-300 mb-1">Department</label>
            <select
              v-model="department"
              class="w-full bg-gray-950/80 border border-gray-700 focus:border-indigo-500 rounded-xl px-3 py-2 text-xs text-gray-100 outline-none"
            >
              <option value="Engineering">Engineering</option>
              <option value="Operations">Operations</option>
              <option value="Human Resources">Human Resources</option>
              <option value="Finance">Finance</option>
              <option value="Security">Security</option>
            </select>
          </div>
        </div>

        <div>
          <label class="block text-xs font-medium text-gray-300 mb-1">Email Address <span class="text-rose-400">*</span></label>
          <input
            v-model="email"
            type="email"
            placeholder="michael.scott@example.com"
            required
            class="w-full bg-gray-950/80 border border-gray-700 focus:border-indigo-500 rounded-xl px-3 py-2 text-xs text-gray-100 outline-none"
          />
        </div>

        <!-- Biometric Enrollment Type -->
        <div>
          <label class="block text-xs font-medium text-gray-300 mb-1">Biometric Feature Template</label>
          <div class="p-3 bg-indigo-500/10 border border-indigo-500/20 rounded-xl text-xs text-indigo-300 flex items-center gap-2">
            <Sparkles class="w-4 h-4 text-indigo-400 shrink-0" />
            <span>Automated 128-d face embedding vector & fingerprint hash generated during registration.</span>
          </div>
        </div>

        <!-- Actions -->
        <div class="flex items-center justify-end gap-3 pt-3 border-t border-gray-800">
          <button type="button" @click="close" class="px-4 py-2 text-xs text-gray-400 hover:text-white">Cancel</button>
          <button
            type="submit"
            :disabled="isSubmitting"
            class="px-5 py-2.5 rounded-xl text-xs font-semibold bg-emerald-600 hover:bg-emerald-500 text-white shadow-lg shadow-emerald-600/30 flex items-center gap-2"
          >
            <Loader2 v-if="isSubmitting" class="w-4 h-4 animate-spin" />
            <span>Register & Enroll User</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { UserPlus, X, Sparkles, Loader2 } from 'lucide-vue-next'
import { useAttendanceStore } from '../stores/attendance'

const props = defineProps({
  isOpen: { type: Boolean, default: false }
})

const emit = defineEmits(['close', 'enrolled'])

const attendanceStore = useAttendanceStore()

const fullName = ref('')
const employeeId = ref(`EMP-${106 + Math.floor(Math.random() * 50)}`)
const department = ref('Engineering')
const email = ref('')
const isSubmitting = ref(false)

const close = () => {
  emit('close')
}

const handleSubmit = async () => {
  isSubmitting.value = true
  try {
    const newUser = {
      id: `user-${Date.now()}`,
      employee_id: employeeId.value,
      full_name: fullName.value,
      email: email.value || `${employeeId.value.toLowerCase()}@example.com`,
      department: department.value,
      fingerprint_template: `FP_TEMPLATE_${employeeId.value}`,
      face_embedding: Array.from({ length: 128 }, (_, i) => 0.07 * (i % 6)),
      is_active: true
    }

    attendanceStore.registeredUsers.push(newUser)
    emit('enrolled', newUser)
    close()
  } finally {
    isSubmitting.value = false
  }
}
</script>
