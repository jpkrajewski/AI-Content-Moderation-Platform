import axiosInstance from './interceptor.ts';
import endpoints from './endpoints.ts';

interface RegisterUserData {
  username: string;
  email: string;
  password: string;
}

interface LoginCredentials {
  email: string;
  password: string;
}

interface AuthResponse {
  token: string;
}

interface UserData {
  id: string;
  username: string;
  email: string;
}

export const registerUser = async (userData: RegisterUserData): Promise<AuthResponse> => {
  const response = await axiosInstance.post(endpoints.auth.register, userData);
  return response.data;
};

export const loginUser = async (credentials: LoginCredentials): Promise<string> => {
  const response = await axiosInstance.post<AuthResponse>(
    endpoints.auth.login,
    credentials,
    {
      headers: {
        'Content-Type': 'application/json',
      },
    }
  );
  return response.data.token;
};

export const getCurrentUser = async (): Promise<UserData> => {
  const response = await axiosInstance.get<UserData>(endpoints.auth.me);
  return response.data;
};
