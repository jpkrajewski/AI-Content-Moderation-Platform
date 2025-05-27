import { defineStore } from 'pinia'
import { getCurrentVersion } from '@/shared/utils/misc'

export const useVersionStore = defineStore('version', {
  state: () => ({
    version: 'Unknown',
  }),
  actions: {
    async fetchVersion() {
      try {
        const data = await getCurrentVersion()
        this.version = data.version
      } catch (error) {
        console.error(`Fetch version error! ${error}`)
      }
    },
  },
})
