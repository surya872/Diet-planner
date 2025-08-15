"""
Enhanced Security Module for Diet Planner Application
Implements enterprise-level security measures
"""

import os
import re
import time
from functools import wraps
from typing import Dict, List, Optional

from flask import Flask, request, jsonify, current_app
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
import secrets
import hashlib
import hmac


class SecurityManager:
    """Centralized security management"""
    
    def __init__(self, app: Optional[Flask] = None):
        self.app = app
        self.failed_login_attempts: Dict[str, List[float]] = {}
        self.blocked_ips: Dict[str, float] = {}
        
        if app:
            self.init_app(app)
    
    def init_app(self, app: Flask):
        """Initialize security for Flask app"""
        self.app = app
        
        # Rate limiting
        self.limiter = Limiter(
            key_func=get_remote_address,
            default_limits=["1000 per hour", "100 per minute"]
        )
        self.limiter.init_app(app)
        
        # Security headers
        self.setup_security_headers(app)
        
        # Input validation
        self.setup_input_validation(app)
        
        # CSRF protection
        self.setup_csrf_protection(app)
    
    def setup_security_headers(self, app: Flask):
        """Configure security headers using Talisman"""
        csp = {
            'default-src': "'self'",
            'script-src': "'self' 'unsafe-inline' https://apis.google.com",
            'style-src': "'self' 'unsafe-inline' https://fonts.googleapis.com",
            'font-src': "'self' https://fonts.gstatic.com",
            'img-src': "'self' data: https:",
            'connect-src': "'self' https://generativelanguage.googleapis.com",
            'frame-ancestors': "'none'",
            'base-uri': "'self'",
            'object-src': "'none'"
        }
        
        # Only enforce HTTPS in production
        force_https = os.getenv('FLASK_ENV') == 'production'
        
        Talisman(
            app,
            force_https=force_https,
            strict_transport_security=True,
            strict_transport_security_max_age=31536000,
            content_security_policy=csp,
            content_security_policy_nonce_in=['script-src', 'style-src'],
            feature_policy={
                'geolocation': "'none'",
                'camera': "'none'",
                'microphone': "'none'"
            }
        )
    
    def setup_input_validation(self, app: Flask):
        """Setup input validation and sanitization"""
        
        @app.before_request
        def validate_input():
            if request.is_json and request.get_json():
                data = request.get_json()
                if not self.validate_json_input(data):
                    return jsonify({"error": "Invalid input data"}), 400
    
    def setup_csrf_protection(self, app: Flask):
        """Setup CSRF protection for state-changing operations"""
        
        @app.before_request
        def check_csrf():
            if request.method in ['POST', 'PUT', 'DELETE']:
                # Skip CSRF for API endpoints with JWT authentication
                if request.path.startswith('/api/') and 'Authorization' in request.headers:
                    return
                
                # Skip CSRF for registration and login endpoints (they don't have JWT yet)
                if request.path in ['/api/register', '/api/login', '/api/health']:
                    return
                
                csrf_token = request.headers.get('X-CSRF-Token')
                session_token = request.cookies.get('csrf_token')
                
                if not csrf_token or not session_token or csrf_token != session_token:
                    return jsonify({"error": "CSRF token missing or invalid"}), 403
    
    def validate_json_input(self, data: dict) -> bool:
        """Validate JSON input for common security issues"""
        if not isinstance(data, dict):
            return False
        
        # Check for excessively large payloads
        if len(str(data)) > 10000:  # 10KB limit
            return False
        
        # Check for suspicious patterns
        suspicious_patterns = [
            r'<script.*?>.*?</script>',  # XSS
            r'javascript:',  # XSS
            r'on\w+\s*=',  # Event handlers
            r'union\s+select',  # SQL injection
            r'drop\s+table',  # SQL injection
            r'\.\./\.\.',  # Directory traversal
        ]
        
        data_str = str(data).lower()
        for pattern in suspicious_patterns:
            if re.search(pattern, data_str, re.IGNORECASE):
                return False
        
        return True
    
    def rate_limit_login_attempts(self, email: str, ip: str) -> bool:
        """Rate limit login attempts per email and IP"""
        current_time = time.time()
        
        # Clean old attempts (older than 15 minutes)
        cutoff_time = current_time - 900
        
        # Check email-based rate limiting
        if email in self.failed_login_attempts:
            self.failed_login_attempts[email] = [
                t for t in self.failed_login_attempts[email] if t > cutoff_time
            ]
            
            if len(self.failed_login_attempts[email]) >= 5:
                return False
        
        # Check IP-based rate limiting
        if ip in self.blocked_ips and self.blocked_ips[ip] > current_time:
            return False
        
        return True
    
    def record_failed_login(self, email: str, ip: str):
        """Record a failed login attempt"""
        current_time = time.time()
        
        # Record failed attempt for email
        if email not in self.failed_login_attempts:
            self.failed_login_attempts[email] = []
        self.failed_login_attempts[email].append(current_time)
        
        # Block IP for 15 minutes after 10 failed attempts
        email_attempts = len(self.failed_login_attempts[email])
        if email_attempts >= 10:
            self.blocked_ips[ip] = current_time + 900  # 15 minutes
    
    def generate_secure_token(self, length: int = 32) -> str:
        """Generate a cryptographically secure random token"""
        return secrets.token_urlsafe(length)
    
    def hash_api_key(self, api_key: str) -> str:
        """Hash an API key for secure storage"""
        salt = os.getenv('API_KEY_SALT', 'default_salt').encode()
        return hashlib.pbkdf2_hex(api_key.encode(), salt, 100000, 32)
    
    def verify_signature(self, payload: str, signature: str, secret: str) -> bool:
        """Verify HMAC signature for webhook/API validation"""
        expected_signature = hmac.new(
            secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()
        
        return hmac.compare_digest(signature, expected_signature)


def require_api_key(f):
    """Decorator to require API key authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key:
            return jsonify({"error": "API key required"}), 401
        
        # Verify API key (implement your own verification logic)
        if not verify_api_key(api_key):
            return jsonify({"error": "Invalid API key"}), 401
        
        return f(*args, **kwargs)
    return decorated_function


def verify_api_key(api_key: str) -> bool:
    """Verify API key against stored hash"""
    # Implementation depends on where you store API keys
    # This is a placeholder - implement according to your needs
    stored_hash = os.getenv('API_KEY_HASH')
    if not stored_hash:
        return False
    
    security_manager = SecurityManager()
    return security_manager.hash_api_key(api_key) == stored_hash


def require_admin(f):
    """Decorator to require admin privileges"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check if user has admin role
        # Implementation depends on your user role system
        return f(*args, **kwargs)
    return decorated_function


# Security configurations for different environments
SECURITY_CONFIGS = {
    'development': {
        'FORCE_HTTPS': False,
        'SESSION_COOKIE_SECURE': False,
        'REMEMBER_COOKIE_SECURE': False,
        'JWT_ACCESS_TOKEN_EXPIRES': 3600,  # 1 hour
    },
    'testing': {
        'FORCE_HTTPS': False,
        'SESSION_COOKIE_SECURE': False,
        'REMEMBER_COOKIE_SECURE': False,
        'JWT_ACCESS_TOKEN_EXPIRES': 600,  # 10 minutes
    },
    'production': {
        'FORCE_HTTPS': True,
        'SESSION_COOKIE_SECURE': True,
        'REMEMBER_COOKIE_SECURE': True,
        'SESSION_COOKIE_HTTPONLY': True,
        'SESSION_COOKIE_SAMESITE': 'Strict',
        'JWT_ACCESS_TOKEN_EXPIRES': 1800,  # 30 minutes
    }
}


def configure_security(app: Flask, environment: str = 'development'):
    """Configure security based on environment"""
    config = SECURITY_CONFIGS.get(environment, SECURITY_CONFIGS['development'])
    
    for key, value in config.items():
        app.config[key] = value
    
    # Initialize security manager
    security_manager = SecurityManager(app)
    
    return security_manager
