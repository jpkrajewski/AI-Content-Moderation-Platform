import axiosInstance from './interceptor.ts'
import endpoints from './endpoints.ts'

const getDashboardSummary = async () => {
  const response = await axiosInstance.get(endpoints.dashboard.summary)
  return response.data
}

const getUserActivityMetrics = async () => {
  const response = await axiosInstance.get(endpoints.dashboard.userActivity)
  return response.data
}

const getModerationKPI = async () => {
  const response = await axiosInstance.get(endpoints.dashboard.moderationStats)
  return response.data
}

export { getDashboardSummary, getUserActivityMetrics, getModerationKPI }
