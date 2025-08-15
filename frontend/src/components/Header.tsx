import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Apple, LogOut, User, Settings } from 'lucide-react';
import { User as UserType } from '../types';

interface HeaderProps {
  user: UserType | null;
  onLogout: () => void;
}

const Header: React.FC<HeaderProps> = ({ user, onLogout }) => {
  const location = useLocation();

  return (
    <header className="bg-white shadow-sm border-b border-gray-200">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <Link to="/" className="flex items-center space-x-3 hover:opacity-80 transition-opacity">
            <div className="flex items-center justify-center w-10 h-10 bg-primary-600 rounded-lg">
              <Apple className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-gray-900">Diet Planner</h1>
              <p className="text-sm text-gray-600">AI-Powered Meal Planning</p>
            </div>
          </Link>
          
          {user && (
            <div className="flex items-center space-x-4">
              <nav className="flex items-center space-x-4">
                <Link
                  to="/"
                  className={`text-sm font-medium transition-colors ${
                    location.pathname === '/' 
                      ? 'text-primary-600' 
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  Diet Plans
                </Link>
                <Link
                  to="/profile"
                  className={`flex items-center space-x-2 text-sm font-medium transition-colors ${
                    location.pathname === '/profile' 
                      ? 'text-primary-600' 
                      : 'text-gray-600 hover:text-gray-900'
                  }`}
                >
                  <Settings className="w-4 h-4" />
                  <span>Profile</span>
                </Link>
              </nav>
              
              <div className="h-6 w-px bg-gray-300"></div>
              
              <div className="flex items-center space-x-2 text-sm text-gray-600">
                <User className="w-4 h-4" />
                <span>{user.name}</span>
              </div>
              
              <button
                onClick={onLogout}
                className="flex items-center space-x-2 text-gray-600 hover:text-gray-900 transition-colors"
              >
                <LogOut className="w-4 h-4" />
                <span>Logout</span>
              </button>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;
