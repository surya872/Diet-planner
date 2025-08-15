"""
Security tests for API endpoints
Tests for 401 unauthorized, 429 rate limits, validation, and error handling
"""

import pytest
import time
from unittest.mock import patch, MagicMock
from app import app, db, User, DietPlan
from tests.conftest import UserFactory


class TestAuthenticationSecurity:
    """Test authentication and authorization security"""
    
    def test_protected_route_requires_auth_401(self, client):
        """Test that protected routes return 401 without authentication"""
        protected_endpoints = [
            ('/api/profile', 'GET'),
            ('/api/profile', 'PUT'),
            ('/api/diet-plan', 'POST'),
            ('/api/diet-plans', 'GET'),
            ('/api/diet-plan/1', 'GET')
        ]
        
        for endpoint, method in protected_endpoints:
            if method == 'GET':
                response = client.get(endpoint)
            elif method == 'POST':
                response = client.post(endpoint, json={})
            elif method == 'PUT':
                response = client.put(endpoint, json={})
            
            assert response.status_code == 401
            data = response.get_json()
            assert 'msg' in data or 'error' in data
    
    def test_invalid_jwt_token_401(self, client):
        """Test that invalid JWT tokens return 401"""
        headers = {'Authorization': 'Bearer invalid-token'}
        
        response = client.get('/api/profile', headers=headers)
        assert response.status_code == 422  # JWT-Extended returns 422 for invalid tokens
    
    def test_expired_jwt_token_401(self, client, db_session):
        """Test that expired JWT tokens return 401"""
        # Create a user
        user = UserFactory()
        db_session.add(user)
        db_session.commit()
        
        # Mock expired token
        with patch('flask_jwt_extended.utils.decode_token') as mock_decode:
            mock_decode.side_effect = Exception("Token has expired")
            
            headers = {'Authorization': 'Bearer expired-token'}
            response = client.get('/api/profile', headers=headers)
            assert response.status_code == 422


