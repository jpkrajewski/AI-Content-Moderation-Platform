import { defineStore } from 'pinia'
import { getUiInfo } from '@/features/moderation/services/moderation'

export const usePendingCountStore = defineStore('pendingCount', {
  state: () => ({
    count: 0,
  }),
  actions: {
    async fetchPendingCount() {
      try {
        const info = await getUiInfo()
        this.count = info.contents.pending_count
      } catch (error) {
        console.error('Failed to fetch pending count:', error)
      }
    },
  },
})
