"""
Unit tests for API endpoints.
"""
import json
from unittest.mock import MagicMock, patch

import pytest

from app import app


@pytest.mark.unit
@pytest.mark.api
class TestHealthEndpoint:
    """Test cases for health check endpoint."""

    def test_health_check(self, client):
        """Test health check endpoint returns correct response."""
        response = client.get("/api/health")

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["status"] == "healthy"
        assert "Diet Planner API is running" in data["message"]


@pytest.mark.unit
@pytest.mark.api
@pytest.mark.auth
class TestAuthenticationEndpoints:
    """Test cases for authentication endpoints."""

    def test_register_valid_user(self, client, db_session):
        """Test user registration with valid data."""
        user_data = {
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123",
            "age": 30,
            "gender": "male",
            "weight": 75,
            "height": 180,
            "activity_level": "moderate",
            "diet_preference": "balanced",
            "health_goals": "Weight loss",
        }

        response = client.post("/api/register", json=user_data)

        assert response.status_code == 201
        data = json.loads(response.data)
        assert "access_token" in data
        assert "user" in data
        assert data["user"]["email"] == "test@example.com"
        assert data["message"] == "User registered successfully"

    def test_register_invalid_data(self, client):
        """Test user registration with invalid data."""
        invalid_data = {
            "name": "",  # Empty name
            "email": "invalid-email",  # Invalid email
            "password": "123",  # Too short password
            "age": -1,  # Invalid age
            "gender": "invalid",  # Invalid gender
            "weight": 0,  # Invalid weight
        }

        response = client.post("/api/register", json=invalid_data)

        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data

    def test_register_duplicate_email(self, client, sample_user):
        """Test registration with duplicate email."""
        user_data = {
            "name": "Another User",
            "email": sample_user.email,  # Duplicate email
            "password": "password123",
            "age": 25,
            "gender": "female",
            "weight": 60,
        }

        response = client.post("/api/register", json=user_data)

        assert response.status_code == 409
        data = json.loads(response.data)
        assert "already exists" in data["error"]

    def test_login_valid_credentials(self, client, sample_user):
        """Test login with valid credentials."""
        login_data = {
            "email": sample_user.email,
            "password": "password123",  # Default password from factory
        }

        response = client.post("/api/login", json=login_data)

        assert response.status_code == 200
        data = json.loads(response.data)
        assert "access_token" in data
        assert "user" in data
        assert data["message"] == "Login successful"

    def test_login_invalid_credentials(self, client, sample_user):
        """Test login with invalid credentials."""
        login_data = {"email": sample_user.email, "password": "wrongpassword"}

        response = client.post("/api/login", json=login_data)

        assert response.status_code == 401
        data = json.loads(response.data)
        assert "Invalid email or password" in data["error"]

    def test_login_nonexistent_user(self, client):
        """Test login with non-existent user."""
        login_data = {"email": "nonexistent@example.com", "password": "password123"}

        response = client.post("/api/login", json=login_data)

        assert response.status_code == 401
        data = json.loads(response.data)
        assert "Invalid email or password" in data["error"]

    def test_login_missing_fields(self, client):
        """Test login with missing required fields."""
        # Missing password
        response = client.post("/api/login", json={"email": "test@example.com"})
        assert response.status_code == 400

        # Missing email
        response = client.post("/api/login", json={"password": "password123"})
        assert response.status_code == 400


@pytest.mark.unit
@pytest.mark.api
@pytest.mark.auth
class TestProfileEndpoints:
    """Test cases for profile management endpoints."""

    def test_get_profile_authenticated(self, client, auth_headers):
        """Test getting profile with valid authentication."""
        response = client.get("/api/profile", headers=auth_headers)

        assert response.status_code == 200
        data = json.loads(response.data)
        assert "email" in data
        assert "name" in data

    def test_get_profile_unauthenticated(self, client):
        """Test getting profile without authentication."""
        response = client.get("/api/profile")

        assert response.status_code == 401

    def test_update_profile_valid_data(self, client, auth_headers):
        """Test updating profile with valid data."""
        update_data = {"name": "Updated Name", "age": 35, "weight": 80}

        response = client.put("/api/profile", json=update_data, headers=auth_headers)


        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["message"] == "Profile updated successfully"
        assert data["user"]["name"] == "Updated Name"

    def test_update_profile_invalid_data(self, client, auth_headers):
        """Test updating profile with invalid data."""
        invalid_data = {"age": -1, "weight": 0}  # Invalid age  # Invalid weight

        response = client.put("/api/profile", json=invalid_data, headers=auth_headers)

        assert response.status_code == 400
        data = json.loads(response.data)
        assert "error" in data

    def test_update_profile_unauthenticated(self, client):
        """Test updating profile without authentication."""
        update_data = {"name": "Updated Name"}

        response = client.put("/api/profile", json=update_data)

        assert response.status_code == 401


@pytest.mark.unit
@pytest.mark.api
class TestDietPlanEndpoints:
    """Test cases for diet plan endpoints."""

    @patch("app.generate_diet_plan_with_gemini")
    def test_generate_diet_plan_authenticated(
        self, mock_gemini, client, auth_headers, mock_gemini_response
    ):
        """Test generating diet plan with valid authentication."""
        mock_gemini.return_value = mock_gemini_response

        response = client.post("/api/diet-plan", headers=auth_headers)

        assert response.status_code == 201
        data = json.loads(response.data)
        assert "plan_name" in data
        assert "total_calories" in data
        assert "plan_data" in data

    def test_generate_diet_plan_unauthenticated(self, client):
        """Test generating diet plan without authentication."""
        response = client.post("/api/diet-plan")

        assert response.status_code == 401

    @patch("app.generate_diet_plan_with_gemini")
    def test_generate_diet_plan_gemini_error(self, mock_gemini, client, auth_headers):
        """Test handling Gemini API errors."""
        mock_gemini.side_effect = Exception("Gemini API error")

        response = client.post("/api/diet-plan", headers=auth_headers)

        assert response.status_code == 500
        data = json.loads(response.data)
        assert "error" in data

    def test_get_user_diet_plans_authenticated(self, client, auth_headers, sample_diet_plan):
        """Test getting user's diet plans with authentication."""
        response = client.get("/api/diet-plans", headers=auth_headers)

        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)

    def test_get_user_diet_plans_unauthenticated(self, client):
        """Test getting diet plans without authentication."""
        response = client.get("/api/diet-plans")

        assert response.status_code == 401

    def test_get_specific_diet_plan_authenticated(self, client, auth_headers, sample_diet_plan):
        """Test getting specific diet plan with authentication."""
        response = client.get(f"/api/diet-plan/{sample_diet_plan.id}", headers=auth_headers)

        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["id"] == sample_diet_plan.id

    def test_get_specific_diet_plan_unauthenticated(self, client, sample_diet_plan):
        """Test getting specific diet plan without authentication."""
        response = client.get(f"/api/diet-plan/{sample_diet_plan.id}")

        assert response.status_code == 401

    def test_get_nonexistent_diet_plan(self, client, auth_headers):
        """Test getting non-existent diet plan."""
        response = client.get("/api/diet-plan/99999", headers=auth_headers)

        assert response.status_code == 404
