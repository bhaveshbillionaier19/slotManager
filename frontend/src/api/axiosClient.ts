import axios from 'axios'
import { getToken } from '@/utils/auth'

export const axiosClient = axios.create({
  baseURL: 'http://localhost:8000',
})

axiosClient.interceptors.request.use((config) => {
  const token = getToken()
  if (token) {
    config.headers = config.headers ?? {}
    config.headers['Authorization'] = `Bearer ${token}`
  }
  return config
})

export default axiosClient


