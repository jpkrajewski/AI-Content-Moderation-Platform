<template>
  <div class="space-y-6">
    <div v-if="loading" class="flex justify-center items-center h-64">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500"></div>
    </div>

    <div
      v-else-if="error"
      class="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative"
      role="alert"
    >
      <strong class="font-bold">Error!</strong>
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
        <ul>
          <li v-for="(count, status) in moderation.statuses" :key="status" class="capitalize">
            {{ status }}: {{ count }}
          </li>
        </ul>
        <p class="mt-4">
          Auto-flag Accuracy: {{ ((moderation.auto_flag_accuracy ?? 0) * 100).toFixed(2) }}%
        </p>
        <p>False Positive Rate: {{ ((moderation.false_positive_rate ?? 0) * 100).toFixed(2) }}%</p>
      </div>

      <div v-if="insights" class="bg-white rounded-lg shadow p-6">
        <h3 class="text-lg font-medium mb-4 text-gray-900">Insights</h3>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div>
            <h4 class="font-semibold mb-2">Most Common PII Types</h4>
            <ul class="list-disc list-inside">
              <li v-for="(count, pii) in insights.most_common_pii_types ?? {}" :key="pii">
                {{ pii }}: {{ count }}
              </li>
            </ul>
          </div>
          <div>
            <h4 class="font-semibold mb-2">Most Common Toxicity Labels</h4>
            <ul class="list-disc list-inside">
              <li v-for="(count, label) in insights.most_common_toxicity_labels ?? {}" :key="label">
                {{ label }}: {{ count }}
              </li>
            </ul>
          </div>
          <div class="list-disc list-inside">
            <h4 class="font-semibold mb-2">PII Detected Rate</h4>
            <p>{{ (insights.pii_detected_rate ?? 0).toFixed(2) }}%</p>
          </div>
        </div>
      </div>

      <div v-if="content" class="bg-white rounded-lg shadow p-6">
        <h3 class="text-lg font-medium mb-4 text-gray-900">Submission Sources</h3>
        <ul>
          <li v-for="(count, source) in content.submission_sources ?? {}" :key="source">
            <a :href="String(source)" target="_blank" class="text-blue-600 hover:underline">{{
              source
            }}</a
            >: {{ count }}
          </li>
        </ul>
      </div>

      <div v-if="content" class="bg-white rounded-lg shadow">
        <div class="px-6 py-4 border-b">
          <h3 class="text-lg font-medium text-gray-900">Peak hours</h3>
        </div>
        <div class="divide-y">
          <div
            v-for="[hour, count] in sortedPeakHours"
            :key="hour"
            class="p-6 flex justify-between"
          >
            <span>Hour: {{ hour }}:00</span>
            <span class="font-semibold">{{ count }} submissions</span>
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
  ContentItem,
  Moderation,
} from '@/features/dashboard/types/dashboard'

const loading = ref(true)
const error = ref('')
const moderation = ref<Moderation | null>(null)
const insights = ref<Insights | null>(null)
const content = ref<ContentItem | null>(null)
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

    if (data.value) {
      moderation.value = data.value.moderation_stats
      insights.value = data.value.insights
      content.value = data.value.recent_content?.[0] || null

      stats.value = [
        {
          title: 'Pending Review',
          value: (data.value.pending_review ?? 0).toString(),
          icon: 'ClockIcon',
          bgColor: 'bg-blue-500',
        },
        {
          title: 'High Risk Content',
          value: (data.value.flagged_content ?? 0).toString(),
          icon: 'ExclamationIcon',
          bgColor: 'bg-red-500',
        },
        {
          title: 'Reviewed Today',
          value: (data.value.total_submissions ?? 0).toString(),
          icon: 'CheckIcon',
          bgColor: 'bg-green-500',
        },
        {
          title: 'Average Response',
          value: `${(data.value.insights?.average_response_time ?? 0).toFixed(1)}m`,
          icon: 'ChartIcon',
          bgColor: 'bg-purple-500',
        },
      ]
    }
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
