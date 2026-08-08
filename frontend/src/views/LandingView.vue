<template>
  <div class="min-h-screen bg-[#0b0f17] text-gray-100 selection:bg-indigo-500 selection:text-white relative overflow-hidden">
    <!-- Background Glowing Orbs -->
    <div class="absolute top-0 left-1/4 w-96 h-96 bg-indigo-600/15 rounded-full blur-3xl pointer-events-none"></div>
    <div class="absolute top-1/3 right-1/4 w-96 h-96 bg-purple-600/15 rounded-full blur-3xl pointer-events-none"></div>
    <div class="absolute bottom-10 left-1/3 w-[30rem] h-[30rem] bg-emerald-600/10 rounded-full blur-3xl pointer-events-none"></div>

    <!-- Navigation Bar -->
    <header class="border-b border-gray-800/80 bg-gray-950/80 sticky top-0 z-50 backdrop-blur-xl">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
        <!-- Logo -->
        <div class="flex items-center gap-3">
          <div class="p-2.5 rounded-2xl bg-gradient-to-tr from-indigo-600 via-purple-600 to-pink-600 text-white shadow-lg shadow-indigo-600/30">
            <ScanFace class="w-6 h-6" />
          </div>
          <div>
            <span class="text-xl font-extrabold tracking-tight text-white flex items-center gap-2">
              BioCheck<span class="text-indigo-400">Pro</span>
              <span class="text-[10px] bg-indigo-500/10 text-indigo-300 border border-indigo-500/20 px-2 py-0.5 rounded-full font-mono uppercase">
                v1.0 Supabase pgvector
              </span>
            </span>
          </div>
        </div>

        <!-- Navigation CTAs -->
        <div class="flex items-center gap-3">
          <router-link
            to="/kiosk"
            class="px-4 py-2 rounded-xl bg-gray-900 hover:bg-gray-800 border border-gray-700/80 text-gray-200 hover:text-white text-xs font-semibold flex items-center gap-2 transition-all shadow-md"
          >
            <Camera class="w-4 h-4 text-indigo-400" />
            <span class="hidden sm:inline">Launch User Kiosk</span>
          </router-link>

          <router-link
            to="/admin"
            class="px-4 py-2 rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold flex items-center gap-2 transition-all shadow-lg shadow-indigo-600/30"
          >
            <ShieldCheck class="w-4 h-4" />
            <span>Admin Portal</span>
          </router-link>
        </div>
      </div>
    </header>

    <!-- Hero Section -->
    <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-16 pb-20 text-center relative z-10 space-y-8">
      <!-- Badge Pill -->
      <div class="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-indigo-500/10 border border-indigo-500/20 text-indigo-300 text-xs font-medium animate-fade-in shadow-inner">
        <Sparkles class="w-4 h-4 text-indigo-400" />
        <span>Next-Generation Biometric Attendance & Hardware Control</span>
      </div>

      <!-- Main Headline -->
      <h1 class="text-4xl sm:text-6xl lg:text-7xl font-extrabold tracking-tight text-white max-w-4xl mx-auto leading-tight">
        Automated Biometric Attendance Powered by <span class="bg-gradient-to-r from-indigo-400 via-purple-400 to-pink-400 bg-clip-text text-transparent">AI & pgvector</span>
      </h1>

      <!-- Subtitle -->
      <p class="text-base sm:text-lg text-gray-300 max-w-2xl mx-auto font-normal leading-relaxed">
        Real-time facial vector matching, WebAuthn hardware fingerprint authentication, automated 9:00 AM daily absentee scheduling, and audit-logged admin overrides.
      </p>

      <!-- Primary Action Buttons -->
      <div class="flex flex-col sm:flex-row items-center justify-center gap-4 pt-4">
        <router-link
          to="/kiosk"
          class="w-full sm:w-auto px-8 py-4 rounded-2xl bg-gradient-to-r from-indigo-600 via-purple-600 to-pink-600 hover:from-indigo-500 hover:to-pink-500 text-white font-bold text-sm shadow-2xl shadow-indigo-600/40 flex items-center justify-center gap-3 transition-all transform hover:-translate-y-0.5"
        >
          <Camera class="w-5 h-5" />
          <span>Launch Employee Kiosk Terminal</span>
          <ArrowRight class="w-4 h-4" />
        </router-link>

        <router-link
          to="/admin"
          class="w-full sm:w-auto px-8 py-4 rounded-2xl bg-gray-900/90 hover:bg-gray-800 border border-gray-700/80 text-gray-100 font-semibold text-sm shadow-xl flex items-center justify-center gap-3 transition-all"
        >
          <LayoutDashboard class="w-5 h-5 text-indigo-400" />
          <span>Open Admin Dashboard</span>
        </router-link>
      </div>

      <!-- Feature Grid Highlights -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-5xl mx-auto pt-12">
        <div class="glass-panel p-5 rounded-2xl border border-gray-800/80 text-left space-y-2">
          <div class="p-2.5 rounded-xl bg-indigo-500/10 text-indigo-400 w-fit">
            <ScanFace class="w-5 h-5" />
          </div>
          <div class="text-sm font-bold text-white">128-d Face Vector AI</div>
          <div class="text-xs text-gray-400">Supabase <code>pgvector</code> HNSW cosine similarity search.</div>
        </div>

        <div class="glass-panel p-5 rounded-2xl border border-gray-800/80 text-left space-y-2">
          <div class="p-2.5 rounded-xl bg-purple-500/10 text-purple-400 w-fit">
            <Fingerprint class="w-5 h-5" />
          </div>
          <div class="text-sm font-bold text-white">WebAuthn Hardware</div>
          <div class="text-xs text-gray-400">Native browser API for USB & TouchID hardware sensors.</div>
        </div>

        <div class="glass-panel p-5 rounded-2xl border border-gray-800/80 text-left space-y-2">
          <div class="p-2.5 rounded-xl bg-amber-500/10 text-amber-400 w-fit">
            <Clock class="w-5 h-5" />
          </div>
          <div class="text-sm font-bold text-white">9:00 AM Cutoff Cron</div>
          <div class="text-xs text-gray-400">APScheduler auto-inserts missing users as <code>ABSENT</code>.</div>
        </div>

        <div class="glass-panel p-5 rounded-2xl border border-gray-800/80 text-left space-y-2">
          <div class="p-2.5 rounded-xl bg-emerald-500/10 text-emerald-400 w-fit">
            <ShieldCheck class="w-5 h-5" />
          </div>
          <div class="text-sm font-bold text-white">Audit Override Log</div>
          <div class="text-xs text-gray-400">Mandatory justification reasons stored in immutable audit table.</div>
        </div>
      </div>
    </section>

    <!-- Architecture & Specs Section -->
    <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 border-t border-gray-800/80">
      <div class="text-center space-y-3 mb-12">
        <h2 class="text-2xl sm:text-3xl font-extrabold text-white">Full-Stack System Architecture</h2>
        <p class="text-xs sm:text-sm text-gray-400 max-w-xl mx-auto">Production tech stack designed for speed, security, and hardware sensor integration.</p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
        <!-- Database Card -->
        <div class="glass-panel p-6 rounded-2xl border border-gray-800/80 space-y-4">
          <div class="flex items-center gap-3">
            <div class="p-3 rounded-xl bg-emerald-500/10 text-emerald-400">
              <Database class="w-6 h-6" />
            </div>
            <div>
              <h3 class="text-base font-bold text-white">Database & Auth</h3>
              <p class="text-xs text-gray-400">Supabase PostgreSQL</p>
            </div>
          </div>
          <ul class="text-xs text-gray-300 space-y-2 font-mono">
            <li class="flex items-center gap-2">
              <CheckCircle2 class="w-4 h-4 text-emerald-400 shrink-0" />
              <span>pgvector (128-d face embeddings)</span>
            </li>
            <li class="flex items-center gap-2">
              <CheckCircle2 class="w-4 h-4 text-emerald-400 shrink-0" />
              <span>Row Level Security (RLS) policies</span>
            </li>
            <li class="flex items-center gap-2">
              <CheckCircle2 class="w-4 h-4 text-emerald-400 shrink-0" />
              <span>Immutable audit_logs table</span>
            </li>
          </ul>
        </div>

        <!-- Backend Card -->
        <div class="glass-panel p-6 rounded-2xl border border-gray-800/80 space-y-4">
          <div class="flex items-center gap-3">
            <div class="p-3 rounded-xl bg-indigo-500/10 text-indigo-400">
              <Server class="w-6 h-6" />
            </div>
            <div>
              <h3 class="text-base font-bold text-white">Backend API</h3>
              <p class="text-xs text-gray-400">Python FastAPI & APScheduler</p>
            </div>
          </div>
          <ul class="text-xs text-gray-300 space-y-2 font-mono">
            <li class="flex items-center gap-2">
              <CheckCircle2 class="w-4 h-4 text-indigo-400 shrink-0" />
              <span>NumPy cosine distance math</span>
            </li>
            <li class="flex items-center gap-2">
              <CheckCircle2 class="w-4 h-4 text-indigo-400 shrink-0" />
              <span>Daily 9:00 AM absentee automation</span>
            </li>
            <li class="flex items-center gap-2">
              <CheckCircle2 class="w-4 h-4 text-indigo-400 shrink-0" />
              <span>Pydantic type-safe validation</span>
            </li>
          </ul>
        </div>

        <!-- Frontend Card -->
        <div class="glass-panel p-6 rounded-2xl border border-gray-800/80 space-y-4">
          <div class="flex items-center gap-3">
            <div class="p-3 rounded-xl bg-purple-500/10 text-purple-400">
              <LayoutDashboard class="w-6 h-6" />
            </div>
            <div>
              <h3 class="text-base font-bold text-white">Frontend SPA</h3>
              <p class="text-xs text-gray-400">Vue 3 & Tailwind CSS</p>
            </div>
          </div>
          <ul class="text-xs text-gray-300 space-y-2 font-mono">
            <li class="flex items-center gap-2">
              <CheckCircle2 class="w-4 h-4 text-purple-400 shrink-0" />
              <span>Composition API & Pinia Store</span>
            </li>
            <li class="flex items-center gap-2">
              <CheckCircle2 class="w-4 h-4 text-purple-400 shrink-0" />
              <span>Dynamic @unhead/vue SEO Head</span>
            </li>
            <li class="flex items-center gap-2">
              <CheckCircle2 class="w-4 h-4 text-purple-400 shrink-0" />
              <span>WebRTC Camera & WebAuthn API</span>
            </li>
          </ul>
        </div>
      </div>
    </section>

    <!-- Footer -->
    <footer class="border-t border-gray-900 py-8 text-center text-xs text-gray-500">
      <div class="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div>
          BioCheckPro Attendance System &copy; 2026. Built with Python FastAPI, Vue 3, & Supabase.
        </div>
        <div class="flex items-center gap-4 text-gray-400">
          <router-link to="/kiosk" class="hover:text-white">User Kiosk</router-link>
          <router-link to="/admin" class="hover:text-white">Admin Portal</router-link>
          <a href="https://github.com/Feliciencalyx/attendance-sstm" target="_blank" class="hover:text-white">GitHub Repo</a>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup>
import { useHead } from '@unhead/vue'
import { 
  ScanFace, 
  Camera, 
  ShieldCheck, 
  Sparkles, 
  ArrowRight, 
  LayoutDashboard, 
  Fingerprint, 
  Clock, 
  Database, 
  Server, 
  CheckCircle2 
} from 'lucide-vue-next'

useHead({
  title: 'BioCheckPro - Enterprise Biometric Attendance System',
  meta: [
    { name: 'description', content: 'Enterprise Biometric Attendance Management System featuring AI facial vector recognition, WebAuthn fingerprint validation, and automated 9:00 AM absentee cutoff rules.' },
    { property: 'og:title', content: 'BioCheckPro Biometric Attendance' },
    { property: 'og:description', content: 'Explore the live biometric user scanning kiosk and admin dashboard.' }
  ]
})
</script>
