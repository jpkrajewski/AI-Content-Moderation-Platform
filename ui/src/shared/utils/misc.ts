import axiosInstance from '@/api/interceptors/interceptor'

export const getCurrentVersion = async () => {
  const response = await axiosInstance.get('/version')
  return response.data
}
