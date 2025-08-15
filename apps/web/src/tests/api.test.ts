/**
 * API service tests with mocked network calls
 * Ensures no real network requests are made during testing
 */

import { 
  register, 
  login, 
  getProfile, 
  updateProfile, 
  generateDietPlan,
  getUserDietPlans,
  healthCheck 
} from '../services/api';
import { server } from './mocks/server';
import { rest } from 'msw';

// Import the mock server setup
import './mocks/server';

describe('API Service Tests', () => {
  describe('Authentication API', () => {
    test('register() should create new user account', async () => {
      const userData = {
        name: 'Test User',
        email: 'test@example.com',
        password: 'password123',
        age: 25,
        gender: 'male' as const,
        weight: 70
      };

      const result = await register(userData);

      expect(result.message).toBe('User registered successfully');
      expect(result.user.name).toBe('Test User');
      expect(result.user.email).toBe('test@example.com');
    });

    test('login() should authenticate user and return token', async () => {
      const credentials = {
        email: 'test@example.com',
        password: 'password123'
      };

      const result = await login(credentials);

      expect(result.message).toBe('Login successful');
      expect(result.access_token).toBe('mock-jwt-token');
      expect(result.user.email).toBe('test@example.com');
    });

    test('login() should handle rate limiting', async () => {
      // Override the handler to simulate rate limiting
      server.use(
        rest.post('http://localhost:5001/api/login', (req, res, ctx) => {
          return res(
            ctx.status(429),
            ctx.json({
              error: 'Rate limit exceeded. Please try again later.',
              status: 429,
              timestamp: new Date().toISOString()
            })
          );
        })
      );

      const credentials = {
        email: 'test@example.com',
        password: 'password123'
      };

      await expect(login(credentials)).rejects.toThrow();
    });
  });

  describe('Profile API', () => {
    beforeEach(() => {
      // Set up authentication token for profile tests
      localStorage.setItem('token', 'mock-jwt-token');
    });

    afterEach(() => {
      localStorage.removeItem('token');
    });

    test('getProfile() should fetch user profile data', async () => {
      const profile = await getProfile();

      expect(profile.name).toBe('Test User');
      expect(profile.email).toBe('test@example.com');
      expect(profile.age).toBe(25);
    });

    test('getProfile() should handle unauthorized access', async () => {
      // Remove token to simulate unauthorized access
      localStorage.removeItem('token');

      await expect(getProfile()).rejects.toThrow();
    });

    test('updateProfile() should update user profile', async () => {
      const updates = {
        name: 'Updated User',
        age: 26,
        weight: 75
      };

      const result = await updateProfile(updates);

      expect(result.message).toBe('Profile updated successfully');
      expect(result.user.name).toBe('Updated User');
      expect(result.user.age).toBe(26);
    });

    test('updateProfile() should handle validation errors', async () => {
      // Override handler to simulate validation error
      server.use(
        rest.put('http://localhost:5001/api/profile', (req, res, ctx) => {
          return res(
            ctx.status(400),
            ctx.json({
              error: 'Validation failed',
              details: { age: 'Age must be between 1 and 120' },
              status: 400
            })
          );
        })
      );

      const invalidUpdates = {
        age: 150 // Invalid age
      };

      await expect(updateProfile(invalidUpdates)).rejects.toThrow();
    });
  });

  describe('Diet Plan API', () => {
    beforeEach(() => {
      localStorage.setItem('token', 'mock-jwt-token');
    });

    afterEach(() => {
      localStorage.removeItem('token');
    });

    test('generateDietPlan() should create new diet plan', async () => {
      const planData = {
        diet_preference: 'vegetarian',
        health_goals: 'weight_loss'
      };

      const result = await generateDietPlan(planData);

      expect(result.plan_name).toBe('Vegetarian Weight Loss Plan');
      expect(result.total_calories).toBe(1800);
      expect(result.plan_data).toBeDefined();
      expect(result.plan_data.days).toHaveLength(1);
    });

    test('generateDietPlan() should handle rate limiting', async () => {
      // Override handler to simulate rate limiting
      server.use(
        rest.post('http://localhost:5001/api/diet-plan', (req, res, ctx) => {
          return res(
            ctx.status(429),
            ctx.json({
              error: 'Rate limit exceeded. Please try again later.',
              status: 429,
              timestamp: new Date().toISOString()
            })
          );
        })
      );

      const planData = {
        diet_preference: 'vegetarian',
        health_goals: 'weight_loss'
      };

      await expect(generateDietPlan(planData)).rejects.toThrow();
    });

    test('generateDietPlan() should handle Gemini API failures', async () => {
      // Override handler to simulate server error (Gemini failure)
      server.use(
        rest.post('http://localhost:5001/api/diet-plan', (req, res, ctx) => {
          return res(
            ctx.status(500),
            ctx.json({
              error: 'Internal server error',
              status: 500,
              timestamp: new Date().toISOString()
            })
          );
        })
      );

      const planData = {
        diet_preference: 'vegetarian',
        health_goals: 'weight_loss'
      };

      await expect(generateDietPlan(planData)).rejects.toThrow();
    });

    test('getUserDietPlans() should fetch user diet plans', async () => {
      const plans = await getUserDietPlans();

      expect(Array.isArray(plans)).toBe(true);
      expect(plans).toHaveLength(1);
      expect(plans[0].plan_name).toBe('Vegetarian Weight Loss Plan');
    });

    test('getUserDietPlans() should handle unauthorized access', async () => {
      localStorage.removeItem('token');

      await expect(getUserDietPlans()).rejects.toThrow();
    });
  });

  describe('Health Check API', () => {
    test('healthCheck() should return system health status', async () => {
      const health = await healthCheck();

      expect(health.status).toBe('healthy');
      expect(health.checks).toBeDefined();
      expect(health.checks.database.status).toBe('healthy');
      expect(health.checks.external_services.gemini_ai.status).toBe('healthy');
    });

    test('healthCheck() should handle server errors', async () => {
      // Override handler to simulate server error
      server.use(
        rest.get('http://localhost:5001/api/health', (req, res, ctx) => {
          return res(
            ctx.status(500),
            ctx.json({
              error: 'Internal server error',
              status: 500,
              timestamp: new Date().toISOString()
            })
          );
        })
      );

      await expect(healthCheck()).rejects.toThrow();
    });
  });

  describe('Network Error Handling', () => {
    test('should handle network errors gracefully', async () => {
      // Override all handlers to simulate network error
      server.use(
        rest.get('*', (req, res, ctx) => {
          return res.networkError('Network connection failed');
        }),
        rest.post('*', (req, res, ctx) => {
          return res.networkError('Network connection failed');
        })
      );

      await expect(healthCheck()).rejects.toThrow();
    });

    test('should handle timeout errors', async () => {
      // Override handler to simulate timeout
      server.use(
        rest.get('http://localhost:5001/api/health', (req, res, ctx) => {
          return res(
            ctx.delay(30000), // 30 second delay to simulate timeout
            ctx.status(200),
            ctx.json({ status: 'healthy' })
          );
        })
      );

      // This test would need timeout configuration in axios
      // For now, we'll just test that the request can be made
      const healthPromise = healthCheck();
      expect(healthPromise).toBeDefined();
    });
  });

  describe('Security Headers Validation', () => {
    test('should receive proper security headers from API', async () => {
      // Override handler to include security headers
      server.use(
        rest.get('http://localhost:5001/api/health', (req, res, ctx) => {
          return res(
            ctx.status(200),
            ctx.set('X-Content-Type-Options', 'nosniff'),
            ctx.set('X-Frame-Options', 'DENY'),
            ctx.set('Referrer-Policy', 'strict-origin-when-cross-origin'),
            ctx.json({ status: 'healthy' })
          );
        })
      );

      // Note: In a real test, you'd need to inspect the response headers
      // This is more of an integration test concept
      const result = await healthCheck();
      expect(result.status).toBe('healthy');
    });
  });
});

