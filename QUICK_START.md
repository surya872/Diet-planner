# Quick Start Guide

## 🚀 Start Your Diet Planner Application

### **Step 1: Get Your Gemini API Key**
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in and create a new API key
3. Copy the key

### **Step 2: Configure Environment**
```bash
# Edit the .env file
nano .env
```

Add your Gemini API key:
```env
GEMINI_API_KEY=your_actual_api_key_here
```

### **Step 3: Start the Application**

#### **Option A: Simple Start (Recommended)**
```bash
./start_simple.sh
```
This opens two terminal windows - one for backend, one for frontend.

#### **Option B: Manual Start**
**Terminal 1 (Backend):**
```bash
cd backend
source venv/bin/activate
python app.py
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm start
```

### **Step 4: Access the Application**
- **Frontend**: http://localhost:3001
- **Backend API**: http://localhost:5001
- **Health Check**: http://localhost:5001/api/health

## 🛠️ Troubleshooting

### **Port 5000 Already in Use**
✅ **Fixed!** Backend now runs on port 5001 to avoid macOS AirPlay conflicts.

### **Database Issues**
```bash
./setup_database.sh
```

### **Backend Issues**
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

### **Frontend Issues**
```bash
cd frontend
npm install
npm start
```

## 📋 Available Commands

```bash
# Start application
./start_simple.sh

# Database management
./manage_database.sh

# Database setup
./setup_database.sh

# View database
psql -U diet_user -d diet_planner
```

## 🎯 What You Can Do

1. **Register**: Fill out the user form with your details
2. **Generate Diet Plan**: Get AI-powered 1-week meal plans
3. **View Nutrition**: See detailed nutritional information
4. **Track Meals**: Log your daily food consumption

## 🍎 Features

- ✅ AI-powered diet plan generation
- ✅ Personalized meal recommendations
- ✅ Nutritional analysis
- ✅ Multiple diet preferences
- ✅ Beautiful, responsive UI
- ✅ User data persistence

Happy diet planning! 🎉
