import { defineStore } from 'pinia';
import { getCurrentVersion } from '@/services/misc';

export const useVersionStore = defineStore('version', {
  state: () => ({
    version: 'Unknown',
  }),
  actions: {
    async fetchVersion() {
      try {
        const data = await getCurrentVersion();
        this.version = data.version;
        console.log('App version:', this.version);
      } catch (error) {
        console.error('Failed to fetch app version:', error);
      }
    },
  },
});
