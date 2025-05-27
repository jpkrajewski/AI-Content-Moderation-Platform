import { defineStore } from 'pinia'
import { listPendingContent } from '@/features/moderation/services/moderation'

export const usePendingCountStore = defineStore('pendingCount', {
  state: () => ({
    count: 0,
  }),
  actions: {
    async fetchPendingCount() {
      try {
        const content = await listPendingContent()
        this.count = content.length
      } catch (error) {
        console.error('Failed to fetch pending count:', error)
      }
    },
  },
})
