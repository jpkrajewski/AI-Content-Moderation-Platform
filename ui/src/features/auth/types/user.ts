export interface User {
  uid: string
  username: string
  email: string
  scope: UserRole
}

export type UserRole = 'admin' | 'moderator' | 'user'

export interface UserState {
  currentUser: User | null
  isAuthenticated: boolean
  loading: boolean
  error: string | null
}

export interface LoginCredentials {
  email: string
  password: string
}

export interface RegisterData extends LoginCredentials {
  name: string
}
