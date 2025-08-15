/**
 * MSW server setup for testing
 * This sets up the mock service worker for intercepting API calls in tests
 */

import { setupServer } from 'msw/node';
import { handlers } from './handlers';

// Setup the mock server with our handlers
export const server = setupServer(...handlers);

// Enable API mocking before tests run
beforeAll(() => {
  server.listen({ onUnhandledRequest: 'error' });
});

// Reset handlers after each test to ensure test isolation
afterEach(() => {
  server.resetHandlers();
});

// Clean up after tests are finished
afterAll(() => {
  server.close();
});
