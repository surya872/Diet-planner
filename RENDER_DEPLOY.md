# 🚀 Render Deployment Fix

## Issue Resolution

The error occurs because Render is expecting specific configuration. Here's the correct setup:

## ✅ Render Dashboard Configuration

### 1. Service Configuration
```
Service Type: Web Service
Environment: Docker
Branch: Deploy (or main)
Root Directory: . (leave empty for root)
```

### 2. Build & Deploy Settings
```
Build Command: (leave empty - Docker handles this)
Start Command: (leave empty - Docker handles this)
```

### 3. Environment Variables (CRITICAL)
```bash
# Add these in Render Dashboard > Environment tab:
APP_ENV=production
FLASK_SECRET_KEY=[Click "Generate" button]
JWT_SECRET_KEY=[Click "Generate" button]  
GEMINI_API_KEY=[Your Gemini API key from Google AI Studio]
PORT=10000
PYTHONPATH=/app
```

### 4. Database Setup
1. Create PostgreSQL database in Render
2. Copy the **Internal Database URL**
3. Add as environment variable:
```bash
DATABASE_URL=[Internal database URL from Render]
```

## 🔧 Alternative: Python Environment

If you prefer Python environment instead of Docker:

### Change Environment to Python:
```
Environment: Python 3
Build Command: cd backend && pip install -r requirements.txt
Start Command: cd backend && ./start-render.sh
Root Directory: . (leave empty)
```

## 🚀 Quick Fix Steps:

1. **Push the new Dockerfile to GitHub**:
   ```bash
   git add Dockerfile backend/start-render.sh
   git commit -m "Add Render deployment files"
   git push origin Deploy
   ```

2. **In Render Dashboard**:
   - Go to your service settings
   - Trigger manual deploy or wait for auto-deploy
   - Check logs for any errors

3. **Monitor Deployment**:
   - Watch the build logs
   - Ensure all environment variables are set
   - Test the health endpoint once deployed

## 🎯 Expected Result:

Your service should deploy successfully and be available at:
```
https://diet-planner-api.onrender.com/api/health
```

## 🔍 Troubleshooting:

If still having issues:
1. Check Render build logs for specific errors
2. Verify all environment variables are set
3. Ensure your Gemini API key is valid
4. Test database connection in logs
