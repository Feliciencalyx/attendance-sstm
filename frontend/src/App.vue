<template>
  <div class="min-h-screen bg-[#0b0f17] text-gray-100 font-sans antialiased selection:bg-indigo-500 selection:text-white">
    <router-view />
  </div>
</template>

<script setup>
import { useHead } from '@unhead/vue'

useHead({
  titleTemplate: '%s | Biometric Attendance Management System',
  meta: [
    { charset: 'utf-8' },
    { name: 'viewport', content: 'width=device-width, initial-scale=1' },
    { name: 'theme-color', content: '#0b0f17' }
  ],
  link: [
    { rel: 'preconnect', href: 'https://fonts.googleapis.com' },
    { rel: 'preconnect', href: 'https://fonts.gstatic.com', crossorigin: '' },
    { rel: 'stylesheet', href: 'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap' }
  ]
})
</script>
