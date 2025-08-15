import axios from 'axios';
import { 
  register, 
  login, 
  getProfile, 
  updateProfile, 
  generateDietPlan,
  setAuthToken,
  removeAuthToken,
  getAuthToken 
} from '../../services/api';

// Mock axios
jest.mock('axios');
const mockedAxios = axios as jest.Mocked<typeof axios>;

// Mock axios create
const mockAxiosInstance = {
  get: jest.fn(),
  post: jest.fn(),
  put: jest.fn(),
  delete: jest.fn(),
  interceptors: {
    request: {
      use: jest.fn(),
    },
    response: {
      use: jest.fn(),
    },
  },
};

mockedAxios.create.mockReturnValue(mockAxiosInstance as any);

describe('API Service', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    localStorage.clear();
  });

  describe('Authentication API calls', () => {
    test('register makes correct API call', async () => {
      const userData = {
        name: 'John Doe',
        email: 'john@example.com',
        password: 'password123',
        age: 30,
        gender: 'male',
        weight: 75,
      };

      const mockResponse = {
        data: {
          message: 'User registered successfully',
          access_token: 'fake-token',
          user: { id: 1, ...userData }
        }
      };

      mockAxiosInstance.post.mockResolvedValue(mockResponse);

      const result = await register(userData);

      expect(mockAxiosInstance.post).toHaveBeenCalledWith('/register', userData);
      expect(result).toBe(mockResponse);
    });

    test('login makes correct API call', async () => {
      const email = 'john@example.com';
      const password = 'password123';

      const mockResponse = {
        data: {
          message: 'Login successful',
          access_token: 'fake-token',
          user: { id: 1, email, name: 'John Doe' }
        }
      };

      mockAxiosInstance.post.mockResolvedValue(mockResponse);

      const result = await login(email, password);

      expect(mockAxiosInstance.post).toHaveBeenCalledWith('/login', { email, password });
      expect(result).toBe(mockResponse);
    });

    test('getProfile makes correct API call', async () => {
      const mockResponse = {
        data: {
          id: 1,
          name: 'John Doe',
          email: 'john@example.com',
          age: 30
        }
      };

      mockAxiosInstance.get.mockResolvedValue(mockResponse);

      const result = await getProfile();

      expect(mockAxiosInstance.get).toHaveBeenCalledWith('/profile');
      expect(result).toBe(mockResponse);
    });

    test('updateProfile makes correct API call', async () => {
      const updateData = {
        name: 'John Updated',
        age: 31
      };

      const mockResponse = {
        data: {
          message: 'Profile updated successfully',
          user: { id: 1, ...updateData }
        }
      };

      mockAxiosInstance.put.mockResolvedValue(mockResponse);

      const result = await updateProfile(updateData);

      expect(mockAxiosInstance.put).toHaveBeenCalledWith('/profile', updateData);
      expect(result).toBe(mockResponse);
    });
  });

  describe('Diet Plan API calls', () => {
    test('generateDietPlan makes correct API call', async () => {
      const mockResponse = {
        data: {
          id: 1,
          plan_name: 'Test Diet Plan',
          total_calories: 2000,
          plan_data: { daily_plans: [] }
        }
      };

      mockAxiosInstance.post.mockResolvedValue(mockResponse);

      const result = await generateDietPlan();

      expect(mockAxiosInstance.post).toHaveBeenCalledWith('/diet-plan');
      expect(result).toBe(mockResponse);
    });
  });

  describe('Token management', () => {
    test('setAuthToken stores token in localStorage', () => {
      const token = 'test-token';
      setAuthToken(token);

      expect(localStorage.setItem).toHaveBeenCalledWith('access_token', token);
    });

    test('removeAuthToken removes token from localStorage', () => {
      removeAuthToken();

      expect(localStorage.removeItem).toHaveBeenCalledWith('access_token');
    });

    test('getAuthToken retrieves token from localStorage', () => {
      const token = 'test-token';
      (localStorage.getItem as jest.Mock).mockReturnValue(token);

      const result = getAuthToken();

      expect(localStorage.getItem).toHaveBeenCalledWith('access_token');
      expect(result).toBe(token);
    });

    test('getAuthToken returns null when no token exists', () => {
      (localStorage.getItem as jest.Mock).mockReturnValue(null);

      const result = getAuthToken();

      expect(result).toBeNull();
    });
  });

  describe('Error handling', () => {
    test('handles API errors correctly', async () => {
      const errorResponse = {
        response: {
          data: { error: 'Invalid credentials' },
          status: 401
        }
      };

      mockAxiosInstance.post.mockRejectedValue(errorResponse);

      await expect(login('wrong@email.com', 'wrongpassword')).rejects.toEqual(errorResponse);
    });

    test('handles network errors correctly', async () => {
      const networkError = new Error('Network Error');
      mockAxiosInstance.get.mockRejectedValue(networkError);

      await expect(getProfile()).rejects.toThrow('Network Error');
    });
  });

  describe('Request interceptors', () => {
    test('adds authorization header when token exists', () => {
      const token = 'test-token';
      (localStorage.getItem as jest.Mock).mockReturnValue(token);

      // Simulate the request interceptor
      const config = { headers: {} };
      const interceptorCallback = mockAxiosInstance.interceptors.request.use.mock.calls[0][0];
      
      const result = interceptorCallback(config);

      expect(result.headers.Authorization).toBe(`Bearer ${token}`);
    });

    test('does not add authorization header when no token exists', () => {
      (localStorage.getItem as jest.Mock).mockReturnValue(null);

      // Simulate the request interceptor
      const config = { headers: {} };
      const interceptorCallback = mockAxiosInstance.interceptors.request.use.mock.calls[0][0];
      
      const result = interceptorCallback(config);

      expect(result.headers.Authorization).toBeUndefined();
    });
  });
});
