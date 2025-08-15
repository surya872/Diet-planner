import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Header from './components/Header';
import Login from './components/Login';
import UserForm from './components/UserForm';
import DietPlanView from './components/DietPlanView';
import Profile from './components/Profile';
import LoadingSpinner from './components/LoadingSpinner';
import { User, DietPlan, UserFormData } from './types';
import { 
  register, 
  login, 
  generateDietPlan, 
  getProfile,
  updateProfile,
  setAuthToken,
  removeAuthToken,
  getAuthToken 
} from './services/api';

function App() {
  const [user, setUser] = useState<User | null>(null);
  const [currentDietPlan, setCurrentDietPlan] = useState<DietPlan | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isLogin, setIsLogin] = useState(true);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [initialLoading, setInitialLoading] = useState(true);

  // Check for existing authentication on app start
  useEffect(() => {
    const checkAuthentication = async () => {
      const token = getAuthToken();
      if (token) {
        try {
          const response = await getProfile();
          setUser(response.data);
          setIsAuthenticated(true);
        } catch (error) {
          // Token might be expired or invalid
          removeAuthToken();
          setIsAuthenticated(false);
        }
      }
      setInitialLoading(false);
    };

    checkAuthentication();
  }, []);

  const handleLogin = async (email: string, password: string) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await login(email, password);
      setAuthToken(response.data.access_token);
      setUser(response.data.user);
      setIsAuthenticated(true);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async (userData: UserFormData & { password: string }) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await register(userData);
      setAuthToken(response.data.access_token);
      setUser(response.data.user);
      setIsAuthenticated(true);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  const handleGenerateDietPlan = async () => {
    if (!user) return;
    
    setLoading(true);
    setError(null);
    
    try {
      const response = await generateDietPlan();
      const newDietPlan = response.data;
      setCurrentDietPlan(newDietPlan);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to generate diet plan');
    } finally {
      setLoading(false);
    }
  };

  const handleProfileUpdate = async (data: Partial<UserFormData> & { password?: string }) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await updateProfile(data);
      setUser(response.data.user);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to update profile');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = () => {
    setUser(null);
    setCurrentDietPlan(null);
    setIsAuthenticated(false);
    removeAuthToken();
  };

  const switchToLogin = () => {
    setIsLogin(true);
    setError(null);
  };

  const switchToRegister = () => {
    setIsLogin(false);
    setError(null);
  };

  if (initialLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <LoadingSpinner />
      </div>
    );
  }

  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        <Header user={user} onLogout={handleLogout} />
        
        <main className="container mx-auto px-4 py-8">
          <Routes>
            <Route 
              path="/" 
              element={
                isAuthenticated && user ? (
                  <DietPlanView 
                    user={user}
                    dietPlan={currentDietPlan}
                    onGeneratePlan={handleGenerateDietPlan}
                    error={error}
                    loading={loading}
                  />
                ) : (
                  <div className="max-w-md mx-auto">
                    {isLogin ? (
                      <Login 
                        onSubmit={handleLogin}
                        onSwitchToRegister={switchToRegister}
                        error={error}
                        loading={loading}
                      />
                    ) : (
                      <UserForm 
                        onSubmit={handleRegister}
                        onSwitchToLogin={switchToLogin}
                        error={error}
                        loading={loading}
                      />
                    )}
                  </div>
                )
              } 
            />
            <Route 
              path="/profile" 
              element={
                isAuthenticated && user ? (
                  <Profile 
                    user={user}
                    onUpdate={handleProfileUpdate}
                    error={error}
                    loading={loading}
                  />
                ) : (
                  <Navigate to="/" replace />
                )
              } 
            />
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;