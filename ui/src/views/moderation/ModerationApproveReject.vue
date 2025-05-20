<script setup lang="ts">
import { ref } from 'vue';
import { approveContent, rejectContent } from '@/services/moderation';
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();
const contentId = route.params.id as string;

console.log('Content ID:', contentId);
const loading = ref(false);
const error = ref('');

const approve = async () => {
  try {
    loading.value = true;
    await approveContent(contentId);
    alert('Content approved successfully!');
    router.push('/moderation/pending');
  } catch {
    error.value = 'Failed to approve content.';
  } finally {
    loading.value = false;
  }
};

const reject = async () => {
  try {
    loading.value = true;
    await rejectContent(contentId);
    alert('Content rejected successfully!');
    router.push('/moderation/pending');
  } catch {
    error.value = 'Failed to reject content.';
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div>
    <h1>Approve or Reject Content</h1>
    <div v-if="loading">Processing...</div>
    <div v-else-if="error">{{ error }}</div>
    <div v-else>
      <h2>Content ID: {{ contentId }}</h2>
      <button @click="approve">Approve</button>
      <button @click="reject">Reject</button>
    </div>
  </div>
</template>