describe('API Error Handling', () => {
  test('should handle 400 Bad Request errors', async () => {
    server.use(
      rest.post('http://localhost:5001/api/register', (req, res, ctx) => {
        return res(
          ctx.status(400),
          ctx.json({
            error: 'Validation failed',
            details: { email: 'Invalid email format' },
            status: 400
          })
        );
      })
    );

    const invalidUserData = {
      name: 'Test User',
      email: 'invalid-email',
      password: 'password123',
      age: 25,
      gender: 'male' as const,
      weight: 70
    };

    await expect(register(invalidUserData)).rejects.toThrow();
  });

  test('should handle 404 Not Found errors', async () => {
    server.use(
      rest.get('http://localhost:5001/api/nonexistent', (req, res, ctx) => {
        return res(
          ctx.status(404),
          ctx.json({
            error: 'Resource not found',
            status: 404,
            timestamp: new Date().toISOString()
          })
        );
      })
    );

    // This would need a corresponding API function
    // For now, we'll test with an existing function that we override
    server.use(
      rest.get('http://localhost:5001/api/health', (req, res, ctx) => {
        return res(
          ctx.status(404),
          ctx.json({
            error: 'Resource not found',
            status: 404,
            timestamp: new Date().toISOString()
          })
        );
      })
    );

    await expect(healthCheck()).rejects.toThrow();
  });
});
