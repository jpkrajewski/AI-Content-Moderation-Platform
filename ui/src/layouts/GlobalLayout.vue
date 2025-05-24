<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Top Navigation Bar -->
    <nav class="bg-white shadow-sm">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <!-- Left side -->
          <div class="flex">
            <!-- Logo -->
            <div class="flex-shrink-0 flex items-center">
              <span class="text-xl font-bold text-blue-600">AI Moderation</span>
            </div>

            <!-- Navigation Links -->
            <div class="hidden sm:ml-6 sm:flex sm:space-x-8">
              <router-link 
                to="/secure/dashboard/summary"
                class="inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                :class="[
                  $route.path === '/secure/dashboard/summary'
                    ? 'border-blue-500 text-gray-900'
                    : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
                ]"
              >
                Dashboard Summary
              </router-link>
              <router-link 
                to="/secure/dashboard/activity-metrics"
                class="inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                :class="[
                  $route.path === '/secure/dashboard/activity-metrics'
                    ? 'border-blue-500 text-gray-900'
                    : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
                ]"
              >
                Activity Metrics
              </router-link>
              <router-link 
                to="/secure/dashboard/kpi"
                class="inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                :class="[
                  $route.path === '/secure/dashboard/kpi'
                    ? 'border-blue-500 text-gray-900'
                    : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
                ]"
              >
                Dashboard KPI
              </router-link>
              <router-link 
                to="/secure/moderation/pending"
                class="inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                :class="[
                  $route.path === '/secure/moderation/pending'
                    ? 'border-blue-500 text-gray-900'
                    : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
                ]"
              >
                Moderation
                <span class="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                  {{ pendingCountStore.count }}
                </span>
              </router-link>
              <router-link 
                to="/secure/content/submit"
                class="inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium"
                :class="[
                  $route.path === '/secure/content/submit'
                    ? 'border-blue-500 text-gray-900'
                    : 'border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700'
                ]"
              >
                Submit Content
              </router-link>
            </div>
          </div>

          <!-- Right side -->
          <div class="flex items-center">
            <!-- Version -->
            <div class="hidden sm:flex items-center mr-4">
              <span class="text-sm text-gray-500">v{{ version }}</span>
            </div>

            <!-- User Menu -->
            <div class="relative ml-3">
              <div class="flex items-center space-x-4">
                <!-- Notifications -->
                <button class="p-1 rounded-full text-gray-400 hover:text-gray-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500">
                  <span class="sr-only">View notifications</span>
                  <svg class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                  </svg>
                  <span class="absolute top-0 right-0 block h-2 w-2 rounded-full bg-red-500 ring-2 ring-white"></span>
                </button>

                <!-- Profile dropdown -->
                <div class="relative">
                  <button 
                    @click="isProfileMenuOpen = !isProfileMenuOpen"
                    class="flex items-center space-x-2 text-sm rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                  >
                    <div class="h-8 w-8 rounded-full bg-blue-600 flex items-center justify-center text-white font-medium">
                      A
                    </div>
                    <span class="text-gray-700">Admin</span>
                    <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                    </svg>
                  </button>

                  <!-- Dropdown menu -->
                  <div 
                    v-if="isProfileMenuOpen"
                    class="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5"
                  >
                    <div class="py-1">
                      <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Your Profile</a>
                      <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Settings</a>
                      <button 
                        @click="logout"
                        class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                      >
                        Sign out
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Mobile menu -->
      <div class="sm:hidden">
        <div class="pt-2 pb-3 space-y-1">
          <router-link 
            v-for="item in mobileMenuItems"
            :key="item.path"
            :to="item.path"
            class="block pl-3 pr-4 py-2 border-l-4 text-base font-medium"
            :class="[
              $route.path === item.path
                ? 'bg-blue-50 border-blue-500 text-blue-700'
                : 'border-transparent text-gray-500 hover:bg-gray-50 hover:border-gray-300 hover:text-gray-700'
            ]"
          >
            {{ item.name }}
            <span 
              v-if="item.badge"
              class="ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
              :class="item.badge.class"
            >
              {{ item.badge.text }}
            </span>
          </router-link>
        </div>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <router-view></router-view>
    </main>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useJwtStore } from '@/stores/jwt'
import { useVersionStore } from '@/stores/version'
import { usePendingCountStore } from '@/stores/pendingCount'

const router = useRouter()
const jwtStore = useJwtStore()
const versionStore = useVersionStore()
const pendingCountStore = usePendingCountStore()
const version = versionStore.version
const isProfileMenuOpen = ref(false)

let countInterval: number | null = null

onMounted(() => {
  pendingCountStore.fetchPendingCount()
  countInterval = window.setInterval(() => {
    pendingCountStore.fetchPendingCount()
  }, 30000)
})

onUnmounted(() => {
  if (countInterval) {
    clearInterval(countInterval)
  }
})

const mobileMenuItems = [
  { name: 'Dashboard Summary', path: '/secure/dashboard/summary' },
  { name: 'Activity Metrics', path: '/secure/dashboard/activity-metrics' },
  { name: 'Dashboard KPI', path: '/secure/dashboard/kpi' },
  { 
    name: 'Moderation', 
    path: '/secure/moderation/pending',
    badge: {
      text: pendingCountStore.count.toString(),
      class: 'bg-yellow-100 text-yellow-800'
    }
  },
  { name: 'Submit Content', path: '/secure/content/submit' }
]

const logout = () => {
  jwtStore.clearJwt()
  router.push('/login')
}
</script>

<style scoped>
.router-link-active {
  @apply border-blue-500 text-gray-900;
}
</style>
