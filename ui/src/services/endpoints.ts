const BASE_URL = 'http://localhost:8080/api/v1'

const endpoints = {
  auth: {
    register: `${BASE_URL}/auth/register`,
    login: `${BASE_URL}/auth/login`,
    me: `${BASE_URL}/auth/me`,
  },

  users: {
    list: `${BASE_URL}/users`,
    getUser: (userId: string) => `${BASE_URL}/users/${userId}`,
    deleteUser: (userId: string) => `${BASE_URL}/users/${userId}`,
  },

  dashboard: {
    summary: `${BASE_URL}/dashboard/summary`,
    userActivity: `${BASE_URL}/dashboard/user-activity`,
    moderationStats: `${BASE_URL}/dashboard/moderation-stats`,
  },

  moderation: {
    listPending: `${BASE_URL}/moderation/pending`,
    getContentAnalysis: (contentId: string) => `${BASE_URL}/moderation/${contentId}`,
    approveContent: (contentId: string) => `${BASE_URL}/moderation/${contentId}/approve`,
    rejectContent: (contentId: string) => `${BASE_URL}/moderation/${contentId}/reject`,
    flagContent: (contentId: string) => `${BASE_URL}/moderation/${contentId}/flag`,
    submitContent: `${BASE_URL}/content`,
  },

  misc: {
    version: `${BASE_URL}/version`,
  },
}

export default endpoints
