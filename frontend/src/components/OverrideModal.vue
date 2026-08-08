<template>
  <div v-if="isOpen" class="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4 bg-black/80 backdrop-blur-sm animate-fade-in">
    <div class="glass-modal w-full max-w-lg max-h-[90vh] overflow-y-auto rounded-2xl border border-gray-700/60 p-4 sm:p-6 shadow-2xl relative">
      <!-- Header -->
      <div class="flex items-center justify-between border-b border-gray-800 pb-3 sm:pb-4 mb-4 sm:mb-5">
        <div class="flex items-center gap-3">
          <div class="p-2 sm:p-2.5 rounded-xl bg-amber-500/10 text-amber-400 border border-amber-500/20 shrink-0">
            <ShieldAlert class="w-5 h-5 sm:w-6 sm:h-6" />
          </div>
          <div>
            <h3 class="text-base sm:text-lg font-semibold text-white">Manual Status Override</h3>
            <p class="text-[11px] sm:text-xs text-gray-400">Admin Audit Protocol Enforcement</p>
          </div>
        </div>
        <button 
          @click="close" 
          class="p-2 rounded-lg text-gray-400 hover:text-white hover:bg-gray-800 transition-colors"
        >
          <X class="w-5 h-5" />
        </button>
      </div>

      <!-- Employee Info Summary -->
      <div class="bg-gray-900/60 rounded-xl p-3.5 sm:p-4 mb-4 sm:mb-5 border border-gray-800/80">
        <div class="grid grid-cols-2 gap-3 text-xs sm:text-sm">
          <div>
            <span class="text-[10px] sm:text-xs text-gray-500 block">Employee Name</span>
            <span class="font-medium text-gray-200 truncate block">{{ record?.full_name }}</span>
          </div>
          <div>
            <span class="text-[10px] sm:text-xs text-gray-500 block">Employee ID</span>
            <span class="font-mono text-gray-300">{{ record?.employee_id }}</span>
          </div>
          <div>
            <span class="text-[10px] sm:text-xs text-gray-500 block">Current Date</span>
            <span class="text-gray-300">{{ record?.date }}</span>
          </div>
          <div>
            <span class="text-[10px] sm:text-xs text-gray-500 block">Current Status</span>
            <span 
              :class="getStatusBadgeClass(record?.status)"
              class="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] sm:text-xs font-medium border mt-0.5"
            >
              {{ record?.status }}
            </span>
          </div>
        </div>
      </div>

      <!-- Override Form -->
      <form @submit.prevent="handleSubmit" class="space-y-4">
        <!-- New Target Status -->
        <div>
          <label class="block text-xs font-medium text-gray-300 mb-2">Select Target Status <span class="text-rose-400">*</span></label>
          <div class="grid grid-cols-2 gap-2">
            <button
              type="button"
              v-for="s in ['PRESENT', 'EXCUSED', 'LATE', 'ABSENT']"
              :key="s"
              @click="targetStatus = s"
              :class="[
                targetStatus === s 
                  ? 'bg-indigo-600/30 border-indigo-500 text-white font-semibold glow-indigo' 
                  : 'bg-gray-800/40 border-gray-700/60 text-gray-400 hover:bg-gray-800 hover:text-gray-200',
                'px-3 py-2.5 rounded-xl text-xs border transition-all flex items-center justify-center gap-2 min-h-[40px]'
              ]"
            >
              <CheckCircle v-if="targetStatus === s" class="w-4 h-4 text-indigo-400 shrink-0" />
              {{ s }}
            </button>
          </div>
        </div>

        <!-- Mandatory Override Reason -->
        <div>
          <label class="block text-xs font-medium text-gray-300 mb-1">
            Mandatory Override Reason <span class="text-rose-400">*</span>
          </label>
          <textarea
            v-model="overrideReason"
            rows="3"
            placeholder="Explain why this status is being manually altered (e.g. Official Medical Leave certificate approved, Hardware Scanner malfunction)."
            class="w-full bg-gray-950/80 border border-gray-700 focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 rounded-xl p-3 text-xs text-gray-100 placeholder-gray-500 outline-none transition-all"
            required
          ></textarea>
          <p v-if="validationError" class="text-xs text-rose-400 mt-1 flex items-center gap-1">
            <AlertCircle class="w-3.5 h-3.5 shrink-0" />
            {{ validationError }}
          </p>
        </div>

        <!-- Admin ID -->
        <div>
          <label class="block text-xs font-medium text-gray-300 mb-1">Performing Admin User ID</label>
          <input
            v-model="adminId"
            type="text"
            class="w-full bg-gray-950/80 border border-gray-700 focus:border-indigo-500 rounded-xl px-3 py-2 text-xs font-mono text-gray-300 outline-none"
          />
        </div>

        <!-- Audit Notice -->
        <div class="p-3 bg-amber-500/10 border border-amber-500/20 rounded-xl text-[11px] text-amber-300/90 flex items-start gap-2">
          <Info class="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
          <span>
            <strong>Immutable Audit Policy:</strong> This override action will be permanently logged in the <code>audit_logs</code> table with your Admin ID and justification.
          </span>
        </div>

        <!-- Actions -->
        <div class="flex items-center justify-end gap-3 pt-3 border-t border-gray-800">
          <button
            type="button"
            @click="close"
            class="px-4 py-2.5 rounded-xl text-xs font-medium text-gray-400 hover:text-white hover:bg-gray-800 transition-colors"
          >
            Cancel
          </button>
          <button
            type="submit"
            :disabled="isSubmitting"
            class="px-5 py-2.5 rounded-xl text-xs font-semibold bg-indigo-600 hover:bg-indigo-500 text-white shadow-lg shadow-indigo-600/30 transition-all flex items-center gap-2 disabled:opacity-50 min-h-[42px]"
          >
            <Loader2 v-if="isSubmitting" class="w-4 h-4 animate-spin" />
            <span>Confirm & Log Override</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { X, ShieldAlert, CheckCircle, AlertCircle, Info, Loader2 } from 'lucide-vue-next'
