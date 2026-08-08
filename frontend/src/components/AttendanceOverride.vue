<template>
  <div class="space-y-6">
    <!-- Filters & Action Bar -->
    <div class="glass-panel p-5 rounded-2xl border border-gray-800/80 space-y-4">
      <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <!-- Date Selector & Search -->
        <div class="flex flex-wrap items-center gap-3">
          <!-- Date Input -->
          <div class="flex items-center gap-2 bg-gray-900/80 border border-gray-700/60 rounded-xl px-3 py-2 text-xs text-gray-200">
            <Calendar class="w-4 h-4 text-indigo-400" />
            <input 
              type="date" 
              v-model="attendanceStore.selectedDate"
              @change="handleDateChange"
              class="bg-transparent text-xs text-gray-100 outline-none cursor-pointer"
            />
          </div>

          <!-- Search Input -->
          <div class="relative min-w-[240px]">
            <Search class="w-4 h-4 text-gray-400 absolute left-3 top-2.5" />
            <input
              type="text"
              v-model="attendanceStore.searchQuery"
              placeholder="Search by Name or Employee ID..."
              class="w-full bg-gray-900/80 border border-gray-700/60 focus:border-indigo-500 rounded-xl pl-9 pr-3 py-2 text-xs text-gray-100 placeholder-gray-500 outline-none transition-all"
            />
          </div>
        </div>

        <!-- Filter Status Pills -->
        <div class="flex items-center gap-1.5 overflow-x-auto pb-1 md:pb-0">
          <button
            v-for="st in ['ALL', 'PRESENT', 'LATE', 'ABSENT', 'EXCUSED']"
            :key="st"
            @click="setStatusFilter(st)"
            :class="[
              attendanceStore.selectedStatusFilter === st
                ? 'bg-indigo-600/30 border-indigo-500 text-indigo-300 font-semibold shadow-md shadow-indigo-500/10'
                : 'bg-gray-900/60 border-gray-800 text-gray-400 hover:text-gray-200 hover:bg-gray-800',
              'px-3 py-1.5 rounded-lg text-xs border transition-all whitespace-nowrap'
            ]"
          >
            {{ st }}
          </button>
        </div>
      </div>
    </div>

    <!-- Attendance Table Card -->
    <div class="glass-panel rounded-2xl border border-gray-800/80 overflow-hidden shadow-xl">
      <!-- Table Top Meta -->
      <div class="px-6 py-4 border-b border-gray-800/80 flex items-center justify-between">
        <div>
          <h2 class="text-base font-semibold text-white flex items-center gap-2">
            <UserCheck class="w-5 h-5 text-indigo-400" />
            Daily Attendance Records
          </h2>
          <p class="text-xs text-gray-400 mt-0.5">Showing records for {{ attendanceStore.selectedDate }}</p>
        </div>
        <div class="flex items-center gap-2">
          <span class="text-xs text-gray-400">Total Records:</span>
          <span class="text-xs font-bold text-indigo-400 bg-indigo-500/10 px-2.5 py-1 rounded-md border border-indigo-500/20">
            {{ attendanceStore.filteredAttendance.length }}
          </span>
        </div>
      </div>

      <!-- Data Table -->
      <div class="overflow-x-auto">
        <table class="w-full text-left text-xs text-gray-300">
          <thead class="bg-gray-900/90 border-b border-gray-800 text-gray-400 uppercase text-[10px] tracking-wider">
            <tr>
              <th scope="col" class="px-6 py-3.5">Employee</th>
              <th scope="col" class="px-6 py-3.5">Department</th>
              <th scope="col" class="px-6 py-3.5">Check-In Time</th>
              <th scope="col" class="px-6 py-3.5">Status</th>
              <th scope="col" class="px-6 py-3.5">Audit / Reason</th>
              <th scope="col" class="px-6 py-3.5 text-right">Admin Actions</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-800/60">
            <tr 
              v-for="record in attendanceStore.filteredAttendance" 
              :key="record.id"
              class="hover:bg-gray-800/40 transition-colors"
            >
              <!-- Employee Info -->
              <td class="px-6 py-4">
                <div class="flex items-center gap-3">
                  <div class="w-8 h-8 rounded-full bg-gradient-to-tr from-indigo-600 to-purple-600 flex items-center justify-center font-bold text-white text-xs shadow-md">
                    {{ getInitials(record.full_name) }}
                  </div>
                  <div>
                    <div class="font-semibold text-gray-100">{{ record.full_name }}</div>
                    <div class="text-[11px] font-mono text-gray-400">{{ record.employee_id }}</div>
                  </div>
                </div>
              </td>

              <!-- Department -->
              <td class="px-6 py-4">
                <span class="bg-gray-800/60 border border-gray-700/50 px-2.5 py-1 rounded-md text-[11px] text-gray-300">
                  {{ record.department || 'General' }}
                </span>
              </td>

              <!-- Check-In Time -->
              <td class="px-6 py-4 font-mono">
                <div v-if="record.check_in_time" class="flex items-center gap-1.5 text-gray-200">
                  <Clock class="w-3.5 h-3.5 text-gray-400" />
                  <span>{{ formatTime(record.check_in_time) }}</span>
                </div>
                <div v-else class="text-gray-500 italic">-- : --</div>
              </td>

              <!-- Status Badge -->
              <td class="px-6 py-4">
                <span
                  :class="getStatusBadgeClass(record.status)"
                  class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-[11px] font-medium border"
                >
                  <span class="w-1.5 h-1.5 rounded-full" :class="getStatusDotClass(record.status)"></span>
                  {{ record.status }}
                </span>
              </td>

              <!-- Audit Reason / Override Indicator -->
              <td class="px-6 py-4 max-w-xs">
                <div v-if="record.override_reason" class="text-xs space-y-0.5">
                  <div class="text-gray-300 line-clamp-1" :title="record.override_reason">
                    "{{ record.override_reason }}"
                  </div>
                  <div class="text-[10px] text-amber-400/90 flex items-center gap-1">
                    <ShieldCheck class="w-3 h-3" />
                    <span>Modified by {{ record.modified_by || 'Admin' }}</span>
                  </div>
                </div>
                <div v-else class="text-gray-500 text-[11px] italic">Standard Entry</div>
              </td>

              <!-- Actions -->
              <td class="px-6 py-4 text-right">
                <button
                  @click="openOverrideModal(record)"
                  class="px-3 py-1.5 rounded-lg bg-indigo-600/20 hover:bg-indigo-600/40 text-indigo-300 border border-indigo-500/30 hover:border-indigo-400 transition-all font-medium text-xs flex items-center gap-1.5 ml-auto"
                >
                  <Edit3 class="w-3.5 h-3.5" />
                  <span>Override Status</span>
                </button>
              </td>
            </tr>

            <!-- Empty State -->
            <tr v-if="attendanceStore.filteredAttendance.length === 0">
              <td colspan="6" class="px-6 py-12 text-center text-gray-500">
                <FileX class="w-10 h-10 mx-auto text-gray-600 mb-2" />
                <p class="text-sm font-medium">No attendance records match the selected filters.</p>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Override Modal -->
    <OverrideModal
      :isOpen="isModalOpen"
      :record="selectedRecord"
      @close="isModalOpen = false"
      @updated="handleRecordUpdated"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useHead } from '@unhead/vue'
