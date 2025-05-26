import endpoints from './endpoints.ts'
import axiosInstance from './interceptor.ts'

const getCurrentVersion = async () => {
  const response = await axiosInstance.get(endpoints.misc.version)
  return response.data
}

export { getCurrentVersion }
