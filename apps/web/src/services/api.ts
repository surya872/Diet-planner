import axios from 'axios';
import { User, DietPlan, UserFormData } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5001/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add request interceptor for error handling
api.interceptors.request.use(
  (config) => {
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

// Authentication functions
export const register = (userData: UserFormData & { password: string }) => 
  api.post<{message: string, access_token: string, user: User}>('/register', userData);

export const login = (email: string, password: string) => 
  api.post<{message: string, access_token: string, user: User}>('/login', { email, password });

// User profile functions
export const getProfile = () => 
  api.get<User>('/profile');

export const updateProfile = (userData: Partial<UserFormData> & { password?: string }) => 
  api.put<{message: string, user: User}>('/profile', userData);

// Diet plan functions
export const generateDietPlan = () => 
  api.post<DietPlan>('/diet-plan');

export const getUserDietPlans = () => 
  api.get<DietPlan[]>('/diet-plans');

export const getDietPlan = (planId: number) => 
  api.get<DietPlan>(`/diet-plan/${planId}`);

// Utility functions
export const healthCheck = () => 
  api.get('/health');

// Auth utilities
export const setAuthToken = (token: string) => {
  localStorage.setItem('access_token', token);
};

export const removeAuthToken = () => {
  localStorage.removeItem('access_token');
};

export const getAuthToken = () => {
  return localStorage.getItem('access_token');
};

export { api };
