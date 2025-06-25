import axiosInstance from '@/api/interceptors/interceptor'
import axios from 'axios'
import type { LoginCredentials, RegisterData, User } from '../types/user'
import { endpoints } from '@/shared/constants/endpoints'

export const authService = {
  async login(credentials: LoginCredentials) {
    const response = await axiosInstance.post('/auth/login', credentials)
    return response.data
  },

  async register(data: RegisterData) {
    const response = await axiosInstance.post('/auth/register', data)
    return response.data
  },

  async logout() {
    await axiosInstance.post('/auth/logout')
  },

  async getCurrentUser(): Promise<User> {
    const response = await axiosInstance.get('/auth/me')
    return response.data
  },

  async initGoogleLogin() {
    window.location.href = 'http://localhost:8080/api/v1/auth/oauth/login'
  },

  async refreshToken(refreshToken: string) {
    const response = await axios.post(
      endpoints.auth.refresh,
      { refresh_token: refreshToken },
      {
        baseURL: 'http://localhost:8080/api/v1',
      },
    )
    return response.data
  },
}
