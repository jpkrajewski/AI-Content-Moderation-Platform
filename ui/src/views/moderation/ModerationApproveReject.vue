<script setup lang="ts">
import { ref } from 'vue'
import { moderateContent } from '@/features/moderation/services/moderation'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()
const contentId = route.params.id as string

const loading = ref(false)
const error = ref('')

const approve = async () => {
  try {
    loading.value = true
    await moderateContent(contentId, 'approve')
    alert('Content approved successfully!')
    router.push('/moderation/pending')
  } catch {
    error.value = 'Failed to approve content.'
  } finally {
    loading.value = false
  }
}

const reject = async () => {
  try {
    loading.value = true
    await moderateContent(contentId, 'reject')
    alert('Content rejected successfully!')
    router.push('/moderation/pending')
  } catch {
    error.value = 'Failed to reject content.'
  } finally {
    loading.value = false
  }
}
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
