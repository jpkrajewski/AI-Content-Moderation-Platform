
<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { getDashboardSummary } from '@/services/dashboard';


const summaryData = ref("");
const loading = ref(true);
const error = ref("");

const fetchSummary = async () => {
    try {
    const data = await getDashboardSummary();
    summaryData.value = JSON.stringify(data, null, 2);
    console.log('Dashboard summary:', data);
    } catch {
    error.value = 'Failed to fetch dashboard summary.';
    } finally {
    loading.value = false;
    }
};

onMounted(fetchSummary);
</script>

<template>
  <div>
    <h1>Dashboard Summary</h1>
    <div v-if="loading">Loading...</div>
    <div v-else-if="error">{{ error }}</div>
    <pre v-else>{{ summaryData }}</pre>
    <h2>Summary Data</h2>
  </div>
</template>
