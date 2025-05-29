<template>
  <div class="space-y-6">
    <div v-if="loading" class="flex justify-center items-center h-64">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
    </div>

    <div
      v-else-if="error"
      class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded"
      role="alert"
    >
      <strong class="font-bold">Error! </strong>
      <span class="block sm:inline"> {{ error }}</span>
    </div>

    <template v-else>
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

      <div v-if="moderation" class="bg-white rounded-lg shadow p-6">
        <h3 class="text-lg font-medium mb-4 text-gray-900">Moderation Statuses</h3>
        <div class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          <div class="bg-white rounded-lg shadow p-6">
            <div class="flex items-center">
              <div class="p-3 rounded-full bg-green-500">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-6 w-6 text-white"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-600">Approved</p>
                <p class="text-2xl font-semibold text-gray-900">
                  {{ moderation.statuses?.approved ?? 0 }}
                </p>
              </div>
            </div>
          </div>
          <div class="bg-white rounded-lg shadow p-6">
            <div class="flex items-center">
              <div class="p-3 rounded-full bg-yellow-500">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-6 w-6 text-white"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M3 21v-4m0 0V5a2 2 0 012-2h6a2 2 0 012 2v11m0 0l3 3m0-3l-3-3m0 3v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"
                  />
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-600">Flagged</p>
                <p class="text-2xl font-semibold text-gray-900">
                  {{ moderation.statuses?.flagged ?? 0 }}
                </p>
              </div>
            </div>
          </div>
          <div class="bg-white rounded-lg shadow p-6">
            <div class="flex items-center">
              <div class="p-3 rounded-full bg-red-500">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-6 w-6 text-white"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-600">Rejected</p>
                <p class="text-2xl font-semibold text-gray-900">
                  {{ moderation.statuses?.rejected ?? 0 }}
                </p>
              </div>
            </div>
          </div>
          <div class="bg-white rounded-lg shadow p-6">
            <div class="flex items-center">
              <div class="p-3 rounded-full bg-blue-500">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-6 w-6 text-white"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v16a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
                  />
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-600">Auto-flag Accuracy</p>
                <p class="text-2xl font-semibold text-gray-900">
                  {{ ((moderation.auto_flag_accuracy ?? 0) * 100).toFixed(2) }}%
                </p>
              </div>
            </div>
          </div>
          <div class="bg-white rounded-lg shadow p-6">
            <div class="flex items-center">
              <div class="p-3 rounded-full bg-teal-500">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-6 w-6 text-white"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
              </div>
              <div class="ml-4">
                <p class="text-sm font-medium text-gray-600">False Positive Rate</p>
                <p class="text-2xl font-semibold text-gray-900">
                  {{ ((moderation.false_positive_rate ?? 0) * 100).toFixed(2) }}%
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div v-if="insights" class="bg-white rounded-lg shadow p-6">
        <h3 class="text-lg font-medium mb-4 text-gray-900">Insights</h3>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="bg-white rounded-lg shadow p-6">
            <h4 class="font-semibold mb-4 text-gray-900">Most Common PII Types</h4>
            <ul class="space-y-2 text-gray-700">
              <li
                v-for="[pii, count] in Object.entries(insights.most_common_pii_types ?? {}).slice(
                  0,
                  5,
                )"
                :key="pii"
                class="flex justify-between items-center"
              >
                <span class="text-sm font-medium">{{ pii }}</span>
                <span class="text-sm font-semibold text-gray-900">{{ count }}</span>
              </li>
            </ul>
          </div>
          <div class="bg-white rounded-lg shadow p-6">
            <h4 class="font-semibold mb-4 text-gray-900">Most Common Toxicity Labels</h4>
            <ul class="space-y-2 text-gray-700">
              <li
                v-for="[label, count] in Object.entries(
                  insights.most_common_toxicity_labels ?? {},
                ).slice(0, 5)"
                :key="label"
                class="flex justify-between items-center"
              >
                <span class="text-sm font-medium">{{ label }}</span>
                <span class="text-sm font-semibold text-gray-900">{{ count }}</span>
              </li>
            </ul>
          </div>
          <div
            class="bg-white rounded-lg shadow p-6 flex flex-col justify-center items-center text-center"
          >
            <h4 class="font-semibold mb-2 text-gray-900">PII Detected Rate</h4>
            <p class="text-4xl font-bold text-blue-600">
              {{ (insights.pii_detected_rate ?? 0).toFixed(2) }}%
            </p>
          </div>
        </div>
      </div>

      <div v-if="content" class="bg-white rounded-lg shadow p-6">
        <h3 class="text-lg font-medium mb-4 text-gray-900">Submission Sources</h3>
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
          <div
            v-for="[source, count] in Object.entries(content.submission_sources ?? {})"
            :key="source"
            class="bg-blue-50 rounded-lg shadow-sm p-4 flex justify-between items-center border border-blue-100"
          >
            <div>
              <p class="text-xs font-semibold text-blue-700">Source:</p>
              <a
                :href="String(source)"
                target="_blank"
                class="text-blue-800 hover:underline font-medium text-sm truncate"
                >{{ source }}</a
              >
            </div>
            <div class="text-right flex flex-col items-end">
              <p class="text-xl font-bold text-blue-900">{{ count }}</p>
              <p class="text-xs text-blue-700">submissions</p>
            </div>
          </div>
        </div>
      </div>

      <div v-if="content" class="bg-white rounded-lg shadow">
        <div class="px-6 py-4 border-b border-gray-200">
          <h3 class="text-lg font-medium text-gray-900">Peak hours</h3>
        </div>
        <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3 p-6">
          <div
            v-for="[hour, count] in sortedPeakHours"
            :key="hour"
            class="bg-green-50 rounded-lg shadow-sm p-4 flex justify-between items-center border border-green-100"
          >
            <div>
              <p class="text-xs font-semibold text-green-700">Hour:</p>
              <span class="text-xl font-bold text-green-900">{{ hour }}:00</span>
            </div>
            <div class="text-right flex flex-col items-end">
              <p class="text-xl font-bold text-green-900">{{ count }}</p>
              <p class="text-xs text-green-700">submissions</p>
            </div>
          </div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { getDashboardSummary } from '@/features/dashboard/services/dashboard'