import { useAttendanceStore } from '../stores/attendance'

const props = defineProps({
  isOpen: { type: Boolean, default: false },
  record: { type: Object, default: null }
})

const emit = defineEmits(['close', 'updated'])

const attendanceStore = useAttendanceStore()

const targetStatus = ref('EXCUSED')
const overrideReason = ref('')
const adminId = ref('ADMIN-001')
const validationError = ref('')
const isSubmitting = ref(false)

watch(() => props.record, (newRec) => {
  if (newRec) {
    targetStatus.value = newRec.status === 'ABSENT' ? 'EXCUSED' : 'PRESENT'
    overrideReason.value = newRec.override_reason || ''
    validationError.value = ''
  }
})

const getStatusBadgeClass = (st) => {
  switch (st) {
    case 'PRESENT': return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
    case 'LATE': return 'bg-amber-500/10 text-amber-400 border-amber-500/30'
    case 'ABSENT': return 'bg-rose-500/10 text-rose-400 border-rose-500/30'
    case 'EXCUSED': return 'bg-indigo-500/10 text-indigo-400 border-indigo-500/30'
    default: return 'bg-gray-800 text-gray-300 border-gray-700'
  }
}

const close = () => {
  emit('close')
}

const handleSubmit = async () => {
  if (!overrideReason.value || overrideReason.value.trim().length < 3) {
    validationError.value = 'Please enter a detailed override reason (at least 3 characters).'
    return
  }

  validationError.value = ''
  isSubmitting.value = true

  try {
    await attendanceStore.overrideStatus(props.record.id, {
      status: targetStatus.value,
      override_reason: overrideReason.value.trim(),
      admin_id: adminId.value || 'ADMIN-001'
    })

    emit('updated')
    close()
  } catch (err) {
    validationError.value = err.message || 'Failed to apply override.'
  } finally {
    isSubmitting.value = false
  }
}
</script>
