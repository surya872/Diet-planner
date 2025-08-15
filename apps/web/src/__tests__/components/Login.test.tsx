import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import Login from '../../components/Login';

describe('Login Component', () => {
  const mockOnSubmit = jest.fn();
  const mockOnSwitchToRegister = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  const defaultProps = {
    onSubmit: mockOnSubmit,
    onSwitchToRegister: mockOnSwitchToRegister,
    error: null,
    loading: false,
  };

  test('renders login form with all required fields', () => {
    render(<Login {...defaultProps} />);

    expect(screen.getByText('Welcome Back')).toBeInTheDocument();
    expect(screen.getByText('Sign in to your diet planner account')).toBeInTheDocument();
    expect(screen.getByLabelText('Email Address')).toBeInTheDocument();
    expect(screen.getByLabelText('Password')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Sign In' })).toBeInTheDocument();
  });

  test('displays error message when provided', () => {
    const errorMessage = 'Invalid email or password';
    render(<Login {...defaultProps} error={errorMessage} />);

    expect(screen.getByText(errorMessage)).toBeInTheDocument();
    expect(screen.getByText(errorMessage)).toHaveClass('text-red-600');
  });

  test('shows loading state when loading is true', () => {
    render(<Login {...defaultProps} loading={true} />);

    expect(screen.getByText('Signing in...')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Signing in...' })).toBeDisabled();
  });

  test('calls onSubmit with email and password when form is submitted', async () => {
    render(<Login {...defaultProps} />);

    const emailInput = screen.getByLabelText('Email Address');
    const passwordInput = screen.getByLabelText('Password');
    const submitButton = screen.getByRole('button', { name: 'Sign In' });

    await userEvent.type(emailInput, 'test@example.com');
    await userEvent.type(passwordInput, 'password123');
    await userEvent.click(submitButton);

    expect(mockOnSubmit).toHaveBeenCalledWith('test@example.com', 'password123');
  });

  test('toggles password visibility when eye icon is clicked', async () => {

    render(<Login {...defaultProps} />);

    const passwordInput = screen.getByLabelText('Password');
    const toggleButton = screen.getByRole('button', { name: '' }); // Eye icon button

    // Initially password should be hidden
    expect(passwordInput).toHaveAttribute('type', 'password');

    // Click to show password
    await userEvent.click(toggleButton);
    expect(passwordInput).toHaveAttribute('type', 'text');

    // Click to hide password again
    await userEvent.click(toggleButton);
    expect(passwordInput).toHaveAttribute('type', 'password');
  });

  test('calls onSwitchToRegister when register link is clicked', async () => {

    render(<Login {...defaultProps} />);

    const registerLink = screen.getByText('Register here');
    await userEvent.click(registerLink);

    expect(mockOnSwitchToRegister).toHaveBeenCalled();
  });

  test('form validation requires email and password', async () => {

    render(<Login {...defaultProps} />);

    const submitButton = screen.getByRole('button', { name: 'Sign In' });
    
    // Try to submit without filling fields
    await userEvent.click(submitButton);

    // Form should not be submitted
    expect(mockOnSubmit).not.toHaveBeenCalled();
  });

  test('maintains form state during typing', async () => {

    render(<Login {...defaultProps} />);

    const emailInput = screen.getByLabelText('Email Address') as HTMLInputElement;
    const passwordInput = screen.getByLabelText('Password') as HTMLInputElement;

    await userEvent.type(emailInput, 'test@example.com');
    await userEvent.type(passwordInput, 'mypassword');

    expect(emailInput.value).toBe('test@example.com');
    expect(passwordInput.value).toBe('mypassword');
  });

  test('prevents form submission when loading', async () => {

    render(<Login {...defaultProps} loading={true} />);

    const emailInput = screen.getByLabelText('Email Address');
    const passwordInput = screen.getByLabelText('Password');
    const submitButton = screen.getByRole('button', { name: 'Signing in...' });

    await userEvent.type(emailInput, 'test@example.com');
    await userEvent.type(passwordInput, 'password123');
    
    // Button should be disabled
    expect(submitButton).toBeDisabled();
    
    // Try to click anyway
    await userEvent.click(submitButton);
    
    // Should not call onSubmit
    expect(mockOnSubmit).not.toHaveBeenCalled();
  });
});
