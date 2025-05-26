import { defineStore } from 'pinia'
import { ref } from 'vue'
import { listPendingContent } from '@/services/moderation'

export const usePendingCountStore = defineStore('pendingCount', () => {
  const count = ref(0)
  const loading = ref(false)
  const error = ref('')

  const fetchPendingCount = async () => {
    try {
      loading.value = true
      const data = await listPendingContent()
      count.value = Array.isArray(data) ? data.length : 0
    } catch (err) {
      error.value = 'Failed to fetch pending count'
      console.error('Failed to fetch pending count:', err)
    } finally {
      loading.value = false
    }
  }

  return {
    count,
    loading,
    error,
    fetchPendingCount
  }
}) 