<template>
  <div class="space-y-6">
    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center h-64">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
      <strong class="font-bold">Error!</strong>
      <span class="block sm:inline"> {{ error }}</span>
    </div>

    <!-- Content -->
    <template v-else>
      <!-- Stats Overview -->
      <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <div v-for="stat in stats" :key="stat.title" class="bg-white rounded-lg shadow p-6">
          <div class="flex items-center">
            <div class="p-3 rounded-full" :class="stat.bgColor">
              <component :is="stat.icon" class="w-6 h-6 text-white" />
            </div>
            <div class="ml-4">
              <p class="text-sm font-medium text-gray-600">{{ stat.title }}</p>
              <p class="text-2xl font-semibold text-gray-900">{{ stat.value }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Recent Content -->
      <div class="bg-white rounded-lg shadow">
        <div class="px-6 py-4 border-b">
          <h3 class="text-lg font-medium text-gray-900">Recent Content</h3>
        </div>
        <div class="divide-y">
          <div v-for="content in recentContent" :key="content.id" class="p-6">
            <div class="flex items-center justify-between">
              <div class="flex items-center space-x-4">
                <div class="flex-shrink-0">
                  <img :src="content.thumbnail" :alt="content.title" class="w-12 h-12 rounded-lg object-cover">
                </div>
                <div>
                  <h4 class="text-sm font-medium text-gray-900">{{ content.title }}</h4>
                  <p class="text-sm text-gray-500">{{ content.type }} • {{ content.date }}</p>
                </div>
              </div>
              <div class="flex items-center space-x-4">
                <div class="flex items-center">
                  <div class="w-24 bg-gray-200 rounded-full h-2.5">
                    <div 
                      class="h-2.5 rounded-full" 
                      :class="getToxicityColor(content.toxicity)"
                      :style="{ width: `${content.toxicity}%` }"
                    ></div>
                  </div>
                  <span class="ml-2 text-sm font-medium" :class="getToxicityTextColor(content.toxicity)">
                    {{ content.toxicity }}%
                  </span>
                </div>
                <button class="text-gray-400 hover:text-gray-500">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getDashboardSummary } from '@/services/dashboard'

const loading = ref(true)
const error = ref('')
const stats = ref([
  {
    title: 'Pending Review',
    value: '0',
    icon: 'ClockIcon',
    bgColor: 'bg-blue-500'
  },
  {
    title: 'High Risk Content',
    value: '0',
    icon: 'ExclamationIcon',
    bgColor: 'bg-red-500'
  },
  {
    title: 'Reviewed Today',
    value: '0',
    icon: 'CheckIcon',
    bgColor: 'bg-green-500'
  },
  {
    title: 'Average Response',
    value: '0m',
    icon: 'ChartIcon',
    bgColor: 'bg-purple-500'
  }
])

const recentContent = ref([])

const getToxicityColor = (toxicity: number) => {
  if (toxicity >= 70) return 'bg-red-500'
  if (toxicity >= 40) return 'bg-yellow-500'
  return 'bg-green-500'
}

const getToxicityTextColor = (toxicity: number) => {
  if (toxicity >= 70) return 'text-red-500'
  if (toxicity >= 40) return 'text-yellow-500'
  return 'text-green-500'
}

const fetchDashboardData = async () => {
  try {
    const data = await getDashboardSummary()
    
    stats.value = [
      {
        title: 'Pending Review',
        value: data.pendingReview?.toString() || '0',
        icon: 'ClockIcon',
        bgColor: 'bg-blue-500'
      },
      {
        title: 'High Risk Content',
        value: data.highRiskContent?.toString() || '0',
        icon: 'ExclamationIcon',
        bgColor: 'bg-red-500'
      },
      {
        title: 'Reviewed Today',
        value: data.reviewedToday?.toString() || '0',
        icon: 'CheckIcon',
        bgColor: 'bg-green-500'
      },
      {
        title: 'Average Response',
        value: `${data.averageResponseTime || 0}m`,
        icon: 'ChartIcon',
        bgColor: 'bg-purple-500'
      }
    ]

    recentContent.value = data.recentContent?.map((content: any) => ({
      id: content.id,
      title: content.title,
      type: content.type,
      date: content.date,
      toxicity: content.toxicity,
      thumbnail: content.thumbnail || 'https://via.placeholder.com/48'
    })) || []

  } catch (err) {
    error.value = 'Failed to fetch dashboard data'
  } finally {
    loading.value = false
  }
}

onMounted(fetchDashboardData)
</script> 