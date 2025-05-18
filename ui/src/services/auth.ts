import axios from 'axios';
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
    email: string;
    password: string;

    constructor(email: string, password: string) {
        this.email = email;
        this.password = password;
    }
}



const registerUser = async (userData: RegisterUser) => {
  const response = await axios.post(endpoints.auth.register, userData);
  return response.data;
};

const loginUser = async (credentials: Credentials) => {
  const response = await axios.post(
    endpoints.auth.login, credentials,
    {
      headers: {
        'Content-Type': 'application/json',
      },
    }
);
  return response.data.token; // Assuming the response contains a token
};

const getCurrentUser = async (token: string) => {
  const response = await axios.get(endpoints.auth.me, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};

export { registerUser, loginUser, getCurrentUser, Credentials };
