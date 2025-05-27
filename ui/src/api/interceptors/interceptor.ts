import axios from 'axios'
import { useJwtStore } from '@/features/auth/stores/jwt'
import { useRouter } from 'vue-router'
import { useNotificationStore } from '@/features/auth/stores/notification'

const axiosInstance = axios.create({
  baseURL: 'http://localhost:8080/api/v1',
})

axiosInstance.interceptors.request.use(
  (config) => {
    const jwtStore = useJwtStore()
    const token = jwtStore.jwt
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
  (error) => {
    if (error.response?.status === 400) {
      const jwtStore = useJwtStore()
      const router = useRouter()
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
