import { defineStore } from 'pinia'
import axios from 'axios'

const API_BASE = '/api/v1'

export const useAttendanceStore = defineStore('attendance', {
  state: () => ({
    attendanceList: [],
    registeredUsers: [],
    selectedDate: new Date().toISOString().split('T')[0],
    selectedStatusFilter: 'ALL',
    searchQuery: '',
    isLoading: false,
    error: null,
    scanNotification: null,
    cutoffNotification: null
  }),

  getters: {
    filteredAttendance(state) {
      return state.attendanceList.filter(item => {
        const matchesStatus = state.selectedStatusFilter === 'ALL' || item.status === state.selectedStatusFilter
        const s = state.searchQuery.toLowerCase()
        const matchesSearch = !s || item.full_name.toLowerCase().includes(s) || item.employee_id.toLowerCase().includes(s)
        return matchesStatus && matchesSearch
      })
    },

    stats(state) {
      const list = state.attendanceList
      return {
        total: list.length,
        present: list.filter(i => i.status === 'PRESENT').length,
        late: list.filter(i => i.status === 'LATE').length,
        absent: list.filter(i => i.status === 'ABSENT').length,
        excused: list.filter(i => i.status === 'EXCUSED').length
      }
    }
  },

  actions: {
    async fetchAttendance() {
      this.isLoading = true
      this.error = null
      try {
        const params = {
          date: this.selectedDate,
          status: this.selectedStatusFilter !== 'ALL' ? this.selectedStatusFilter : undefined,
          search: this.searchQuery || undefined
        }
        const response = await axios.get(`${API_BASE}/attendance`, { params })
        this.attendanceList = response.data
      } catch (err) {
        console.warn('Backend API connection failed, loading fallback local dataset.', err.message)
        // Standalone fallback mock dataset if backend service is offline
        this.attendanceList = [
          {
            id: 'b0000000-0000-0000-0000-000000000001',
            user_id: 'a0000000-0000-0000-0000-000000000001',
            employee_id: 'EMP-101',
            full_name: 'Sarah Connor',
            email: 'sarah.connor@example.com',
            department: 'Engineering',
            date: this.selectedDate,
            check_in_time: `${this.selectedDate}T08:45:00Z`,
            status: 'PRESENT',
            override_reason: null,
            modified_by: null,
            updated_at: `${this.selectedDate}T08:45:00Z`
          },
          {
            id: 'b0000000-0000-0000-0000-000000000002',
            user_id: 'a0000000-0000-0000-0000-000000000002',
            employee_id: 'EMP-102',
            full_name: 'Alex Mercer',
            email: 'alex.mercer@example.com',
            department: 'Operations',
            date: this.selectedDate,
            check_in_time: `${this.selectedDate}T09:22:15Z`,
            status: 'LATE',
            override_reason: null,
            modified_by: null,
            updated_at: `${this.selectedDate}T09:22:15Z`
          },
          {
            id: 'b0000000-0000-0000-0000-000000000003',
            user_id: 'a0000000-0000-0000-0000-000000000003',
            employee_id: 'EMP-103',
            full_name: 'Elena Rostova',
            email: 'elena.rostova@example.com',
            department: 'Human Resources',
            date: this.selectedDate,
            check_in_time: null,
            status: 'ABSENT',
            override_reason: 'Automated 9:00 AM System Cutoff',
            modified_by: 'SYSTEM_SCHEDULER',
            updated_at: `${this.selectedDate}T09:00:00Z`
          }
        ]
      } finally {
        this.isLoading = false
      }
    },

    async fetchUsers() {
      try {
        const response = await axios.get(`${API_BASE}/users`)
        this.registeredUsers = response.data
      } catch (err) {
        this.registeredUsers = [
          { id: 'a0000000-0000-0000-0000-000000000001', employee_id: 'EMP-101', full_name: 'Sarah Connor', fingerprint_template: 'FP_TEMPLATE_SARAH_CONNOR_9981' },
          { id: 'a0000000-0000-0000-0000-000000000002', employee_id: 'EMP-102', full_name: 'Alex Mercer', fingerprint_template: 'FP_TEMPLATE_ALEX_MERCER_1204' },
          { id: 'a0000000-0000-0000-0000-000000000003', employee_id: 'EMP-103', full_name: 'Elena Rostova', fingerprint_template: 'FP_TEMPLATE_ELENA_ROSTOVA_5512' },
          { id: 'a0000000-0000-0000-0000-000000000004', employee_id: 'EMP-104', full_name: 'David Vance', fingerprint_template: 'FP_TEMPLATE_DAVID_VANCE_7743' },
          { id: 'a0000000-0000-0000-0000-000000000005', employee_id: 'EMP-105', full_name: 'Marcus Wright', fingerprint_template: 'FP_TEMPLATE_MARCUS_WRIGHT_8831' }
        ]
      }
    },

    async sendBiometricScan(payload) {
      this.isLoading = true
      this.scanNotification = null
      try {
        const response = await axios.post(`${API_BASE}/biometric/scan`, payload)
        this.scanNotification = {
          type: 'success',
          message: response.data.message,
          data: response.data
        }
        await this.fetchAttendance()
        return response.data
      } catch (err) {
        const msg = err.response?.data?.detail || err.message
        this.scanNotification = {
          type: 'error',
          message: msg
        }
        throw new Error(msg)
      } finally {
        this.isLoading = false
      }
    },

    async overrideStatus(attendanceId, overridePayload) {
      this.isLoading = true
      try {
        const response = await axios.post(`${API_BASE}/attendance/${attendanceId}/override`, overridePayload)
        
        // Update local state record instantly
        const idx = this.attendanceList.findIndex(item => item.id === attendanceId)
        if (idx !== -1) {
          this.attendanceList[idx] = response.data
        } else {
          await this.fetchAttendance()
        }
        return response.data
      } catch (err) {
        // Local fallback update if backend offline
        const idx = this.attendanceList.findIndex(item => item.id === attendanceId)
        if (idx !== -1) {
          this.attendanceList[idx].status = overridePayload.status
          this.attendanceList[idx].override_reason = overridePayload.override_reason
          this.attendanceList[idx].modified_by = overridePayload.admin_id
          this.attendanceList[idx].updated_at = new Date().toISOString()
        }
        return this.attendanceList[idx]
      } finally {
        this.isLoading = false
      }
    },

    async triggerCutoff() {
      this.isLoading = true
      try {
        const response = await axios.post(`${API_BASE}/scheduler/trigger-cutoff`, null, {
          params: { target_date: this.selectedDate }
        })
        this.cutoffNotification = response.data
        await this.fetchAttendance()
        return response.data
      } catch (err) {
        console.warn('Cutoff API error, triggering fallback simulation', err)
        // Fallback simulation: find registered users without attendance record for selectedDate
        const currentCheckins = new Set(this.attendanceList.map(a => a.user_id))
        const missing = this.registeredUsers.filter(u => !currentCheckins.has(u.id))
        
        missing.forEach(u => {
          this.attendanceList.push({
            id: `cutoff-${u.id}-${Date.now()}`,
            user_id: u.id,
            employee_id: u.employee_id,
            full_name: u.full_name,
            email: u.email || `${u.employee_id.toLowerCase()}@example.com`,
            department: u.department || 'General',
            date: this.selectedDate,
            check_in_time: null,
            status: 'ABSENT',
            override_reason: 'Automated 9:00 AM System Cutoff',
            modified_by: 'SYSTEM_SCHEDULER',
            updated_at: new Date().toISOString()
          })
        })
        this.cutoffNotification = {
          message: `Simulated 9:00 AM Cutoff executed for ${this.selectedDate}. Marked ${missing.length} missing user(s) as ABSENT.`,
          absent_count: missing.length
        }
      } finally {
        this.isLoading = false
      }
    }
  }
})
