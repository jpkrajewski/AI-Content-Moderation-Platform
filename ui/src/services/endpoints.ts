const BASE_URL = 'http://localhost:8080/api/v1';

const endpoints = {
  // Authentication endpoints
  auth: {
    register: `${BASE_URL}/auth/register`, // POST: Register a new user
    login: `${BASE_URL}/auth/login`, // POST: Login and receive token
    me: `${BASE_URL}/auth/me`, // GET: Get current user
  },

  // User management endpoints
  users: {
    list: `${BASE_URL}/users`, // GET: Admin - list all users
    getUser: (userId: string) => `${BASE_URL}/users/${userId}`, // GET: Admin - view a specific user
    deleteUser: (userId: string) => `${BASE_URL}/users/${userId}`, // DELETE: Admin - delete a specific user
  },

  // Dashboard endpoints
  dashboard: {
    summary: `${BASE_URL}/dashboard/summary`, // GET: Admin - get statistics
    userActivity: `${BASE_URL}/dashboard/user-activity`, // GET: Admin - user activity metrics
    moderationStats: `${BASE_URL}/dashboard/moderation-stats`, // GET: Admin - moderation KPIs
  },

  // Moderation endpoints
  moderation: {
    listPending: `${BASE_URL}/moderation/pending`, // GET: Admin - list flagged content
    getContentAnalysis: (contentId: string) => `${BASE_URL}/moderation/${contentId}`, // GET: Admin - view analysis of single content
    approveContent: (contentId: string) => `${BASE_URL}/moderation/${contentId}/approve`, // POST: Admin - approve content
    rejectContent: (contentId: string) => `${BASE_URL}/moderation/${contentId}/reject`, // POST: Admin - reject content
    flagContent: (contentId: string) => `${BASE_URL}/moderation/${contentId}/flag`, // POST: Manually flag content
  },

  misc: {
    version: `${BASE_URL}/version`, // GET: Get the current version of the API
  }
};

export default endpoints;
