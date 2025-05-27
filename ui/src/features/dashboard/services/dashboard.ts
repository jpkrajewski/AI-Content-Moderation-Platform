import axiosInstance from '@/api/interceptors/interceptor'
import type { DashboardData } from '../types/dashboard'

export const getDashboardSummary = async (): Promise<DashboardData> => {
  const response = await axiosInstance.get('/dashboard/summary')
  return response.data
}

export const getModerationStats = async () => {
  const response = await axiosInstance.get('/dashboard/moderation-stats')
  return response.data
}

export const getActivityMetrics = async () => {
  const response = await axiosInstance.get('/dashboard/activity-metrics')
  return response.data
}

export const getKPI = async () => {
  const response = await axiosInstance.get('/dashboard/kpi')
  return response.data
}

export const dashboardService = {
  getDashboardSummary,
  getModerationStats,
  getActivityMetrics,
  getKPI,
}
