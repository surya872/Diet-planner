-- Migration to add password authentication
-- Run this script to update existing database schema

-- Add password_hash column to users table
ALTER TABLE users ADD COLUMN IF NOT EXISTS password_hash VARCHAR(255);

-- For existing users without passwords, you can either:
-- 1. Set a default password (not recommended for production)
-- 2. Require users to reset their passwords

-- Example: Set a default password "password123" (hashed) for existing users
-- This is just for testing - in production, implement proper password reset
UPDATE users 
SET password_hash = '$2b$12$LQv3c1yqBwEHxkGatEuueONTpm7dEOVUzlKjEYJLy8.6fFtJL3F8u' 
WHERE password_hash IS NULL OR password_hash = '';

-- Create index on email for faster lookups during login
CREATE INDEX IF NOT EXISTS idx_users_email_login ON users(email) WHERE password_hash IS NOT NULL;

-- Verify the migration
SELECT 
    column_name, 
    data_type, 
    is_nullable 
FROM information_schema.columns 
WHERE table_name = 'users' 
ORDER BY ordinal_position;
