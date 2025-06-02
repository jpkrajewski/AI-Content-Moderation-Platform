export const API_BASE_URL = 'http://localhost:8080/api/v1'

export const endpoints = {
  auth: {
    login: '/auth/login',
    register: '/auth/register',
    logout: '/auth/logout',
    me: '/auth/me',
  },
  moderation: {
    pending: '/moderation/pending',
    history: '/moderation/history',
    submitContent: '/content',
    approve: (id: string) => `/moderation/${id}/approve`,
    reject: (id: string) => `/moderation/${id}/reject`,
    getApiKeys: '/clients/apikeys',
    createApiKey: '/clients/apikeys',
    deactivateApiKey: (id: string) => `/clients/apikeys/${id}`,
    reactivateApiKey: (id: string) => `/clients/apikeys/${id}/reactivate`,
    deleteApiKey: (id: string) => `/clients/apikeys/${id}`,
  },
  dashboard: {
    summary: '/dashboard/summary',
    stats: '/dashboard/stats',
  },
  content: {
    list: '/content',
    create: '/content',
    update: (id: string) => `/content/${id}`,
    delete: (id: string) => `/content/${id}`,
  },
  version: '/version',
}
