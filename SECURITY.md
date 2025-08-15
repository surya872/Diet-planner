# Security Policy

## 🔒 Security Overview

The Diet Planner application implements enterprise-level security measures to protect user data and ensure secure operations. This document outlines our security practices, policies, and procedures.

## 📋 Table of Contents

- [Security Features](#security-features)
- [Supported Versions](#supported-versions)
- [Reporting Vulnerabilities](#reporting-vulnerabilities)
- [Security Architecture](#security-architecture)
- [Data Protection](#data-protection)
- [Authentication & Authorization](#authentication--authorization)
- [Input Validation](#input-validation)
- [Rate Limiting](#rate-limiting)
- [Security Headers](#security-headers)
- [Dependency Management](#dependency-management)
- [Deployment Security](#deployment-security)
- [Monitoring & Incident Response](#monitoring--incident-response)

## 🛡️ Security Features

### Implemented Security Controls

- ✅ **Authentication**: JWT-based stateless authentication
- ✅ **Authorization**: Role-based access control ready
- ✅ **Password Security**: bcrypt hashing with salt
- ✅ **Rate Limiting**: API endpoint protection
- ✅ **Input Validation**: Multi-layer validation and sanitization
- ✅ **Security Headers**: CSP, HSTS, X-Frame-Options, etc.
- ✅ **CORS Protection**: Configured origins control
- ✅ **SQL Injection Prevention**: ORM-based queries
- ✅ **XSS Protection**: Input sanitization and CSP
- ✅ **Error Handling**: Sanitized error responses
- ✅ **Dependency Scanning**: Automated vulnerability detection
- ✅ **Security Auditing**: Regular security scans

## 📅 Supported Versions

We actively maintain security updates for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | ✅ Yes            |
| < 1.0   | ❌ No             |

## 🚨 Reporting Vulnerabilities

### Security Contact

If you discover a security vulnerability, please report it responsibly:

- **Email**: security@dietplanner.com (if available)
- **GitHub**: Create a private security advisory
- **Response Time**: We aim to respond within 24 hours

### What to Include

When reporting a security issue, please provide:

1. **Description**: Clear description of the vulnerability
2. **Steps to Reproduce**: Detailed reproduction steps
3. **Impact Assessment**: Potential impact and affected components
4. **Proof of Concept**: If available (please be responsible)
5. **Suggested Fix**: If you have ideas for remediation

### Responsible Disclosure

- **Do not** publicly disclose the vulnerability until we've had a chance to investigate
- **Do not** access or modify user data without permission
- **Do not** perform denial of service attacks
- We will credit security researchers who follow responsible disclosure

## 🏗️ Security Architecture

### Application Layer Security

```
┌─────────────────────────────────────────────────────────────┐
│                    SECURITY LAYERS                         │
├─────────────────────────────────────────────────────────────┤
│ 🌐 Transport Layer (HTTPS/TLS)                            │
├─────────────────────────────────────────────────────────────┤
│ 🛡️  Security Headers (CSP, HSTS, X-Frame-Options)        │
├─────────────────────────────────────────────────────────────┤
│ 🚦 Rate Limiting (Login: 10/min, Diet Plans: 5/min)      │
├─────────────────────────────────────────────────────────────┤
│ 🔐 Authentication (JWT with 30min expiry in prod)         │
├─────────────────────────────────────────────────────────────┤
│ ✅ Input Validation (Multi-layer validation)              │
├─────────────────────────────────────────────────────────────┤
│ 🗄️  Data Layer Protection (ORM, parameterized queries)    │
└─────────────────────────────────────────────────────────────┘
```

### Security Boundaries

1. **External Boundary**: Internet ↔ Load Balancer/CDN
2. **Application Boundary**: Load Balancer ↔ Application Server
3. **Data Boundary**: Application Server ↔ Database
4. **Service Boundary**: Application ↔ External APIs (Gemini)

## 🔒 Data Protection

### Data Classification

- **Public**: API documentation, general app information
- **Internal**: Application logs, system metrics
- **Confidential**: User profiles, diet plans
- **Restricted**: Authentication credentials, API keys

### Data Encryption

- **In Transit**: TLS 1.3 for all HTTP communications
- **At Rest**: Database encryption enabled in production
- **Application**: Secrets stored in environment variables
- **Passwords**: bcrypt hashing with salt rounds

### Data Retention

- **User Data**: Retained until account deletion
- **Logs**: 30 days retention for security logs
- **Backups**: Encrypted backups with 1-year retention
- **Analytics**: Anonymized data only

## 🔐 Authentication & Authorization

### Authentication Flow

```
1. User submits credentials → POST /api/login
2. Server validates credentials (bcrypt verification)
3. Server generates JWT token (30min expiry in production)
4. Client stores token securely
5. Client includes token in Authorization header
6. Server validates token on protected routes
```

### JWT Configuration

- **Algorithm**: HS256
- **Expiry**: 
  - Development: 24 hours
  - Production: 30 minutes
  - Testing: 10 minutes
- **Claims**: `user_id`, `exp`, `iat`
- **Secret**: Environment-specific, rotated regularly

### Authorization Levels

- **Public**: Health checks, registration, login
- **Authenticated**: Profile access, diet plan generation
- **Admin**: System administration (future implementation)

## ✅ Input Validation

### Validation Layers

1. **Frontend Validation**: Basic type checking and format validation
2. **API Validation**: Comprehensive server-side validation
3. **Database Validation**: Schema constraints and triggers

### Validation Rules

```python
# User Registration/Profile Validation
{
    "name": {"required": True, "min_length": 2, "max_length": 100},
    "email": {"required": True, "format": "email", "max_length": 255},
    "password": {"required": True, "min_length": 6, "max_length": 100},
    "age": {"required": True, "min_value": 1, "max_value": 120},
    "gender": {"required": True, "allowed_values": ["male", "female", "other"]},
    "weight": {"required": True, "min_value": 20, "max_value": 300}
}
```

### Sanitization

- **XSS Prevention**: HTML entity encoding
- **SQL Injection**: ORM-based parameterized queries
- **Path Traversal**: Input path validation
- **Command Injection**: No direct command execution

## 🚦 Rate Limiting

### Endpoint Rate Limits

| Endpoint | Rate Limit | Window | Error Code |
|----------|------------|--------|------------|
| `POST /api/login` | 10 requests | 1 minute | 429 |
| `POST /api/diet-plan` | 5 requests | 1 minute | 429 |
| `POST /api/register` | 5 requests | 1 minute | 429 |
| `Global Default` | 1000 requests | 1 hour | 429 |

### Rate Limiting Implementation

- **Storage**: Redis for distributed rate limiting
- **Strategy**: Token bucket algorithm
- **Headers**: Rate limit headers in responses
- **Bypass**: Admin users can bypass limits (future)

## 🛡️ Security Headers

### Implemented Headers

```http
# Content Security Policy
Content-Security-Policy: default-src 'self'; script-src 'self' https://apis.google.com

# Prevent MIME sniffing
X-Content-Type-Options: nosniff

# Prevent clickjacking
X-Frame-Options: DENY

# Control referrer information
Referrer-Policy: strict-origin-when-cross-origin

# HTTPS enforcement (production)
Strict-Transport-Security: max-age=31536000; includeSubDomains

# XSS protection
X-XSS-Protection: 1; mode=block
```

### CORS Configuration

```python
# Development
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001", 
    "http://localhost:3002"
]

# Production
CORS_ORIGINS = [
    "https://your-production-domain.com"
]
```

## 📦 Dependency Management

### Security Scanning

```bash
# Python dependencies
pip-audit --desc --format=json
safety check
bandit -r apps/api/

# Node.js dependencies
npm audit --audit-level moderate
```

### Update Strategy

- **Critical Security Updates**: Applied immediately
- **Major Updates**: Tested in staging first
- **Regular Updates**: Monthly dependency review
- **Automated Scanning**: CI/CD pipeline integration

### Pinned Dependencies

All dependencies are pinned to specific versions for security and reproducibility:

```python
# Example from requirements.txt
Flask==3.0.0
psycopg2-binary==2.9.9
bcrypt==4.1.2
```

## 🚀 Deployment Security

### Environment Security

- **Secrets Management**: Environment variables only
- **Key Rotation**: Regular rotation of secrets
- **Access Control**: Least privilege principle
- **Network Security**: VPC isolation when possible

### Production Hardening

```python
# Production configuration
DEBUG = False
TESTING = False
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Strict'
```

### Container Security

- **Base Images**: Official, minimal images
- **Non-root User**: Containers run as non-root
- **Resource Limits**: CPU and memory constraints
- **Scanning**: Regular image vulnerability scans

## 📊 Monitoring & Incident Response

### Security Monitoring

- **Failed Authentication**: Track failed login attempts
- **Rate Limiting**: Monitor rate limit violations
- **Error Rates**: Unusual error patterns
- **Resource Usage**: Detect DoS attempts

### Logging Strategy

```python
# Security event logging
app.logger.warning(f"Failed login attempt for user: {email} from {client_ip}")
app.logger.error(f"Rate limit exceeded for {client_ip}")
app.logger.info(f"Successful login for user: {email}")
```

### Incident Response

1. **Detection**: Automated monitoring alerts
2. **Assessment**: Evaluate impact and scope
3. **Containment**: Isolate affected systems
4. **Eradication**: Remove threats and vulnerabilities
5. **Recovery**: Restore normal operations
6. **Lessons Learned**: Post-incident review

### Emergency Contacts

- **Security Team**: security@dietplanner.com
- **Infrastructure**: devops@dietplanner.com
- **Management**: management@dietplanner.com

## 🔧 Security Configuration Examples

### Environment Variables

```bash
# Required security environment variables
APP_ENV=production
FLASK_SECRET_KEY=<32-character-random-string>
JWT_SECRET_KEY=<32-character-random-string>
POSTGRES_PASSWORD=<strong-database-password>
```

### API Security Middleware

```python
# Security middleware configuration
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1MB
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)
app.config['RATELIMIT_DEFAULT'] = "1000 per hour"
```

## 📚 Security Resources

### Internal Documentation

- [OPERATIONS.md](./OPERATIONS.md) - Operational security procedures
- [DEVELOPMENT.md](./DEVELOPMENT.md) - Secure development practices
- [ARCHITECTURE.md](./ARCHITECTURE.md) - Security architecture details

### External References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Flask Security Best Practices](https://flask.palletsprojects.com/en/2.3.x/security/)
- [JWT Security Best Practices](https://datatracker.ietf.org/doc/html/draft-ietf-oauth-jwt-bcp-07)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

## 📞 Security Contacts

For security-related inquiries:

- **General Security**: security@dietplanner.com
- **Vulnerability Reports**: Use GitHub Security Advisories
- **Emergency**: Include "URGENT SECURITY" in subject line

---

**Last Updated**: December 2024
**Next Review**: March 2025
