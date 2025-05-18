<script setup lang="ts">
import { ref } from 'vue';
import { flagContent } from '@/services/moderation';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();
const contentId = route.params.contentId as string;

const loading = ref(false);
const error = ref('');

const flag = async () => {
  try {
    loading.value = true;
    await flagContent(contentId);
    alert('Content flagged successfully!');
    router.push('/moderation/pending'); // Redirect after action
  } catch {
    error.value = 'Failed to flag content.';
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div>
    <h1>Flag Content</h1>
    <div v-if="loading">Processing...</div>
    <div v-else-if="error">{{ error }}</div>
    <div v-else>
      <h2>Content ID: {{ contentId }}</h2>
      <button @click="flag">Flag Content</button>
    </div>
  </div>
</template>
