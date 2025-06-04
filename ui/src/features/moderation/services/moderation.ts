import axiosInstance from '@/api/interceptors/interceptor'
import type { ContentItem } from '../types/moderation'

interface PaginationParams {
  page: number
  page_size: number
}

export interface ModerationInfo {
  pending_count: number
}

export interface ApiKeyInfo {
  active_count: number
  deactivated_count: number
  all_count: number
}

export interface UiInfo {
  contents: ModerationInfo
  api_keys: ApiKeyInfo
}

export const listPendingContent = async (params: PaginationParams): Promise<ContentItem[]> => {
  const response = await axiosInstance.get('/moderation/pending', { params })
  return response.data
}

export const moderateContent = async (
  contentId: string,
  decision: 'approve' | 'reject',
  reason?: string,
) => {
  const url = `/moderation/${contentId}/${decision}`
  const response = await axiosInstance.post(url, { reason })
  return response.data
}

export const getContentHistory = async (): Promise<ContentItem[]> => {
  const response = await axiosInstance.get('/moderation/history')
  return response.data
}

export const analyzeContent = async (contentId: string) => {
  const response = await axiosInstance.post(`/moderation/${contentId}`)
  return response.data
}

export const getContentAnalysis = async (contentId: string): Promise<ContentItem> => {
  const response = await axiosInstance.get(`/moderation/${contentId}`)
  return response.data
}

export const flagContent = async (contentId: string, reason?: string) => {
  const response = await axiosInstance.post(`/moderation/${contentId}/flag`, { reason })
  return response.data
}

export const getUiInfo = async (): Promise<UiInfo> => {
  const response = await axiosInstance.get('/display/info')
  return response.data as UiInfo
}

export const moderationService = {
  listPendingContent,
  moderateContent,
  getContentHistory,
  analyzeContent,
  getContentAnalysis,
  flagContent,
  getUiInfo,
}
