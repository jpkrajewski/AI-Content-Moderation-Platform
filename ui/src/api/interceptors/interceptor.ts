import axios from 'axios'
import { useJwtStore } from '@/features/auth/stores/jwt'
import router from '@/router'
import { useNotificationStore } from '@/features/auth/stores/notification'
import { authService } from '@/features/auth/services/auth'
import { isJwtValid } from '@/shared/utils/jwt'

const axiosInstance = axios.create({
  baseURL: 'http://localhost:8080/api/v1',
})

let isRefreshing = false
type FailedQueueItem = { resolve: (token: string | null) => void; reject: (error: unknown) => void }
let failedQueue: FailedQueueItem[] = []
let refreshPromise: Promise<void> | null = null

const PUBLIC_ENDPOINTS = ['/auth/login', '/auth/register', '/auth/refresh', '/version']

function processQueue(error: unknown, token: string | null = null) {
  failedQueue.forEach((prom) => {
    if (error) {
      prom.reject(error)
    } else {
      prom.resolve(token)
    }
  })
  failedQueue = []
}

axiosInstance.interceptors.request.use(
  async (config) => {
    if (PUBLIC_ENDPOINTS.some((endpoint) => config.url?.includes(endpoint))) {
      return config
    }

    let token = localStorage.getItem('jwt') || ''
    let refreshToken = localStorage.getItem('refresh_token') || ''

    if (!token || !refreshToken || !isJwtValid(token)) {
      if (refreshToken) {
        if (!refreshPromise) {
          refreshPromise = authService
            .refreshToken(refreshToken)
            .then((data) => {
              token = data.token || ''
              refreshToken = data.refresh || ''
              localStorage.setItem('jwt', token)
              localStorage.setItem('refresh_token', refreshToken)
            })
            .catch(() => {
              localStorage.removeItem('jwt')
              localStorage.removeItem('refresh_token')
              router.push('/login')
              throw new Error('Session expired')
            })
            .finally(() => {
              refreshPromise = null
            })
        }
        await refreshPromise
        token = localStorage.getItem('jwt') || ''
      } else {
        localStorage.removeItem('jwt')
        localStorage.removeItem('refresh_token')
        router.push('/login')
        throw new Error('Session expired')
      }
    }

    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  },
)

axiosInstance.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    if (error.response?.status === 403 && !originalRequest._retry) {
      const jwtStore = useJwtStore()
      const notificationStore = useNotificationStore()
      const refreshToken = jwtStore.refreshToken
      if (!refreshToken) {
        jwtStore.clearTokens()
        notificationStore.addNotification({
          type: 'warning',
          message: 'Your session has expired. Please log in again.',
          duration: 5000,
        })
        router.push('/login')
        return Promise.reject(error)
      }
      if (isRefreshing) {
        return new Promise(function (resolve, reject) {
          failedQueue.push({ resolve, reject })
        })
          .then((token) => {
            originalRequest.headers['Authorization'] = 'Bearer ' + token
            originalRequest._retry = true
            return axiosInstance(originalRequest)
          })
          .catch((err) => {
            return Promise.reject(err)
          })
      }
      originalRequest._retry = true
      isRefreshing = true
      return new Promise((resolve, reject) => {
        ;(async () => {
          try {
            const data = await authService.refreshToken(refreshToken)
            jwtStore.setTokens(data.token, data.refresh)
            axiosInstance.defaults.headers.common['Authorization'] = 'Bearer ' + data.token
            processQueue(null, data.token)
            originalRequest.headers['Authorization'] = 'Bearer ' + data.token
            resolve(axiosInstance(originalRequest))
          } catch (err: unknown) {
            processQueue(err, null)
            jwtStore.clearTokens()
            notificationStore.addNotification({
              type: 'warning',
              message: 'Your session has expired. Please log in again.',
              duration: 5000,
            })
            router.push('/login')
            reject(err)
          } finally {
            isRefreshing = false
          }
        })()
      })
    }
    if (error.response?.status === 400) {
      const jwtStore = useJwtStore()
      const notificationStore = useNotificationStore()
      jwtStore.clearJwt()
      notificationStore.addNotification({
        type: 'warning',
        message: 'Your session has expired. Please log in again.',
        duration: 5000,
      })
      router.push('/login')
    }
    return Promise.reject(error)
  },
)

export default axiosInstance
