import axiosInstance from './interceptor.ts';
import endpoints from './endpoints.ts';


class RegisterUser {
    username: string;
    email: string;
    password: string;

    constructor(username: string, email: string, password: string) {
        this.username = username;
        this.email = email;
        this.password = password;
    }
}

class Credentials {
    username: string;
    password: string;

    constructor(username: string, password: string) {
        this.username = username;
        this.password = password;
    }
}



const registerUser = async (userData: RegisterUser) => {
  const response = await axiosInstance.post(endpoints.auth.register, userData);
  return response.data;
};

const loginUser = async (credentials: Credentials) => {
  const response = await axiosInstance.post(
    endpoints.auth.login, credentials,
    {
      headers: {
        'Content-Type': 'application/json',
      },
    }
);
  return response.data.token; // Assuming the response contains a token
};

const getCurrentUser = async () => {
  const response = await axiosInstance.get(endpoints.auth.me);
  return response.data;
};

export { registerUser, loginUser, getCurrentUser, Credentials };
