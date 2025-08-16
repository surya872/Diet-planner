# 🚀 Deployment Guide: Render + Netlify

## Overview
This guide deploys your Diet Planner application using:
- **Backend**: Render (Flask API + PostgreSQL)
- **Frontend**: Netlify (React SPA)

## 📋 Prerequisites

1. **GitHub Repository**: Push your code to GitHub
2. **Render Account**: Create account at render.com
3. **Netlify Account**: Create account at netlify.com
4. **Gemini API Key**: Get from Google AI Studio

## 🎯 Phase 1: Deploy Backend to Render

### Step 1: Create Render Service

1. **Connect GitHub**:
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

2. **Configure Service**:
   ```
   Name: diet-planner-api
   Environment: Python
   Branch: main
   Root Directory: backend
   Build Command: pip install -r requirements.txt
   Start Command: ./start-render.sh
   ```

3. **Set Environment Variables**:
   ```bash
   APP_ENV=production
   FLASK_SECRET_KEY=[Auto-generate]
   JWT_SECRET_KEY=[Auto-generate]
   GEMINI_API_KEY=[Your Gemini API key]
   CORS_ORIGINS=https://diet-planner.netlify.app
   ```

### Step 2: Create PostgreSQL Database

1. **New Database**:
   - Click "New +" → "PostgreSQL"
   - Name: `diet-planner-db`
   - Plan: Free tier

2. **Connect to Backend**:
   - Copy connection string
   - Add as `DATABASE_URL` environment variable

### Step 3: Test Backend

```bash
# Your backend will be available at:
https://diet-planner-api.onrender.com

# Test health endpoint:
curl https://diet-planner-api.onrender.com/api/health
```

## 🎯 Phase 2: Deploy Frontend to Netlify

### Step 1: Configure Frontend

1. **Update Environment**:
   ```bash
   # In frontend/env.production
   REACT_APP_API_URL=https://diet-planner-api.onrender.com/api
   ```

### Step 2: Deploy to Netlify

1. **Connect GitHub**:
   - Go to [netlify.com](https://netlify.com)
   - Click "New site from Git"
   - Connect your GitHub repository

2. **Configure Build**:
   ```
   Base directory: frontend
   Build command: npm run build
   Publish directory: frontend/build
   ```

3. **Set Environment Variables**:
   ```bash
   REACT_APP_API_URL=https://diet-planner-api.onrender.com/api
   NODE_VERSION=18
   ```

### Step 3: Configure Custom Domain (Optional)

1. **Netlify Domain**:
   - Go to Site settings → Domain management
   - Change site name to: `diet-planner`
   - URL becomes: `https://diet-planner.netlify.app`

2. **Update Backend CORS**:
   ```bash
   # In Render dashboard, update CORS_ORIGINS:
   CORS_ORIGINS=https://diet-planner.netlify.app
   ```

## 🎯 Phase 3: Test Complete Application

### Test Registration Flow

1. **Frontend**: https://diet-planner.netlify.app
2. **Register new user**
3. **Login**
4. **Generate diet plan**
5. **Check all features work**

### Monitor Logs

1. **Render Logs**: View in Render dashboard
2. **Netlify Logs**: View in Netlify dashboard
3. **Check browser console** for any errors

## 🔧 Environment Variables Summary

### Render (Backend)
```bash
APP_ENV=production
FLASK_SECRET_KEY=[auto-generated]
JWT_SECRET_KEY=[auto-generated] 
GEMINI_API_KEY=[your-key]
DATABASE_URL=[auto-set by Render]
CORS_ORIGINS=https://diet-planner.netlify.app
```

### Netlify (Frontend)
```bash
REACT_APP_API_URL=https://diet-planner-api.onrender.com/api
NODE_VERSION=18
```

## 🚨 Troubleshooting

### Backend Issues
- Check Render logs for Python errors
- Verify all environment variables are set
- Test database connection

### Frontend Issues  
- Check browser console for errors
- Verify REACT_APP_API_URL is correct
- Test API endpoints directly

### CORS Issues
- Ensure CORS_ORIGINS includes your Netlify URL
- Check for typos in domain names
- Verify both HTTP and HTTPS versions if needed

## 🎉 Success!

Your Diet Planner application is now deployed with:
- ✅ Enterprise security features
- ✅ Production-ready infrastructure  
- ✅ Automatic SSL certificates
- ✅ CDN optimization
- ✅ Database persistence

**Live URLs**:
- Frontend: https://diet-planner.netlify.app
- Backend: https://diet-planner-api.onrender.com
- API Health: https://diet-planner-api.onrender.com/api/health
