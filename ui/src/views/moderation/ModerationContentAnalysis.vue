<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { getContentAnalysis } from '@/services/moderation';
import { useRoute } from 'vue-router';

const route = useRoute();
const contentId = route.params.contentId as string;

const contentAnalysis = ref('');
const loading = ref(true);
const error = ref('');

const fetchContentAnalysis = async () => {
  try {
    const data = await getContentAnalysis(contentId);
    contentAnalysis.value = JSON.stringify(data, null, 2); // Format as JSON for display
    console.log('Content analysis:', data);
  } catch {
    error.value = 'Failed to fetch content analysis.';
  } finally {
    loading.value = false;
  }
};

onMounted(fetchContentAnalysis);
</script>

<template>
  <div>
    <h1>Content Analysis</h1>
    <div v-if="loading">Loading...</div>
    <div v-else-if="error">{{ error }}</div>
    <pre v-else>{{ contentAnalysis }}</pre>
  </div>
</template>
