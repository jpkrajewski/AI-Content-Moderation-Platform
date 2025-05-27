import { defineStore } from 'pinia'
import { v4 as uuidv4 } from 'uuid'
import type { Notification } from '@/shared/types/notification'

export const useNotificationStore = defineStore('notification', {
  state: (): { notifications: Notification[] } => ({
    notifications: [],
  }),

  actions: {
    addNotification(notification: Omit<Notification, 'id'>) {
      const id = uuidv4()
      this.notifications.push({ ...notification, id })

      if (notification.duration !== 0) {
        setTimeout(() => {
          this.removeNotification(id)
        }, notification.duration || 5000)
      }
    },

    removeNotification(id: string) {
      const index = this.notifications.findIndex((n) => n.id === id)
      if (index !== -1) {
        this.notifications.splice(index, 1)
      }
    },
  },
})
