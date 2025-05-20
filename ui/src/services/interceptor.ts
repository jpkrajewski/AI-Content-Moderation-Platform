import axios from 'axios';
import { useJwtStore } from '@/stores/jwt.ts';

const axiosInstance = axios.create({
  baseURL: 'http://localhost:8080/api/v1',
});

axiosInstance.interceptors.request.use(
  (config) => {
    const jwtStore = useJwtStore();
    const token = jwtStore.jwt;
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default axiosInstance;