import type {
  DashboardData,
  Insights,
  Moderation,
  Content,
} from '@/features/dashboard/types/dashboard'

const loading = ref(true)
const error = ref('')
const moderation = ref<Moderation | null>(null)
const insights = ref<Insights | null>(null)
const content = ref<Content | null>(null)
const data = ref<DashboardData | null>(null)

const stats = ref([
  { title: 'Pending Review', value: '0', icon: 'ClockIcon', bgColor: 'bg-blue-500' },
  { title: 'High Risk Content', value: '0', icon: 'ExclamationIcon', bgColor: 'bg-red-500' },
  { title: 'Reviewed Today', value: '0', icon: 'CheckIcon', bgColor: 'bg-green-500' },
  { title: 'Average Response', value: '0m', icon: 'ChartIcon', bgColor: 'bg-purple-500' },
])

const fetchDashboardData = async () => {
  try {
    const response = await getDashboardSummary()
    data.value = response

    moderation.value = data.value.moderation
    insights.value = data.value.insights
    content.value = data.value.content || null

    stats.value = [
      {
        title: 'Pending Review',
        value: (data.value?.moderation?.statuses?.rejected ?? 0).toString(),
        icon: 'ClockIcon',
        bgColor: 'bg-blue-500',
      },
      {
        title: 'High Risk Content',
        value: (data.value?.insights?.most_common_toxicity_labels?.toxicity ?? 0).toString(),
        icon: 'ExclamationIcon',
        bgColor: 'bg-red-500',
      },
      {
        title: 'Reviewed Today',
        value: (data.value?.content?.submission_counts?.today ?? 0).toString(),
        icon: 'CheckIcon',
        bgColor: 'bg-green-500',
      },
      {
        title: 'Average Response',
        value: `${Math.abs(data.value?.content?.growth_rate ?? 0).toFixed(1)}m`,
        icon: 'ChartIcon',
        bgColor: 'bg-purple-500',
      },
    ]
  } catch (e) {
    console.error(e)
    error.value = 'Failed to fetch dashboard data'
  } finally {
    loading.value = false
  }
}

const sortedPeakHours = computed(() => {
  if (!content.value?.peak_hours) return []
  return Object.entries(content.value.peak_hours).sort((a, b) => Number(a[0]) - Number(b[0]))
})

onMounted(fetchDashboardData)
</script>
