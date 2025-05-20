<template>
  <div class="min-h-screen bg-gray-50">
    <!-- Sidebar -->
    <aside class="fixed inset-y-0 left-0 w-64 bg-white shadow-lg transform transition-transform duration-200 ease-in-out">
      <!-- Logo -->
      <div class="flex items-center justify-center h-16 border-b bg-gradient-to-r from-blue-600 to-blue-700">
        <h1 class="text-xl font-bold text-white">Content Moderation</h1>
      </div>

      <!-- Navigation -->
      <nav class="mt-6 px-4">
        <div class="space-y-1">
          <router-link 
            v-for="item in navigationItems" 
            :key="item.path"
            :to="item.path"
            class="flex items-center px-4 py-3 text-sm font-medium rounded-lg transition-colors duration-200"
            :class="[
              $route.path === item.path 
                ? 'bg-blue-50 text-blue-700' 
                : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
            ]"
          >
            <component :is="item.icon" class="w-5 h-5 mr-3" :class="$route.path === item.path ? 'text-blue-600' : 'text-gray-400'" />
            {{ item.name }}
            <span 
              v-if="item.badge" 
              class="ml-auto inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
              :class="item.badge.type === 'warning' ? 'bg-yellow-100 text-yellow-800' : 'bg-blue-100 text-blue-800'"
            >
              {{ item.badge.text }}
            </span>
          </router-link>
        </div>

        <!-- Divider -->
        <div class="mt-6 pt-6 border-t border-gray-200">
          <div class="px-4">
            <h3 class="text-xs font-semibold text-gray-500 uppercase tracking-wider">
              Settings
            </h3>
          </div>
          <div class="mt-2 space-y-1">
            <router-link 
              to="/settings"
              class="flex items-center px-4 py-3 text-sm font-medium rounded-lg transition-colors duration-200"
              :class="[
                $route.path === '/settings' 
                  ? 'bg-blue-50 text-blue-700' 
                  : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
              ]"
            >
              <svg class="w-5 h-5 mr-3" :class="$route.path === '/settings' ? 'text-blue-600' : 'text-gray-400'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              Settings
            </router-link>
          </div>
        </div>
      </nav>
    </aside>

    <!-- Main Content -->
    <div class="ml-64">
      <!-- Header -->
      <header class="bg-white shadow-sm">
        <div class="flex items-center justify-between h-16 px-8">
          <div class="flex items-center">
            <h2 class="text-lg font-semibold text-gray-800">{{ currentPageTitle }}</h2>
          </div>
          <div class="flex items-center space-x-4">
            <!-- Notifications -->
            <div class="relative">
              <button class="p-2 text-gray-600 hover:text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500 rounded-lg">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
                </svg>
                <span class="absolute top-0 right-0 block h-2 w-2 rounded-full bg-red-500 ring-2 ring-white"></span>
              </button>
            </div>

            <!-- User Menu -->
            <div class="relative">
              <button 
                class="flex items-center space-x-2 text-gray-600 hover:text-gray-800 focus:outline-none focus:ring-2 focus:ring-blue-500 rounded-lg px-3 py-2"
                @click="isUserMenuOpen = !isUserMenuOpen"
              >
                <div class="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center text-white font-medium">
                  A
                </div>
                <span class="text-sm font-medium">Admin</span>
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
                </svg>
              </button>

              <!-- Dropdown Menu -->
              <div 
                v-if="isUserMenuOpen"
                class="absolute right-0 mt-2 w-48 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5"
              >
                <div class="py-1">
                  <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Your Profile</a>
                  <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Settings</a>
                  <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100">Sign out</a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </header>

      <!-- Page Content -->
      <main class="p-8">
        <router-view></router-view>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const isUserMenuOpen = ref(false)

const navigationItems = [
  {
    name: 'Dashboard',
    path: '/',
    icon: 'HomeIcon',
    badge: {
      text: 'New',
      type: 'info'
    }
  },
  {
    name: 'Content Queue',
    path: '/queue',
    icon: 'QueueIcon',
    badge: {
      text: '24',
      type: 'warning'
    }
  },
  {
    name: 'Reports',
    path: '/reports',
    icon: 'ChartIcon'
  }
]

const currentPageTitle = computed(() => {
  return navigationItems.find(item => item.path === route.path)?.name || 'Dashboard'
})
</script>

<style scoped>
.router-link-active {
  @apply bg-blue-50 text-blue-700;
}
</style> 