import { 
  Calendar, 
  Search, 
  UserCheck, 
  Clock, 
  ShieldCheck, 
  Edit3, 
  FileX 
} from 'lucide-vue-next'
import { useAttendanceStore } from '../stores/attendance'
import OverrideModal from './OverrideModal.vue'

// Dynamic SEO Head Management via @unhead/vue as specified in requirements
useHead({
  title: 'Attendance Management & Manual Override Portal',
  meta: [
    { name: 'description', content: 'Enterprise Biometric Attendance Management system with daily 9:00 AM automated cutoff and audit-logged manual status overrides.' },
    { property: 'og:title', content: 'Biometric Attendance Admin System' },
    { property: 'og:description', content: 'Manage daily attendance, view 9:00 AM cutoff reports, and audit manual overrides.' }
  ]
})

const attendanceStore = useAttendanceStore()
const isModalOpen = ref(false)
const selectedRecord = ref(null)

onMounted(() => {
  attendanceStore.fetchAttendance()
})

const handleDateChange = () => {
  attendanceStore.fetchAttendance()
}

const setStatusFilter = (st) => {
  attendanceStore.selectedStatusFilter = st
  attendanceStore.fetchAttendance()
}

const openOverrideModal = (record) => {
  selectedRecord.value = record
  isModalOpen.value = true
}

const handleRecordUpdated = () => {
  attendanceStore.fetchAttendance()
}

const getInitials = (name) => {
  if (!name) return 'U'
  return name.split(' ').map(n => n[0]).join('').toUpperCase().slice(0, 2)
}

const formatTime = (isoString) => {
  if (!isoString) return ''
  const d = new Date(isoString)
  return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })
}

const getStatusBadgeClass = (st) => {
  switch (st) {
    case 'PRESENT': return 'bg-emerald-500/10 text-emerald-400 border-emerald-500/30'
    case 'LATE': return 'bg-amber-500/10 text-amber-400 border-amber-500/30'
    case 'ABSENT': return 'bg-rose-500/10 text-rose-400 border-rose-500/30'
    case 'EXCUSED': return 'bg-indigo-500/10 text-indigo-400 border-indigo-500/30'
    default: return 'bg-gray-800 text-gray-300 border-gray-700'
  }
}

const getStatusDotClass = (st) => {
  switch (st) {
    case 'PRESENT': return 'bg-emerald-400'
    case 'LATE': return 'bg-amber-400'
    case 'ABSENT': return 'bg-rose-400'
    case 'EXCUSED': return 'bg-indigo-400'
    default: return 'bg-gray-400'
  }
}
</script>
