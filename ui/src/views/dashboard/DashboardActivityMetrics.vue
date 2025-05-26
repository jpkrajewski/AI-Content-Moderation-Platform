<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getUserActivityMetrics } from '@/services/dashboard'

const metricsData = ref('')
const loading = ref(true)
const error = ref('')

const fetchActivityMetrics = async () => {
  try {
    const data = await getUserActivityMetrics()
    metricsData.value = JSON.stringify(data, null, 2)
  } catch {
    error.value = 'Failed to fetch dashboard summary.'
  } finally {
    loading.value = false
  }
}

onMounted(fetchActivityMetrics)
</script>

<template>
  <div>
    <h1>Dashboard Activity Metrics</h1>
    <div v-if="loading">Loading...</div>
    <div v-else-if="error">{{ error }}</div>
    <pre v-else>{{ metricsData }}</pre>
  </div>
</template>
