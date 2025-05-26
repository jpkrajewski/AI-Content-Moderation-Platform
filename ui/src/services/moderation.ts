import axiosInstance from './interceptor.ts'
import endpoints from './endpoints.ts'

const listPendingContent = async () => {
  const response = await axiosInstance.get(endpoints.moderation.listPending)
  return response.data
}

const getContentAnalysis = async (contentId: string) => {
  const response = await axiosInstance.get(endpoints.moderation.getContentAnalysis(contentId))
  return response.data
}

const approveContent = async (contentId: string) => {
  const response = await axiosInstance.post(endpoints.moderation.approveContent(contentId))
  return response.data
}

const rejectContent = async (contentId: string) => {
  const response = await axiosInstance.post(endpoints.moderation.rejectContent(contentId))
  return response.data
}

const flagContent = async (contentId: string) => {
  const response = await axiosInstance.post(endpoints.moderation.flagContent(contentId))
  return response.data
}

export { listPendingContent, getContentAnalysis, approveContent, rejectContent, flagContent }
