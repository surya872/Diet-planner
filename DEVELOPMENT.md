# Development Guide - Diet Planner Application

## 🏗️ Enterprise-Level SDLC Implementation

This project follows enterprise-level Software Development Life Cycle (SDLC) practices with Test-Driven Development (TDD) methodology.

## 📋 Table of Contents

- [Development Setup](#development-setup)
- [Test-Driven Development](#test-driven-development)
- [Code Quality Standards](#code-quality-standards)
- [CI/CD Pipeline](#cicd-pipeline)
- [Environment Management](#environment-management)
- [Testing Strategy](#testing-strategy)
- [Code Review Process](#code-review-process)
- [Security Guidelines](#security-guidelines)

## 🚀 Development Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Git

### Quick Start
```bash
# Clone and setup
git clone <repository-url>
cd diet-planner

# Install all dependencies
make install

# Setup database
make setup-db

# Run all tests
make test

# Start development servers
make dev
```

### Manual Setup
```bash
# Backend setup
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Frontend setup
cd frontend
npm ci

# Database setup
./setup_database.sh
```

## 🧪 Test-Driven Development (TDD)

### TDD Cycle
1. **Red**: Write a failing test
2. **Green**: Write minimal code to pass
3. **Refactor**: Improve code while keeping tests green

### Testing Commands
```bash
# Run all tests
make test

# Run backend tests only
make test-backend

# Run frontend tests only
make test-frontend

# Run with coverage
make coverage

# Run specific test types
make test-integration
make test-e2e
```

### Test Structure

#### Backend Tests
```
backend/tests/
├── unit/           # Unit tests for individual components
├── integration/    # Integration tests for API workflows
└── e2e/           # End-to-end tests
```

#### Frontend Tests
```
frontend/src/__tests__/
├── components/     # Component unit tests
├── services/      # API service tests
└── utils/         # Utility function tests
```

### Test Coverage Requirements
- **Minimum Coverage**: 80%
- **Critical Paths**: 100% (authentication, payments)
- **Integration Tests**: All API endpoints
- **Frontend Components**: All user-facing components

## 📝 Code Quality Standards

### Backend Standards
- **PEP 8** compliance via `flake8`
- **Code formatting** via `black`
- **Import sorting** via `isort`
- **Type checking** via `mypy`
- **Security scanning** via `bandit`

### Frontend Standards
- **ESLint** for code quality
- **Prettier** for formatting
- **TypeScript** for type safety
- **Testing Library** for component testing

### Running Quality Checks
```bash
# All quality checks
make lint

# Format all code
make format

# Security scan
make security-scan
```

## 🔄 CI/CD Pipeline

### GitHub Actions Workflow
The CI/CD pipeline runs on every push and pull request:

1. **Code Quality Checks**
   - Linting (flake8, ESLint)
   - Formatting (black, prettier)
   - Type checking (mypy, TypeScript)

2. **Testing**
   - Unit tests (pytest, Jest)
   - Integration tests
   - Coverage reporting

3. **Security Scanning**
   - Dependency vulnerabilities
   - Code security issues

4. **Build & Deploy**
   - Docker image builds
   - Deployment to staging/production

### Pipeline Commands
```bash
# Run full CI pipeline locally
make ci

# Pre-commit checks
make pre-commit
```

## 🌍 Environment Management

### Environment Files
- `.env.example` - Template for environment variables
- `.env` - Local development (not in git)
- `.env.test` - Testing environment
- `.env.production` - Production environment

### Required Environment Variables
```bash
# Database
POSTGRES_HOST=localhost
POSTGRES_DB=diet_planner
POSTGRES_USER=diet_user
POSTGRES_PASSWORD=your_password

# API Keys
GEMINI_API_KEY=your_gemini_key

# Security
FLASK_SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret

# Environment
FLASK_ENV=development
```

### Environment Setup
```bash
# Copy example file
cp env.example .env

# Edit with your values
nano .env
```

## 🎯 Testing Strategy

### Test Pyramid
```
    /\
   /  \     E2E Tests (Few, Slow, High Confidence)
  /____\
 /      \    Integration Tests (Some, Medium Speed)
/__________\  Unit Tests (Many, Fast, Focused)
```

### Backend Testing
- **Unit Tests**: Models, utilities, business logic
- **Integration Tests**: API endpoints, database operations
- **E2E Tests**: Complete user workflows

### Frontend Testing
- **Unit Tests**: Components, hooks, utilities
- **Integration Tests**: Component interactions
- **E2E Tests**: User journeys (Cypress/Playwright)

### Test Data Management
- **Factories**: Use `factory-boy` for test data creation
- **Fixtures**: Shared test setup in `conftest.py`
- **Mocking**: Mock external services (Gemini API)

## 👥 Code Review Process

### Pull Request Requirements
1. **All tests passing**
2. **Code coverage maintained**
3. **Linting checks pass**
4. **Security scan clean**
5. **Peer review approval**

### Review Checklist
- [ ] Code follows style guidelines
- [ ] Tests cover new functionality
- [ ] Documentation updated
- [ ] No security vulnerabilities
- [ ] Performance considerations
- [ ] Error handling implemented

## 🔒 Security Guidelines

### Authentication & Authorization
- JWT tokens with expiration
- Password hashing with bcrypt
- Input validation and sanitization
- CORS properly configured

### Data Protection
- Environment variables for secrets
- SQL injection prevention
- XSS protection
- HTTPS in production

### Security Tools
- `bandit` for Python security scanning
- `npm audit` for Node.js vulnerabilities
- Dependency updates via Dependabot

## 📊 Monitoring & Logging

### Development Logging
```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)
```

### Health Checks
```bash
# Check application health
make health

# Manual health check
curl http://localhost:5001/api/health
curl http://localhost:3001
```

## 🛠️ Development Workflow

### Feature Development
1. **Create feature branch** from `develop`
2. **Write failing tests** (TDD Red)
3. **Implement minimum code** (TDD Green)
4. **Refactor and improve** (TDD Refactor)
5. **Run full test suite**
6. **Create pull request**
7. **Code review and merge**

### Git Workflow
```bash
# Start new feature
git checkout develop
git pull origin develop
git checkout -b feature/new-feature

# During development
git add .
git commit -m "feat: add new feature"

# Before push
make pre-commit

# Push and create PR
git push origin feature/new-feature
```

### Branch Naming
- `feature/description` - New features
- `bugfix/description` - Bug fixes
- `hotfix/description` - Critical fixes
- `refactor/description` - Code refactoring

## 📈 Performance Guidelines

### Backend Performance
- Database query optimization
- API response caching
- Background task processing
- Resource monitoring

### Frontend Performance
- Code splitting
- Lazy loading
- Image optimization
- Bundle size monitoring

## 🔧 Debugging

### Backend Debugging
```bash
# Debug mode
FLASK_ENV=development python app.py

# With debugger
python -m pdb app.py
```

### Frontend Debugging
```bash
# Development server with debugging
npm start

# Build analysis
npm run build
npm run analyze
```

## 📚 Additional Resources

- [Flask Testing Guide](https://flask.palletsprojects.com/en/2.3.x/testing/)
- [React Testing Library](https://testing-library.com/docs/react-testing-library/intro/)
- [pytest Documentation](https://docs.pytest.org/en/stable/)
- [GitHub Actions](https://docs.github.com/en/actions)

---

For questions or support, please contact the development team or create an issue in the repository.