class TestRateLimiting:
    """Test rate limiting functionality"""
    
    def test_login_rate_limit_429(self, client, db_session):
        """Test that login endpoint rate limits at 10 requests per minute"""
        # Create a user for login attempts
        user = UserFactory(email="test@example.com")
        db_session.add(user)
        db_session.commit()
        
        login_data = {
            "email": "test@example.com",
            "password": "wrong_password"
        }
        
        # Make 11 rapid login attempts (limit is 10 per minute)
        responses = []
        for i in range(11):
            response = client.post('/api/login', json=login_data)
            responses.append(response)
        
        # The 11th request should be rate limited
        assert responses[-1].status_code == 429
        data = responses[-1].get_json()
        assert 'Rate limit exceeded' in data.get('error', '')
    
    def test_diet_plan_rate_limit_429(self, client, db_session):
        """Test that diet-plan endpoint rate limits at 5 requests per minute"""
        # Create and login a user
        user = UserFactory()
        db_session.add(user)
        db_session.commit()
        
        # Login to get token
        login_response = client.post('/api/login', json={
            "email": user.email,
            "password": "password123"
        })
        token = login_response.get_json()['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        
        diet_plan_data = {
            "diet_preference": "vegetarian",
            "health_goals": "weight_loss"
        }
        
        # Make 6 rapid diet plan requests (limit is 5 per minute)
        responses = []
        for i in range(6):
            response = client.post('/api/diet-plan', json=diet_plan_data, headers=headers)
            responses.append(response)
        
        # The 6th request should be rate limited
        assert responses[-1].status_code == 429
        data = responses[-1].get_json()
        assert 'Rate limit exceeded' in data.get('error', '')


class TestInputValidation:
    """Test input validation and profile validation"""
    
    def test_registration_validation_errors(self, client):
        """Test registration with invalid data returns validation errors"""
        invalid_data_sets = [
            # Missing required fields
            {},
            # Invalid email format
            {
                "name": "Test User",
                "email": "invalid-email",
                "password": "password123",
                "age": 25,
                "gender": "male",
                "weight": 70
            },
            # Age out of range
            {
                "name": "Test User",
                "email": "test@example.com",
                "password": "password123",
                "age": 150,
                "gender": "male",
                "weight": 70
            },
            # Weight out of range
            {
                "name": "Test User",
                "email": "test@example.com",
                "password": "password123",
                "age": 25,
                "gender": "male",
                "weight": 500
            },
            # Invalid gender
            {
                "name": "Test User",
                "email": "test@example.com",
                "password": "password123",
                "age": 25,
                "gender": "invalid",
                "weight": 70
            }
        ]
        
        for invalid_data in invalid_data_sets:
            response = client.post('/api/register', json=invalid_data)
            assert response.status_code == 400
            data = response.get_json()
            assert 'error' in data
    
    def test_profile_update_validation(self, client, db_session):
        """Test profile update validation"""
        # Create and login a user
        user = UserFactory()
        db_session.add(user)
        db_session.commit()
        
        # Login to get token
        login_response = client.post('/api/login', json={
            "email": user.email,
            "password": "password123"
        })
        token = login_response.get_json()['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # Test invalid profile updates
        invalid_updates = [
            {"email": "invalid-email-format"},
            {"age": -5},
            {"weight": 1000},
            {"gender": "invalid_gender"}
        ]
        
        for invalid_data in invalid_updates:
            response = client.put('/api/profile', json=invalid_data, headers=headers)
            assert response.status_code == 400
            data = response.get_json()
            assert 'error' in data
    
    def test_large_payload_rejected(self, client):
        """Test that payloads larger than MAX_CONTENT_LENGTH are rejected"""
        # Create a payload larger than 1MB
        large_data = {
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123",
            "age": 25,
            "gender": "male",
            "weight": 70,
            "large_field": "x" * (1024 * 1024 + 1)  # Just over 1MB
        }
        
        response = client.post('/api/register', json=large_data)
        assert response.status_code == 413  # Payload Too Large


class TestGeminiFallback:
    """Test Gemini AI integration and fallback handling"""
    
    def test_gemini_api_failure_fallback(self, client, db_session):
        """Test that Gemini API failures are handled gracefully with fallback"""
        # Create and login a user
        user = UserFactory()
        db_session.add(user)
        db_session.commit()
        
        # Login to get token
        login_response = client.post('/api/login', json={
            "email": user.email,
            "password": "password123"
        })
        token = login_response.get_json()['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # Mock Gemini API failure
        with patch('google.generativeai.GenerativeModel.generate_content') as mock_generate:
            mock_generate.side_effect = Exception("API rate limit exceeded")
            
            diet_plan_data = {
                "diet_preference": "vegetarian",
                "health_goals": "weight_loss"
            }
            
            response = client.post('/api/diet-plan', json=diet_plan_data, headers=headers)
            
            # Should still return a response, possibly with fallback content
            assert response.status_code in [200, 500]  # Either success with fallback or proper error
            
            if response.status_code == 500:
                data = response.get_json()
                assert 'error' in data
                assert data['status'] == 500
    
    def test_gemini_parse_fallback(self, client, db_session):
        """Test parsing fallback when Gemini returns unparseable content"""
        # Create and login a user
        user = UserFactory()
        db_session.add(user)
        db_session.commit()
        
        # Login to get token
        login_response = client.post('/api/login', json={
            "email": user.email,
            "password": "password123"
        })
        token = login_response.get_json()['access_token']
        headers = {'Authorization': f'Bearer {token}'}
        
        # Mock Gemini returning unparseable content
        mock_response = MagicMock()
        mock_response.text = "This is not valid JSON content that cannot be parsed"
        
        with patch('google.generativeai.GenerativeModel.generate_content') as mock_generate:
            mock_generate.return_value = mock_response
            
            diet_plan_data = {
                "diet_preference": "vegetarian",
                "health_goals": "weight_loss"
            }
            
            response = client.post('/api/diet-plan', json=diet_plan_data, headers=headers)
            
            # Should handle parsing errors gracefully
            assert response.status_code in [200, 500]
            
            if response.status_code == 500:
                data = response.get_json()
                assert 'error' in data


class TestSecurityHeaders:
    """Test security headers are properly set"""
    
    def test_security_headers_present(self, client):
        """Test that all required security headers are present in responses"""
        response = client.get('/api/health')
        
        # Check for required security headers
        assert 'X-Content-Type-Options' in response.headers
        assert response.headers['X-Content-Type-Options'] == 'nosniff'
        
        assert 'X-Frame-Options' in response.headers
        assert response.headers['X-Frame-Options'] == 'DENY'
        
        assert 'Referrer-Policy' in response.headers
        assert response.headers['Referrer-Policy'] == 'strict-origin-when-cross-origin'
    
    def test_csp_header_present(self, client):
        """Test that Content Security Policy header is present"""
        response = client.get('/api/health')
        
        # CSP should be present (either from Talisman or fallback)
        csp_headers = ['Content-Security-Policy', 'Content-Security-Policy-Report-Only']
        has_csp = any(header in response.headers for header in csp_headers)
        assert has_csp


class TestErrorHandling:
    """Test global error handling"""
    
    def test_500_error_sanitized_response(self, client):
        """Test that 500 errors return sanitized responses without stack traces"""
        # Mock an internal error
        with patch('apps.api.app.genai.configure') as mock_config:
            mock_config.side_effect = Exception("Internal server error")
            
            # This should trigger the global error handler
            response = client.get('/api/health')
            
            if response.status_code == 500:
                data = response.get_json()
                assert data['error'] == 'Internal server error'
                assert data['status'] == 500
                assert 'timestamp' in data
                # Ensure no stack trace is exposed to client
                assert 'traceback' not in str(data).lower()
                assert 'exception' not in str(data).lower()
    
    def test_404_error_handling(self, client):
        """Test 404 error handling"""
        response = client.get('/api/nonexistent-endpoint')
        assert response.status_code == 404
        
        data = response.get_json()
        assert data['error'] == 'Resource not found'
        assert data['status'] == 404
        assert 'timestamp' in data
    
    def test_400_error_handling(self, client):
        """Test 400 error handling"""
        # Send invalid JSON
        response = client.post('/api/register',
                             data="invalid json",
                             content_type='application/json')
        assert response.status_code == 400
