<template>
  <div class="min-h-screen bg-gray-50 dark:bg-gray-900 pb-16 transition-colors duration-200">
    <LandingNav />
    <div class="pt-16">
      <router-view />
    </div>
    <AppBottomNav />
  </div>
</template>

<script setup lang="ts">
import AppBottomNav from '../components/ui/AppBottomNav.vue'
import LandingNav from '../components/ui/LandingNav.vue'
</script>
