import axios from 'axios';
import { ParentRegistrationData, RegistrationResponse } from '../types/auth';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

// Request interceptor to add auth token if available
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle common errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authApi = {
  registerParent: async (data: ParentRegistrationData): Promise<RegistrationResponse> => {
    const payload = {
      first_name: data.firstName,
      last_name: data.lastName,
      email: data.email,
      mobile_no: data.mobileNo,
      preferred_language: data.preferredLanguage,
      password: data.password,
      confirm_password: data.confirmPassword,
    };

    const response = await api.post('/auth/register/parent/', payload);
    return response.data;
  },

  verifyEmail: async (token: string) => {
    const response = await api.post('/auth/verify-email/', { token });
    return response.data;
  },

  resendVerification: async (email: string) => {
    const response = await api.post('/auth/resend-verification/', { email });
    return response.data;
  },

  login: async (email: string, password: string) => {
    const response = await api.post('/auth/login/', { email, password });
    return response.data;
  },

  healthCheck: async () => {
    const response = await api.get('/auth/health/');
    return response.data;
  },
};

export default api;