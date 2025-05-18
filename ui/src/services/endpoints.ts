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
};

export default endpoints;
