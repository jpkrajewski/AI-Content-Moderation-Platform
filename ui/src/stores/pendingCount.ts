import { defineStore } from 'pinia'
import { getModerationInfo } from '@/features/moderation/services/moderation'

export const usePendingCountStore = defineStore('pendingCount', {
  state: () => ({
    count: 0,
  }),
  actions: {
    async fetchPendingCount() {
      try {
        const info = await getModerationInfo()
        this.count = info.pending_count
      } catch (error) {
        console.error('Failed to fetch pending count:', error)
      }
    },
  },
})
