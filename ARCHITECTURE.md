# Diet Planner Application - 3-Tier Architecture

## 🏗️ Enterprise Architecture Overview

The Diet Planner application follows a modern 3-tier enterprise architecture pattern, implementing separation of concerns, scalability, and maintainability principles.

## 📋 Table of Contents

- [Architecture Overview](#architecture-overview)
- [Tier 1: Presentation Layer](#tier-1-presentation-layer)
- [Tier 2: Application Layer](#tier-2-application-layer)
- [Tier 3: Data Layer](#tier-3-data-layer)
- [Cross-Cutting Concerns](#cross-cutting-concerns)
- [Deployment Architecture](#deployment-architecture)
- [Security Architecture](#security-architecture)
- [Monitoring & Observability](#monitoring--observability)

## 🎯 Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     PRESENTATION LAYER                         │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │   React     │  │  TypeScript │  │  Tailwind   │            │
│  │   Frontend  │  │   Strict    │  │    CSS      │            │
│  │             │  │   Types     │  │   Styling   │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
└─────────────────────────────────────────────────────────────────┘
                                │
                            HTTP/HTTPS
                                │
┌─────────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │    Flask    │  │  Security   │  │ Monitoring  │            │
│  │   RESTful   │  │   Headers   │  │   Health    │            │
│  │     API     │  │ Rate Limit  │  │   Checks    │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │    JWT      │  │  Validation │  │   Gemini    │            │
│  │    Auth     │  │   Layer     │  │     AI      │            │
│  │             │  │             │  │   Service   │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
└─────────────────────────────────────────────────────────────────┘
                                │
                             SQL/ORM
                                │
┌─────────────────────────────────────────────────────────────────┐
│                       DATA LAYER                               │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │ PostgreSQL  │  │ SQLAlchemy  │  │  Database   │            │
│  │  Database   │  │     ORM     │  │ Migrations  │            │
│  │             │  │             │  │             │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│  │   Backup    │  │ Connection  │  │   Indexing  │            │
│  │  Strategy   │  │   Pooling   │  │ Optimization│            │
│  │             │  │             │  │             │            │
│  └─────────────┘  └─────────────┘  └─────────────┘            │
└─────────────────────────────────────────────────────────────────┘
```

## 🎨 Tier 1: Presentation Layer

### Technology Stack
- **Framework**: React 18 with TypeScript
- **Styling**: Tailwind CSS with custom components
- **Routing**: React Router DOM v6
- **State Management**: React Hooks + Context API
- **Build Tool**: Create React App with custom configurations

### Key Components

#### 1. User Interface Components
```
frontend/src/components/
├── Header.tsx              # Navigation and user info
├── LoadingSpinner.tsx      # Loading indicators
├── Login.tsx              # User authentication
├── UserForm.tsx           # Registration form
├── Profile.tsx            # User profile management
└── DietPlanView.tsx       # Diet plan display
```

#### 2. Service Layer
```
frontend/src/services/
├── api.ts                 # API communication layer
└── auth.ts               # Authentication utilities
```

#### 3. Type Definitions
```
frontend/src/types/
├── index.ts              # Application-wide type definitions
├── api.ts                # API response types
└── user.ts               # User-related types
```

### Architecture Principles
- **Component Separation**: Functional components with single responsibility
- **Type Safety**: Strict TypeScript configuration
- **Responsive Design**: Mobile-first approach with Tailwind CSS
- **Performance**: Code splitting and lazy loading
- **Accessibility**: WCAG 2.1 AA compliance

### State Management Strategy
```typescript
// Context-based state management
interface AppState {
  user: User | null;
  isAuthenticated: boolean;
  loading: boolean;
  error: string | null;
  dietPlan: DietPlan | null;
}

// Actions for state updates
type AppAction = 
  | { type: 'SET_USER'; payload: User }
  | { type: 'SET_LOADING'; payload: boolean }
  | { type: 'SET_ERROR'; payload: string }
  | { type: 'LOGOUT' };
```

## ⚙️ Tier 2: Application Layer

### Technology Stack
- **Framework**: Flask 2.3+ with Python 3.11+
- **API Design**: RESTful architecture
- **Authentication**: JWT with Flask-JWT-Extended
- **Validation**: Marshmallow schemas
- **Database ORM**: SQLAlchemy with Flask-SQLAlchemy

### Application Structure
```
backend/
├── app.py                 # Main application entry point
├── config.py             # Environment-specific configurations
├── security.py           # Security middleware and utilities
├── monitoring.py         # Application monitoring and health checks
├── models/               # Database models (future expansion)
├── services/             # Business logic services (future expansion)
├── utils/                # Utility functions
└── tests/                # Comprehensive test suite
```

### API Architecture

#### 1. Authentication Endpoints
```python
POST /api/register        # User registration
POST /api/login          # User authentication
GET  /api/profile        # Get user profile
PUT  /api/profile        # Update user profile
```

#### 2. Diet Plan Endpoints
```python
POST /api/diet-plan      # Generate new diet plan
GET  /api/diet-plans     # Get user's diet plans
GET  /api/diet-plan/<id> # Get specific diet plan
```

#### 3. Health & Monitoring Endpoints
```python
GET  /api/health         # Basic health check
GET  /api/health/detailed # Detailed health metrics
GET  /api/metrics        # Prometheus-compatible metrics
GET  /api/performance    # Performance analysis
```

### Security Implementation

#### 1. Input Validation
```python
def validate_user_data(data, is_update=False):
    """Comprehensive input validation with security checks"""
    # XSS prevention
    # SQL injection prevention
    # Data type validation
    # Business rule validation
```

#### 2. Authentication & Authorization
```python
# JWT-based authentication
@jwt_required()
def protected_endpoint():
    current_user = get_jwt_identity()
    # Business logic
```

#### 3. Rate Limiting
```python
# Endpoint-specific rate limiting
@limiter.limit("5 per minute")
@app.route("/api/login", methods=["POST"])
def login():
    # Authentication logic
```

### Business Logic Layer

#### 1. User Management Service
- User registration and authentication
- Profile management
- Password security (bcrypt hashing)

#### 2. Diet Plan Generation Service
- AI integration with Google Gemini
- Nutritional calculations
- Personalization algorithms

#### 3. Data Validation Service
- Input sanitization
- Business rule enforcement
- Security validation

## 🗄️ Tier 3: Data Layer

### Database Architecture

#### 1. PostgreSQL Database Design
```sql
-- Core database schema
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    age INTEGER NOT NULL,
    gender VARCHAR(20) NOT NULL,
    weight NUMERIC(5,2) NOT NULL,
    height NUMERIC(5,2),
    activity_level VARCHAR(50),
    diet_preference VARCHAR(50),
    health_goals TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE diet_plans (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    plan_name VARCHAR(255) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    total_calories INTEGER,
    plan_data JSONB NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE meal_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    meal_name VARCHAR(255) NOT NULL,
    calories INTEGER,
    logged_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 2. Database Optimization
- **Indexing Strategy**: Optimized indexes for query performance
- **Connection Pooling**: Efficient connection management
- **Query Optimization**: Analyzed and optimized queries
- **Backup Strategy**: Automated backup and recovery procedures

#### 3. Data Access Layer
```python
# SQLAlchemy ORM models
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    # ... other fields
    
    # Relationships
    diet_plans = db.relationship('DietPlan', backref='user', lazy=True)
    meal_logs = db.relationship('MealLog', backref='user', lazy=True)
```

### Data Management Strategies

#### 1. Migration Management
```bash
# Database migration workflow
./manage_database.sh migrate    # Apply migrations
./manage_database.sh backup     # Backup database
./manage_database.sh restore    # Restore from backup
```

#### 2. Data Validation
- Schema-level constraints
- Application-level validation
- Business rule enforcement

#### 3. Performance Monitoring
- Query performance tracking
- Connection pool monitoring
- Database health checks

## 🔄 Cross-Cutting Concerns

### 1. Security Architecture

#### Authentication Flow
```
Client → Login Request → Backend
Backend → Validate Credentials → Database
Database → Return User Data → Backend
Backend → Generate JWT Token → Client
Client → Store Token → LocalStorage
Client → Include Token in Headers → Subsequent Requests
```

#### Security Layers
- **Transport Security**: HTTPS/TLS encryption
- **Authentication**: JWT-based stateless authentication
- **Authorization**: Role-based access control (ready for expansion)
- **Input Validation**: Multi-layer validation and sanitization
- **Output Encoding**: XSS prevention
- **Rate Limiting**: DDoS and brute force protection

### 2. Error Handling Strategy

#### Frontend Error Handling
```typescript
// Centralized error handling
const handleApiError = (error: AxiosError) => {
  if (error.response?.status === 401) {
    // Handle authentication errors
    logout();
    redirectToLogin();
  } else if (error.response?.status >= 500) {
    // Handle server errors
    showErrorNotification('Server error occurred');
  }
  // Log error for monitoring
  logError(error);
};
```

#### Backend Error Handling
```python
# Global error handlers
@app.errorhandler(ValidationError)
def handle_validation_error(error):
    return jsonify({'error': error.messages}), 400

@app.errorhandler(500)
def handle_internal_error(error):
    app.logger.error(f'Internal error: {error}')
    return jsonify({'error': 'Internal server error'}), 500
```

### 3. Logging and Monitoring

#### Application Monitoring
- **Health Checks**: Endpoint health monitoring
- **Performance Metrics**: Response time tracking
- **Error Tracking**: Centralized error logging
- **Resource Monitoring**: CPU, memory, and disk usage

#### Logging Strategy
```python
# Structured logging
import logging

logger = logging.getLogger(__name__)

# Log levels:
# ERROR: System failures, exceptions
# WARNING: Potential issues, failed login attempts
# INFO: Normal operations, successful requests
# DEBUG: Detailed execution flow (development only)
```

## 🚀 Deployment Architecture

### Multi-Environment Strategy

#### 1. Development Environment
- Local development setup
- Hot reloading for rapid development
- Comprehensive logging and debugging
- Mock services for external dependencies

#### 2. Staging Environment
- Production-like environment for testing
- Automated deployment from develop branch
- Integration testing with real services
- Performance testing and load testing

#### 3. Production Environment
- Optimized for performance and reliability
- Auto-scaling capabilities
- Comprehensive monitoring and alerting
- Backup and disaster recovery procedures

### Container Architecture
```dockerfile
# Multi-stage build for optimization
FROM node:18-alpine AS frontend-build
# Frontend build process

FROM python:3.11-slim AS backend-build
# Backend build process

FROM nginx:alpine AS production
# Production-ready container
```

### Cloud Deployment Options

#### 1. Render.com (Recommended for simplicity)
- Automatic deployments from Git
- Managed PostgreSQL database
- Built-in SSL certificates
- Environment variable management

#### 2. Railway.app (Good for scalability)
- Container-based deployments
- Automatic scaling
- Integrated monitoring
- Database management

#### 3. Vercel + Backend hosting
- Optimized frontend hosting
- Serverless backend functions
- Global CDN distribution
- Analytics and monitoring

## 📊 Performance Considerations

### Frontend Optimization
- **Code Splitting**: Lazy loading of components
- **Bundle Optimization**: Tree shaking and minification
- **Caching Strategy**: Service worker implementation
- **Image Optimization**: WebP format and lazy loading

### Backend Optimization
- **Database Connection Pooling**: Efficient connection management
- **Query Optimization**: Indexed queries and query analysis
- **Caching Layer**: Redis for session and data caching
- **Rate Limiting**: Protection against abuse

### Monitoring and Alerting
- **Application Performance Monitoring (APM)**
- **Real User Monitoring (RUM)**
- **Infrastructure monitoring**
- **Custom business metrics**

## 🔐 Security Best Practices

### Data Protection
- **Encryption at Rest**: Database encryption
- **Encryption in Transit**: HTTPS/TLS
- **Key Management**: Secure environment variables
- **Access Control**: Principle of least privilege

### Compliance Considerations
- **GDPR Compliance**: Data privacy and user rights
- **Data Retention**: Automated data cleanup policies
- **Audit Logging**: Comprehensive audit trails
- **Security Scanning**: Automated vulnerability assessment

## 📈 Scalability and Future Enhancements

### Horizontal Scaling
- **Load Balancing**: Multiple application instances
- **Database Sharding**: Horizontal database scaling
- **Microservices**: Service decomposition strategy
- **API Gateway**: Centralized API management

### Potential Enhancements
- **Mobile Applications**: React Native implementation
- **Real-time Features**: WebSocket integration
- **Machine Learning**: Advanced recommendation engine
- **Social Features**: User community and sharing

This architecture provides a solid foundation for a scalable, secure, and maintainable diet planning application while following enterprise-level best practices.
