# Deployment Guide - Diet Planner Application

## 🚀 Complete Deployment Guide for Multiple Platforms

This guide provides step-by-step instructions for deploying the Diet Planner application to various cloud platforms and environments.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Environment Setup](#environment-setup)
- [Deployment Options](#deployment-options)
- [Platform-Specific Guides](#platform-specific-guides)
- [Post-Deployment](#post-deployment)
- [Monitoring & Maintenance](#monitoring--maintenance)
- [Troubleshooting](#troubleshooting)

## 🔧 Prerequisites

### Required Tools
```bash
# Install required tools
npm install -g vercel      # For Vercel deployments
npm install -g @railway/cli # For Railway deployments
curl -fsSL https://render.com/install | sh  # For Render deployments

# Docker (for container deployments)
docker --version
docker-compose --version

# Git (for version control)
git --version
```

### Required Accounts
- [Render.com](https://render.com) - Easiest option, free tier available
- [Railway.app](https://railway.app) - Developer-friendly, free tier
- [Vercel](https://vercel.com) - Excellent for frontend, free tier
- [Heroku](https://heroku.com) - Traditional PaaS, limited free tier
- [GitHub](https://github.com) - For code repository and CI/CD

## 🌍 Environment Setup

### 1. Environment Variables

Create environment-specific `.env` files:

#### `.env.production`
```env
# Production Environment Variables
FLASK_ENV=production
FLASK_SECRET_KEY=your_super_secure_secret_key_here
JWT_SECRET_KEY=your_jwt_secret_key_here

# Database (will be provided by hosting platform)
POSTGRES_HOST=your_db_host
POSTGRES_PORT=5432
POSTGRES_DB=diet_planner
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password

# AI Service
GEMINI_API_KEY=your_gemini_api_key_here

# Frontend URL (for CORS)
FRONTEND_URL=https://your-frontend-domain.com
```

#### `.env.staging`
```env
# Staging Environment Variables
FLASK_ENV=staging
FLASK_SECRET_KEY=staging_secret_key
JWT_SECRET_KEY=staging_jwt_secret

# Database
POSTGRES_HOST=staging_db_host
POSTGRES_PORT=5432
POSTGRES_DB=diet_planner_staging
POSTGRES_USER=staging_user
POSTGRES_PASSWORD=staging_password

# AI Service
GEMINI_API_KEY=your_gemini_api_key_here

# Frontend URL
FRONTEND_URL=https://staging-diet-planner.com
```

### 2. Security Keys Generation

```bash
# Generate secure keys
python -c "import secrets; print('FLASK_SECRET_KEY=' + secrets.token_urlsafe(32))"
python -c "import secrets; print('JWT_SECRET_KEY=' + secrets.token_urlsafe(32))"
```

## 🎯 Deployment Options

### Quick Comparison

| Platform | Difficulty | Free Tier | Database | Best For |
|----------|------------|-----------|----------|----------|
| **Render** | ⭐⭐ | ✅ Yes | PostgreSQL | Full-stack apps |
| **Railway** | ⭐⭐ | ✅ Yes | PostgreSQL | Developer experience |
| **Vercel** | ⭐ | ✅ Yes | External | Frontend + Serverless |
| **Heroku** | ⭐⭐⭐ | ⚠️ Limited | PostgreSQL | Traditional deployments |
| **Docker** | ⭐⭐⭐⭐ | N/A | Self-managed | Custom infrastructure |

## 📖 Platform-Specific Guides

### 🟢 Option 1: Render.com (Recommended)

#### Why Render?
- Easiest deployment process
- Free PostgreSQL database
- Automatic HTTPS
- GitHub integration
- Zero configuration required

#### Step-by-Step Deployment

1. **Prepare Your Repository**
   ```bash
   # Ensure your code is pushed to GitHub
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Deploy Using Blueprint**
   ```bash
   # Use our automated deployment script
   ./deployment/deploy.sh render --env production
   ```

3. **Manual Deployment (Alternative)**
   
   a. **Create Render Account**: Go to [render.com](https://render.com) and sign up
   
   b. **Connect GitHub**: Link your GitHub repository
   
   c. **Create Database**:
      - Go to Dashboard → New → PostgreSQL
      - Name: `diet-planner-db`
      - Plan: Free
      - Copy connection details
   
   d. **Deploy Backend**:
      - Go to Dashboard → New → Web Service
      - Connect your repository
      - Settings:
        ```
        Name: diet-planner-backend
        Environment: Python 3
        Build Command: cd backend && pip install -r requirements.txt
        Start Command: cd backend && gunicorn --bind 0.0.0.0:$PORT app:app
        ```
      - Environment Variables:
        ```
        FLASK_ENV=production
        FLASK_SECRET_KEY=[generated key]
        JWT_SECRET_KEY=[generated key]
        POSTGRES_HOST=[from database]
        POSTGRES_PORT=[from database]
        POSTGRES_DB=[from database]
        POSTGRES_USER=[from database]
        POSTGRES_PASSWORD=[from database]
        GEMINI_API_KEY=[your API key]
        ```
   
   e. **Deploy Frontend**:
      - Go to Dashboard → New → Static Site
      - Settings:
        ```
        Name: diet-planner-frontend
        Build Command: cd frontend && npm run build
        Publish Directory: frontend/build
        ```
      - Environment Variables:
        ```
        REACT_APP_API_URL=https://diet-planner-backend.onrender.com/api
        ```

4. **Verify Deployment**
   ```bash
   # Check backend health
   curl https://diet-planner-backend.onrender.com/api/health
   
   # Check frontend
   curl https://diet-planner-frontend.onrender.com
   ```

### 🚂 Option 2: Railway.app

#### Step-by-Step Deployment

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   railway login
   ```

2. **Deploy Backend**
   ```bash
   cd backend
   railway init
   railway add postgresql
   railway deploy
   ```

3. **Configure Environment**
   ```bash
   railway variables set FLASK_ENV=production
   railway variables set FLASK_SECRET_KEY=your_secret_key
   railway variables set JWT_SECRET_KEY=your_jwt_secret
   railway variables set GEMINI_API_KEY=your_gemini_key
   ```

4. **Deploy Frontend**
   ```bash
   cd ../frontend
   railway init
   railway variables set REACT_APP_API_URL=https://your-backend.railway.app/api
   railway deploy
   ```

### ▲ Option 3: Vercel (Frontend) + Backend Hosting

#### Frontend Deployment to Vercel

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   vercel login
   ```

2. **Deploy Frontend**
   ```bash
   cd frontend
   vercel --prod
   ```

3. **Configure Environment Variables**
   ```bash
   vercel env add REACT_APP_API_URL production
   # Enter your backend URL
   ```

#### Backend Options for Vercel
- Use Railway/Render for backend
- Use Vercel Serverless Functions (requires code adaptation)
- Use external database service

### 🐳 Option 4: Docker Deployment

#### Local Docker Deployment

1. **Build and Run**
   ```bash
   # Using our deployment script
   ./deployment/deploy.sh docker --build
   
   # Or manually
   docker-compose -f deployment/docker-compose.prod.yml up --build -d
   ```

2. **Check Services**
   ```bash
   docker-compose -f deployment/docker-compose.prod.yml ps
   docker-compose -f deployment/docker-compose.prod.yml logs -f
   ```

#### Cloud Docker Deployment

1. **Push to Container Registry**
   ```bash
   # Build images
   docker build -f backend/Dockerfile.prod -t your-registry/diet-planner-backend backend/
   docker build -f frontend/Dockerfile.prod -t your-registry/diet-planner-frontend frontend/
   
   # Push images
   docker push your-registry/diet-planner-backend
   docker push your-registry/diet-planner-frontend
   ```

2. **Deploy to Cloud Provider**
   - **DigitalOcean App Platform**
   - **Google Cloud Run**
   - **AWS ECS**
   - **Azure Container Instances**

### 💜 Option 5: Heroku

#### Step-by-Step Deployment

1. **Install Heroku CLI**
   ```bash
   # Install from https://devcenter.heroku.com/articles/heroku-cli
   heroku login
   ```

2. **Create Heroku Apps**
   ```bash
   # Backend
   heroku create your-diet-planner-backend
   heroku addons:create heroku-postgresql:mini --app your-diet-planner-backend
   
   # Frontend (optional, can use Vercel instead)
   heroku create your-diet-planner-frontend --buildpack mars/create-react-app
   ```

3. **Configure Environment Variables**
   ```bash
   heroku config:set FLASK_ENV=production --app your-diet-planner-backend
   heroku config:set FLASK_SECRET_KEY=your_secret --app your-diet-planner-backend
   heroku config:set JWT_SECRET_KEY=your_jwt_secret --app your-diet-planner-backend
   heroku config:set GEMINI_API_KEY=your_gemini_key --app your-diet-planner-backend
   ```

4. **Deploy**
   ```bash
   # Backend
   git subtree push --prefix backend heroku main
   
   # Frontend
   heroku config:set REACT_APP_API_URL=https://your-diet-planner-backend.herokuapp.com/api --app your-diet-planner-frontend
   git subtree push --prefix frontend heroku main
   ```

## ✅ Post-Deployment

### 1. Health Checks

```bash
# Backend health check
curl https://your-backend-url.com/api/health

# Expected response:
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "uptime": 3600,
  "checks": {
    "database": {"status": "healthy"},
    "external_services": {"gemini_ai": {"status": "healthy"}}
  }
}
```

### 2. Database Setup

```bash
# Run database migrations (if needed)
# This is typically done automatically, but can be run manually:

# For Render/Railway (via web terminal)
python -c "from app import db; db.create_all()"

# For Heroku
heroku run python -c "from app import db; db.create_all()" --app your-app-name
```

### 3. Environment Verification

```bash
# Test user registration
curl -X POST https://your-backend-url.com/api/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "password": "testpassword123",
    "age": 30,
    "gender": "male",
    "weight": 75
  }'

# Test login
curl -X POST https://your-backend-url.com/api/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpassword123"
  }'
```

## 📊 Monitoring & Maintenance

### 1. Application Monitoring

#### Health Check Endpoints
```bash
# Basic health
GET /api/health

# Detailed health with metrics
GET /api/health/detailed

# Performance metrics
GET /api/metrics

# Performance analysis
GET /api/performance
```

#### Setting Up Monitoring

1. **Uptime Monitoring**
   - Use UptimeRobot, Pingdom, or similar
   - Monitor `/api/health` endpoint
   - Set up alerts for downtime

2. **Error Tracking**
   - Implement Sentry.io for error tracking
   - Monitor application logs
   - Set up error rate alerts

3. **Performance Monitoring**
   - Monitor response times
   - Track database query performance
   - Monitor resource usage

### 2. Backup Strategy

#### Database Backups
```bash
# Automated backups (usually provided by hosting platform)
# Manual backup example for PostgreSQL:
pg_dump $DATABASE_URL > backup_$(date +%Y%m%d_%H%M%S).sql

# Restore from backup:
psql $DATABASE_URL < backup_file.sql
```

#### Application Backups
- Code: Stored in Git repository
- Environment variables: Document in secure location
- Database: Regular automated backups
- User uploads: Cloud storage with versioning

### 3. Security Maintenance

#### Regular Security Tasks
- Update dependencies monthly
- Rotate API keys quarterly
- Review access logs weekly
- Update TLS certificates (automatic with most platforms)

#### Security Monitoring
```bash
# Check for vulnerabilities
npm audit                # Frontend dependencies
safety check            # Backend dependencies
bandit -r backend/      # Python security scan
```

## 🔧 Troubleshooting

### Common Issues

#### 1. Database Connection Issues
```bash
# Check database connectivity
python -c "
import psycopg2
conn = psycopg2.connect('your_database_url')
print('Database connection successful')
conn.close()
"
```

**Solutions:**
- Verify database URL format
- Check network connectivity
- Ensure database service is running
- Verify credentials

#### 2. Environment Variable Issues
```bash
# Check environment variables
echo $FLASK_ENV
echo $GEMINI_API_KEY

# In Python application:
import os
print(f"FLASK_ENV: {os.getenv('FLASK_ENV')}")
```

**Solutions:**
- Verify all required environment variables are set
- Check for typos in variable names
- Ensure variables are properly escaped
- Restart application after changes

#### 3. Frontend API Connection Issues
```bash
# Check CORS configuration
curl -H "Origin: https://your-frontend-domain.com" \
     -H "Access-Control-Request-Method: POST" \
     -H "Access-Control-Request-Headers: X-Requested-With" \
     -X OPTIONS \
     https://your-backend-url.com/api/health
```

**Solutions:**
- Verify API URL in frontend environment variables
- Check CORS configuration in backend
- Ensure HTTPS is properly configured
- Verify network connectivity

#### 4. Build Failures

**Backend Build Issues:**
```bash
# Check Python version
python --version

# Install dependencies manually
pip install -r requirements.txt

# Check for missing system dependencies
apt-get update && apt-get install -y build-essential libpq-dev
```

**Frontend Build Issues:**
```bash
# Check Node.js version
node --version
npm --version

# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install

# Check memory limits
NODE_OPTIONS="--max-old-space-size=4096" npm run build
```

### Performance Issues

#### 1. Slow Database Queries
```sql
-- Check slow queries (PostgreSQL)
SELECT query, mean_time, calls
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

-- Add indexes for frequently queried columns
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_diet_plans_user_id ON diet_plans(user_id);
```

#### 2. High Response Times
```bash
# Check application metrics
curl https://your-backend-url.com/api/performance

# Monitor resource usage
top -p $(pgrep -f "gunicorn")
```

#### 3. Memory Issues
```bash
# Check memory usage
free -h
docker stats  # For Docker deployments

# Optimize Python memory usage
PYTHONOPTIMIZE=1 python app.py
```

### Getting Help

#### Support Resources
- **Platform Documentation**: Check your hosting platform's docs
- **Community Support**: GitHub Issues, Stack Overflow
- **Application Logs**: Always check application logs first
- **Health Endpoints**: Use built-in health checks

#### Log Analysis
```bash
# Check application logs
# Render: View in dashboard
# Railway: railway logs
# Heroku: heroku logs --tail --app your-app-name
# Docker: docker-compose logs -f

# Common log patterns to look for:
grep "ERROR" logs/app.log
grep "WARNING" logs/app.log
grep "Database" logs/app.log
```

## 🎉 Conclusion

This deployment guide provides comprehensive instructions for deploying the Diet Planner application to multiple platforms. Choose the platform that best fits your needs:

- **Render.com**: Best for beginners and simple deployments
- **Railway.app**: Great developer experience with modern tooling
- **Vercel**: Excellent for frontend-focused applications
- **Docker**: Maximum flexibility and control
- **Heroku**: Traditional PaaS with extensive documentation

Remember to:
1. Always test in staging before production
2. Set up monitoring and alerts
3. Keep backups of your data
4. Update dependencies regularly
5. Monitor application performance

Your Diet Planner application is now ready for production use!
