<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { listPendingContent } from '@/services/moderation';

const pendingContent = ref('');
const loading = ref(true);
const error = ref('');

const fetchPendingContent = async () => {
  try {
    const data = await listPendingContent();
    pendingContent.value = JSON.stringify(data, null, 2); // Format as JSON for display
    console.log('Pending moderation content:', data);
  } catch {
    error.value = 'Failed to fetch pending moderation content.';
  } finally {
    loading.value = false;
  }
};

onMounted(fetchPendingContent);
</script>

<template>
  <div>
    <h1>Pending Moderation Content</h1>
    <div v-if="loading">Loading...</div>
    <div v-else-if="error">{{ error }}</div>
    <pre v-else>{{ pendingContent }}</pre>
  </div>
</template>
