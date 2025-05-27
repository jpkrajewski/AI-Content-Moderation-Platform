import axiosInstance from '@/api/interceptors/interceptor'
import type { ContentItem } from '../types/content'

export const listPendingContent = async (): Promise<ContentItem[]> => {
  const response = await axiosInstance.get('/moderation/pending')
  return response.data
}

export const moderateContent = async (
  contentId: string,
  decision: 'approve' | 'reject',
  reason?: string,
) => {
  const response = await axiosInstance.post(`/moderation/${contentId}`, {
    decision,
    reason,
  })
  return response.data
}

export const getContentHistory = async (): Promise<ContentItem[]> => {
  const response = await axiosInstance.get('/moderation/history')
  return response.data
}

export const analyzeContent = async (contentId: string) => {
  const response = await axiosInstance.post(`/moderation/${contentId}/analyze`)
  return response.data
}

export const getContentAnalysis = async (contentId: string): Promise<ContentItem> => {
  const response = await axiosInstance.get(`/moderation/${contentId}/analysis`)
  return response.data
}

export const flagContent = async (contentId: string, reason?: string) => {
  const response = await axiosInstance.post(`/moderation/${contentId}/flag`, { reason })
  return response.data
}

export const moderationService = {
  listPendingContent,
  moderateContent,
  getContentHistory,
  analyzeContent,
  getContentAnalysis,
  flagContent,
}
