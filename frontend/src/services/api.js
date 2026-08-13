import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000/api',
  headers: { 'Content-Type': 'application/json' },
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('nepse_access_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

export const authGet = (url, config = {}) => config.method === 'delete' ? api.delete(url) : api.get(url, config)
export const authPost = (url, data) => api.post(url, data)
export const authDelete = (url) => api.delete(url)
export const dashboardApi = () => api.get('/analytics/dashboard/')
export const stocksApi = (search = '') => api.get('/stocks/', { params: search ? { search } : {} })
export const stockHistoryApi = (symbol, range = '1M') => api.get(`/stocks/${symbol}/history/`, { params: { range } })
export const technicalApi = (symbol) => api.get(`/stocks/${symbol}/technical-analysis/`)
export const brokerAnalysisApi = (symbol, period) => api.get(`/stocks/${symbol}/broker-analysis/`, { params: { period } })
export const brokersApi = () => api.get('/brokers/')
export const brokerActivityApi = (number) => api.get(`/brokers/${number}/activity/`)

export default api
