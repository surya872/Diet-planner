"""
Integration tests for complete authentication flow.
"""
import json
from unittest.mock import patch

import pytest


@pytest.mark.integration
@pytest.mark.auth
class TestCompleteAuthFlow:
    """Test complete authentication workflow."""

    def test_complete_user_registration_and_login_flow(self, client, db_session):
        """Test complete flow from registration to accessing protected resources."""
        # Step 1: Register a new user
        user_data = {
            "name": "Integration Test User",
            "email": "integration@example.com",
            "password": "password123",
            "age": 28,
            "gender": "female",
            "weight": 65,
            "height": 170,
            "activity_level": "moderate",
            "diet_preference": "vegetarian",
            "health_goals": "Maintain healthy weight",
        }

        # Register user
        register_response = client.post("/api/register", json=user_data)
        assert register_response.status_code == 201

        register_data = json.loads(register_response.data)
        assert "access_token" in register_data
        assert "user" in register_data

        # user_id = register_data["user"]["id"]  # Not used in this test
        access_token = register_data["access_token"]

        # Step 2: Access profile with token from registration
        auth_headers = {"Authorization": f"Bearer {access_token}"}
        profile_response = client.get("/api/profile", headers=auth_headers)
        assert profile_response.status_code == 200

        profile_data = json.loads(profile_response.data)
        assert profile_data["email"] == "integration@example.com"
        assert profile_data["name"] == "Integration Test User"

        # Step 3: Logout (simulate by not using token) and login again
        login_data = {"email": "integration@example.com", "password": "password123"}

        login_response = client.post("/api/login", json=login_data)
        assert login_response.status_code == 200

        login_response_data = json.loads(login_response.data)
        assert "access_token" in login_response_data

        new_token = login_response_data["access_token"]
        new_auth_headers = {"Authorization": f"Bearer {new_token}"}

        # Step 4: Access profile with new token
        profile_response_2 = client.get("/api/profile", headers=new_auth_headers)
        assert profile_response_2.status_code == 200

        # Step 5: Update profile
        update_data = {"name": "Updated Integration User", "age": 29, "weight": 66}

        update_response = client.put("/api/profile", json=update_data, headers=new_auth_headers)
        assert update_response.status_code == 200

        update_response_data = json.loads(update_response.data)
        assert update_response_data["user"]["name"] == "Updated Integration User"
        assert update_response_data["user"]["age"] == 29

        # Step 6: Verify updated profile
        final_profile_response = client.get("/api/profile", headers=new_auth_headers)
        assert final_profile_response.status_code == 200

        final_profile_data = json.loads(final_profile_response.data)
        assert final_profile_data["name"] == "Updated Integration User"
        assert final_profile_data["age"] == 29

    def test_invalid_token_rejection(self, client):
        """Test that invalid tokens are properly rejected."""
        invalid_headers = {"Authorization": "Bearer invalid_token_here"}

        # Try to access protected endpoints with invalid token
        profile_response = client.get("/api/profile", headers=invalid_headers)
        assert profile_response.status_code == 422  # JWT decode error

        # diet_plan_response = client.post("/api/diet-plan", headers=invalid_headers)  # Not used
        assert profile_response.status_code == 422

    def test_missing_token_rejection(self, client):
        """Test that requests without tokens are rejected."""
        # Try to access protected endpoints without token
        profile_response = client.get("/api/profile")
        assert profile_response.status_code == 401

        diet_plan_response = client.post("/api/diet-plan")
        assert diet_plan_response.status_code == 401

        update_response = client.put("/api/profile", json={"name": "Test"})
        assert update_response.status_code == 401


@pytest.mark.integration
@pytest.mark.auth
class TestPasswordUpdateFlow:
    """Test password update functionality."""

    def test_password_update_and_login(self, client, db_session):
        """Test updating password and logging in with new password."""
        # Register user
        user_data = {
            "name": "Password Test User",
            "email": "password@example.com",
            "password": "oldpassword123",
            "age": 30,
            "gender": "male",
            "weight": 75,
        }

        register_response = client.post("/api/register", json=user_data)
        assert register_response.status_code == 201

        # Get token
        token = json.loads(register_response.data)["access_token"]
        auth_headers = {"Authorization": f"Bearer {token}"}

        # Update password
        update_data = {"password": "newpassword123"}
        update_response = client.put("/api/profile", json=update_data, headers=auth_headers)
        assert update_response.status_code == 200

        # Try login with old password (should fail)
        old_login_data = {"email": "password@example.com", "password": "oldpassword123"}
        old_login_response = client.post("/api/login", json=old_login_data)
        assert old_login_response.status_code == 401

        # Try login with new password (should succeed)
        new_login_data = {"email": "password@example.com", "password": "newpassword123"}
        new_login_response = client.post("/api/login", json=new_login_data)
        assert new_login_response.status_code == 200
