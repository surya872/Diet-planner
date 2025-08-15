import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import UserForm from '../../components/UserForm';

describe('UserForm Component', () => {
  const mockOnSubmit = jest.fn();
  const mockOnSwitchToLogin = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
    // Mock window.alert
    global.alert = jest.fn();
  });

  const defaultProps = {
    onSubmit: mockOnSubmit,
    onSwitchToLogin: mockOnSwitchToLogin,
    error: null,
    loading: false,
  };

  test('renders registration form with all required fields', () => {
    render(<UserForm {...defaultProps} />);

    expect(screen.getByText('Create Your Account')).toBeInTheDocument();
    expect(screen.getByLabelText('Full Name *')).toBeInTheDocument();
    expect(screen.getByLabelText('Email Address *')).toBeInTheDocument();
    expect(screen.getByLabelText('Password *')).toBeInTheDocument();
    expect(screen.getByLabelText('Confirm Password *')).toBeInTheDocument();
    expect(screen.getByLabelText('Age *')).toBeInTheDocument();
    expect(screen.getByLabelText('Gender *')).toBeInTheDocument();
    expect(screen.getByLabelText('Weight (kg) *')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Create My Account' })).toBeInTheDocument();
  });

  test('displays error message when provided', () => {
    const errorMessage = 'Email already exists';
    render(<UserForm {...defaultProps} error={errorMessage} />);

    expect(screen.getByText(errorMessage)).toBeInTheDocument();
  });

  test('shows loading state when loading is true', () => {
    render(<UserForm {...defaultProps} loading={true} />);

    expect(screen.getByText('Creating Account...')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: 'Creating Account...' })).toBeDisabled();
  });

  test('validates password confirmation match', async () => {

    render(<UserForm {...defaultProps} />);

    // Fill in all required fields
    await userEvent.type(screen.getByLabelText('Full Name *'), 'John Doe');
    await userEvent.type(screen.getByLabelText('Email Address *'), 'john@example.com');
    await userEvent.type(screen.getByLabelText('Password *'), 'password123');
    await userEvent.type(screen.getByLabelText('Confirm Password *'), 'differentpassword');
    
    const submitButton = screen.getByRole('button', { name: 'Create My Account' });
    await userEvent.click(submitButton);

    expect(global.alert).toHaveBeenCalledWith('Passwords do not match');
    expect(mockOnSubmit).not.toHaveBeenCalled();
  });

  test('validates minimum password length', async () => {

    render(<UserForm {...defaultProps} />);

    // Fill in all required fields with short password
    await userEvent.type(screen.getByLabelText('Full Name *'), 'John Doe');
    await userEvent.type(screen.getByLabelText('Email Address *'), 'john@example.com');
    await userEvent.type(screen.getByLabelText('Password *'), '123');
    await userEvent.type(screen.getByLabelText('Confirm Password *'), '123');
    
    const submitButton = screen.getByRole('button', { name: 'Create My Account' });
    await userEvent.click(submitButton);

    expect(global.alert).toHaveBeenCalledWith('Password must be at least 6 characters long');
    expect(mockOnSubmit).not.toHaveBeenCalled();
  });

  test('submits form with valid data', async () => {

    render(<UserForm {...defaultProps} />);

    // Fill in all required fields
    await userEvent.type(screen.getByLabelText('Full Name *'), 'John Doe');
    await userEvent.type(screen.getByLabelText('Email Address *'), 'john@example.com');
    await userEvent.type(screen.getByLabelText('Password *'), 'password123');
    await userEvent.type(screen.getByLabelText('Confirm Password *'), 'password123');
    await userEvent.type(screen.getByLabelText('Age *'), '30');
    await userEvent.selectOptions(screen.getByLabelText('Gender *'), 'male');
    await userEvent.type(screen.getByLabelText('Weight (kg) *'), '75');
    
    const submitButton = screen.getByRole('button', { name: 'Create My Account' });
    await userEvent.click(submitButton);

    expect(mockOnSubmit).toHaveBeenCalledWith({
      name: 'John Doe',
      email: 'john@example.com',
      password: 'password123',
      age: 30,
      gender: 'male',
      weight: 75,
      height: 170,
      activity_level: 'moderate',
      diet_preference: 'balanced',
      health_goals: ''
    });
  });

  test('toggles password visibility', async () => {

    render(<UserForm {...defaultProps} />);

    const passwordInput = screen.getByLabelText('Password *');
    const confirmPasswordInput = screen.getByLabelText('Confirm Password *');
    
    // Find the eye icons (there should be two)
    const eyeButtons = screen.getAllByRole('button', { name: '' });

    // Initially passwords should be hidden
    expect(passwordInput).toHaveAttribute('type', 'password');
    expect(confirmPasswordInput).toHaveAttribute('type', 'password');

    // Click first eye icon (password field)
    await userEvent.click(eyeButtons[0]);
    expect(passwordInput).toHaveAttribute('type', 'text');

    // Click second eye icon (confirm password field)
    await userEvent.click(eyeButtons[1]);
    expect(confirmPasswordInput).toHaveAttribute('type', 'text');
  });

  test('calls onSwitchToLogin when login link is clicked', async () => {

    render(<UserForm {...defaultProps} />);

    const loginLink = screen.getByText('Sign in here');
    await userEvent.click(loginLink);

    expect(mockOnSwitchToLogin).toHaveBeenCalled();
  });

  test('handles numeric input fields correctly', async () => {

    render(<UserForm {...defaultProps} />);

    const ageInput = screen.getByLabelText('Age *') as HTMLInputElement;
    const weightInput = screen.getByLabelText('Weight (kg) *') as HTMLInputElement;
    const heightInput = screen.getByLabelText('Height (cm)') as HTMLInputElement;

    await userEvent.type(ageInput, '25');
    await userEvent.type(weightInput, '70.5');
    await userEvent.type(heightInput, '175');

    expect(ageInput.value).toBe('25');
    expect(weightInput.value).toBe('70.5');
    expect(heightInput.value).toBe('175');
  });

  test('sets default values for optional fields', () => {
    render(<UserForm {...defaultProps} />);

    const activitySelect = screen.getByLabelText('Activity Level') as HTMLSelectElement;
    const dietSelect = screen.getByLabelText('Diet Preference') as HTMLSelectElement;
    const heightInput = screen.getByLabelText('Height (cm)') as HTMLInputElement;

    expect(activitySelect.value).toBe('moderate');
    expect(dietSelect.value).toBe('balanced');
    expect(heightInput.value).toBe('170');
  });

  test('prevents form submission when loading', async () => {

    render(<UserForm {...defaultProps} loading={true} />);

    const submitButton = screen.getByRole('button', { name: 'Creating Account...' });
    
    expect(submitButton).toBeDisabled();
    
    await userEvent.click(submitButton);
    expect(mockOnSubmit).not.toHaveBeenCalled();
  });
});
