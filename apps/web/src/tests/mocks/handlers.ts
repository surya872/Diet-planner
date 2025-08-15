/**
 * MSW handlers for API mocking in tests
 * Ensures no real network calls are made during testing
 */

import { rest } from 'msw';

const API_BASE_URL = 'http://localhost:5001/api';

export const handlers = [
  // Health check endpoint
  rest.get(`${API_BASE_URL}/health`, (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        status: 'healthy',
        timestamp: new Date().toISOString(),
        uptime: 3600,
        checks: {
          database: { status: 'healthy' },
          external_services: { gemini_ai: { status: 'healthy' } }
        }
      })
    );
  }),

  // User registration
  rest.post(`${API_BASE_URL}/register`, (req, res, ctx) => {
    return res(
      ctx.status(201),
      ctx.json({
        message: 'User registered successfully',
        user: {
          id: 1,
          name: 'Test User',
          email: 'test@example.com',
          age: 25,
          gender: 'male',
          weight: 70
        }
      })
    );
  }),

  // User login
  rest.post(`${API_BASE_URL}/login`, (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        message: 'Login successful',
        access_token: 'mock-jwt-token',
        user: {
          id: 1,
          name: 'Test User',
          email: 'test@example.com',
          age: 25,
          gender: 'male',
          weight: 70
        }
      })
    );
  }),

  // Get user profile
  rest.get(`${API_BASE_URL}/profile`, (req, res, ctx) => {
    const authHeader = req.headers.get('Authorization');
    
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return res(
        ctx.status(401),
        ctx.json({
          error: 'Authorization token required'
        })
      );
    }

    return res(
      ctx.status(200),
      ctx.json({
        id: 1,
        name: 'Test User',
        email: 'test@example.com',
        age: 25,
        gender: 'male',
        weight: 70,
        height: 175,
        activity_level: 'moderate',
        diet_preference: 'vegetarian',
        health_goals: 'weight_loss'
      })
    );
  }),

  // Update user profile
  rest.put(`${API_BASE_URL}/profile`, (req, res, ctx) => {
    const authHeader = req.headers.get('Authorization');
    
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return res(
        ctx.status(401),
        ctx.json({
          error: 'Authorization token required'
        })
      );
    }

    return res(
      ctx.status(200),
      ctx.json({
        message: 'Profile updated successfully',
        user: {
          id: 1,
          name: 'Updated User',
          email: 'test@example.com',
          age: 26,
          gender: 'male',
          weight: 75
        }
      })
    );
  }),

  // Generate diet plan
  rest.post(`${API_BASE_URL}/diet-plan`, (req, res, ctx) => {
    const authHeader = req.headers.get('Authorization');
    
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return res(
        ctx.status(401),
        ctx.json({
          error: 'Authorization token required'
        })
      );
    }

    return res(
      ctx.status(201),
      ctx.json({
        id: 1,
        plan_name: 'Vegetarian Weight Loss Plan',
        start_date: '2024-01-15',
        end_date: '2024-01-21',
        total_calories: 1800,
        plan_data: {
          days: [
            {
              day: 1,
              date: '2024-01-15',
              meals: [
                {
                  type: 'breakfast',
                  name: 'Oatmeal with Berries',
                  calories: 350,
                  protein: 12,
                  carbs: 65,
                  fat: 8
                },
                {
                  type: 'lunch',
                  name: 'Quinoa Salad',
                  calories: 450,
                  protein: 18,
                  carbs: 70,
                  fat: 12
                },
                {
                  type: 'dinner',
                  name: 'Vegetable Stir Fry',
                  calories: 400,
                  protein: 15,
                  carbs: 55,
                  fat: 15
                }
              ],
              total_calories: 1200,
              total_protein: 45,
              total_carbs: 190,
              total_fat: 35
            }
          ],
          nutrition_summary: {
            daily_average_calories: 1800,
            daily_average_protein: 70,
            daily_average_carbs: 225,
            daily_average_fat: 60
          }
        }
      })
    );
  }),

  // Get user diet plans
  rest.get(`${API_BASE_URL}/diet-plans`, (req, res, ctx) => {
    const authHeader = req.headers.get('Authorization');
    
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return res(
        ctx.status(401),
        ctx.json({
          error: 'Authorization token required'
        })
      );
    }

    return res(
      ctx.status(200),
      ctx.json([
        {
          id: 1,
          plan_name: 'Vegetarian Weight Loss Plan',
          start_date: '2024-01-15',
          end_date: '2024-01-21',
          total_calories: 1800,
          created_at: '2024-01-15T10:00:00Z'
        }
      ])
    );
  }),

  // Rate limit errors
  rest.post(`${API_BASE_URL}/login-rate-limited`, (req, res, ctx) => {
    return res(
      ctx.status(429),
      ctx.json({
        error: 'Rate limit exceeded. Please try again later.',
        status: 429,
        timestamp: new Date().toISOString()
      })
    );
  }),

  rest.post(`${API_BASE_URL}/diet-plan-rate-limited`, (req, res, ctx) => {
    return res(
      ctx.status(429),
      ctx.json({
        error: 'Rate limit exceeded. Please try again later.',
        status: 429,
        timestamp: new Date().toISOString()
      })
    );
  }),

  // Error scenarios
  rest.post(`${API_BASE_URL}/server-error`, (req, res, ctx) => {
    return res(
      ctx.status(500),
      ctx.json({
        error: 'Internal server error',
        status: 500,
        timestamp: new Date().toISOString()
      })
    );
  }),

  rest.get(`${API_BASE_URL}/not-found`, (req, res, ctx) => {
    return res(
      ctx.status(404),
      ctx.json({
        error: 'Resource not found',
        status: 404,
        timestamp: new Date().toISOString()
      })
    );
  })
];

export { rest };
