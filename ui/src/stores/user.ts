import { defineStore } from 'pinia'
import { authService } from '@/features/auth/services/auth'
import type { User, UserState, LoginCredentials, RegisterData } from '@/features/auth/types/user'
import { useNotificationStore } from './notification'

export const useUserStore = defineStore('user', {
  state: (): UserState => ({
    currentUser: null,
    isAuthenticated: false,
    loading: false,
    error: null,
  }),

  getters: {
    isAdmin: (state) => state.currentUser?.scope === 'admin',
    isModerator: (state) => state.currentUser?.scope === 'moderator',
  },

  actions: {
    async login(credentials: LoginCredentials) {
      this.loading = true
      this.error = null
      const notificationStore = useNotificationStore()

      try {
        const { user } = await authService.login(credentials)
        this.currentUser = user
        this.isAuthenticated = true
        notificationStore.addNotification({
          type: 'success',
          message: 'Successfully logged in',
        })
      } catch (error) {
        this.error = 'Failed to login'
        notificationStore.addNotification({
          type: 'error',
          message: 'Failed to login. Please check your credentials.',
        })
        throw error
      } finally {
        this.loading = false
      }
    },

    async register(data: RegisterData) {
      this.loading = true
      this.error = null
      const notificationStore = useNotificationStore()

      try {
        const { user } = await authService.register(data)
        this.currentUser = user
        this.isAuthenticated = true
        notificationStore.addNotification({
          type: 'success',
          message: 'Successfully registered',
        })
      } catch (error) {
        this.error = 'Failed to register'
        notificationStore.addNotification({
          type: 'error',
          message: 'Failed to register. Please try again.',
        })
        throw error
      } finally {
        this.loading = false
      }
    },

    async logout() {
      const notificationStore = useNotificationStore()
      try {
        await authService.logout()
        this.currentUser = null
        this.isAuthenticated = false
        notificationStore.addNotification({
          type: 'success',
          message: 'Successfully logged out',
        })
      } catch (error) {
        notificationStore.addNotification({
          type: 'error',
          message: 'Failed to log out',
        })
        throw error
      }
    },

    setUser(user: User) {
      this.currentUser = user
      this.isAuthenticated = true
    },

    clearUser() {
      this.currentUser = null
      this.isAuthenticated = false
    },
  },
})
