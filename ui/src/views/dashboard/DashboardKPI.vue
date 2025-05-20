<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { getModerationKPI } from '@/services/dashboard';


const kpiData = ref("");
const loading = ref(true);
const error = ref("");

const fetchKPI = async () => {
    try {
    const data = await getModerationKPI();
    kpiData.value = JSON.stringify(data, null, 2);
    } catch {
    error.value = 'Failed to fetch dashboard summary.';
    } finally {
    loading.value = false;
    }
};

onMounted(fetchKPI);
</script>

<template>
  <div>
    <h1>Dashboard KPI</h1>
    <div v-if="loading">Loading...</div>
    <div v-else-if="error">{{ error }}</div>
    <pre v-else>{{ kpiData }}</pre>
    <h2>Summary KPI</h2>
  </div>
</template>
