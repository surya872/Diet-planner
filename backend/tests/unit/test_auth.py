"""
Unit tests for authentication functionality.
"""
from unittest.mock import patch

import pytest

from app import validate_user_data


@pytest.mark.unit
@pytest.mark.auth
class TestUserValidation:
    """Test cases for user data validation."""

    def test_valid_user_data(self):
        """Test validation with valid user data."""
        valid_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123",
            "age": 30,
            "gender": "male",
            "weight": 75.5,
            "height": 180,
            "activity_level": "moderate",
            "diet_preference": "balanced",
            "health_goals": "Weight loss",
        }

        result = validate_user_data(valid_data)
        assert result is None  # No validation errors

    def test_missing_required_fields(self):
        """Test validation with missing required fields."""
        incomplete_data = {
            "name": "John Doe",
            # Missing email, password, age, gender, weight
        }

        result = validate_user_data(incomplete_data)
        assert result is not None
        assert "Missing required field" in result

    def test_empty_string_values(self):
        """Test validation with empty string values."""
        data_with_empty_strings = {
            "name": "",  # Empty name
            "email": "john@example.com",
            "password": "password123",
            "age": 30,
            "gender": "male",
            "weight": 75,
        }

        result = validate_user_data(data_with_empty_strings)
        assert result is not None
        assert "cannot be empty" in result

    def test_invalid_email_format(self):
        """Test validation with invalid email format."""
        data_with_invalid_email = {
            "name": "John Doe",
            "email": "invalid-email",  # Invalid format
            "password": "password123",
            "age": 30,
            "gender": "male",
            "weight": 75,
        }

        result = validate_user_data(data_with_invalid_email)
        assert result is not None
        assert "valid email address" in result

    def test_password_too_short(self):
        """Test validation with too short password."""
        data_with_short_password = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "123",  # Too short
            "age": 30,
            "gender": "male",
            "weight": 75,
        }

        result = validate_user_data(data_with_short_password)
        assert result is not None
        assert "at least 6 characters" in result

    def test_invalid_age_range(self):
        """Test validation with invalid age values."""
        # Test too young
        data_too_young = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123",
            "age": 0,  # Too young
            "gender": "male",
            "weight": 75,
        }

        result = validate_user_data(data_too_young)
        assert result is not None
        assert "at least 1" in result

        # Test too old
        data_too_old = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123",
            "age": 150,  # Too old
            "gender": "male",
            "weight": 75,
        }

        result = validate_user_data(data_too_old)
        assert result is not None
        assert "at most 120" in result

    def test_invalid_gender(self):
        """Test validation with invalid gender value."""
        data_with_invalid_gender = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123",
            "age": 30,
            "gender": "invalid",  # Invalid gender
            "weight": 75,
        }

        result = validate_user_data(data_with_invalid_gender)
        assert result is not None
        assert "must be one of" in result

    def test_invalid_weight_range(self):
        """Test validation with invalid weight values."""
        # Test too light
        data_too_light = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123",
            "age": 30,
            "gender": "male",
            "weight": 10,  # Too light
        }

        result = validate_user_data(data_too_light)
        assert result is not None
        assert "at least 20" in result

        # Test too heavy
        data_too_heavy = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123",
            "age": 30,
            "gender": "male",
            "weight": 400,  # Too heavy
        }

        result = validate_user_data(data_too_heavy)
        assert result is not None
        assert "at most 300" in result

    def test_optional_fields_validation(self):
        """Test validation of optional fields."""
        data_with_optional_fields = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123",
            "age": 30,
            "gender": "male",
            "weight": 75,
            "height": 50,  # Too short
            "activity_level": "invalid_level",  # Invalid activity level
            "diet_preference": "invalid_diet",  # Invalid diet preference
        }

        result = validate_user_data(data_with_optional_fields)
        assert result is not None
        # Should catch validation errors for optional fields too

    def test_update_validation_without_password(self):
        """Test validation for updates where password is not required."""
        update_data = {
            "name": "John Updated",
            "email": "john.updated@example.com",
            "age": 31,
            "gender": "male",
            "weight": 76
            # No password field
        }

        result = validate_user_data(update_data, is_update=True)
        assert result is None  # Should pass validation for updates


@pytest.mark.unit
@pytest.mark.auth
class TestPasswordHashing:
    """Test cases for password hashing functionality."""

    def test_password_hashing_consistency(self, sample_user):
        """Test that password hashing is consistent."""
        password = "testpassword123"

        # Set password
        sample_user.set_password(password)
        hash1 = sample_user.password_hash

        # Set same password again
        sample_user.set_password(password)
        hash2 = sample_user.password_hash

        # Hashes should be different (due to salt) but both should verify
        assert hash1 != hash2
        assert sample_user.check_password(password)

    def test_password_verification_case_sensitive(self, sample_user):
        """Test that password verification is case sensitive."""
        password = "TestPassword123"
        sample_user.set_password(password)

        assert sample_user.check_password("TestPassword123") is True
        assert sample_user.check_password("testpassword123") is False
        assert sample_user.check_password("TESTPASSWORD123") is False
