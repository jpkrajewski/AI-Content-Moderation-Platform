import axiosInstance from '@/api/interceptors/interceptor'
import { endpoints } from '@/shared/constants/endpoints'
import type { AxiosError } from 'axios'
import type { ApiKey } from '../types'

export const apiKeysService = {
  async fetchApiKeys(): Promise<ApiKey[]> {
    try {
      const response = await axiosInstance.get<ApiKey[]>(endpoints.moderation.getApiKeys)
      return response.data
    } catch (error) {
      console.error('Error fetching API keys:', error as AxiosError)
      throw error
    }
  },

  async createApiKey(payload: {
    source: string
    client_id: string
    current_scope: string[]
  }): Promise<ApiKey> {
    try {
      const response = await axiosInstance.post<ApiKey>(endpoints.moderation.createApiKey, payload)
      return response.data
    } catch (error) {
      console.error('Error creating API key:', error as AxiosError)
      throw error
    }
  },

  async deactivateApiKey(id: string): Promise<void> {
    try {
      await axiosInstance.patch(endpoints.moderation.deactivateApiKey(id))
    } catch (error) {
      console.error(`Error deactivating API Key ${id}:`, error as AxiosError)
      throw error
    }
  },

  async reactivateApiKey(id: string): Promise<void> {
    try {
      await axiosInstance.patch(endpoints.moderation.reactivateApiKey(id))
    } catch (error) {
      console.error(`Error reactivating API Key ${id}:`, error as AxiosError)
      throw error
    }
  },

  async deleteApiKey(id: string): Promise<void> {
    try {
      await axiosInstance.delete(endpoints.moderation.deleteApiKey(id))
    } catch (error) {
      console.error(`Error deleting API Key ${id}:`, error as AxiosError)
      throw error
    }
  },
}
