import React, { useState } from 'react';
import { User, Edit3, Save, X } from 'lucide-react';
import { UserFormData } from '../types';

interface ProfileProps {
  user: any;
  onUpdate: (data: Partial<UserFormData> & { password?: string }) => void;
  error: string | null;
  loading: boolean;
}

const Profile: React.FC<ProfileProps> = ({ user, onUpdate, error, loading }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    name: user?.name || '',
    email: user?.email || '',
    age: user?.age || 25,
    gender: user?.gender || 'male',
    weight: user?.weight || 70,
    height: user?.height || 170,
    activity_level: user?.activity_level || 'moderate',
    diet_preference: user?.diet_preference || 'balanced',
    health_goals: user?.health_goals || '',
    password: ''
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'age' || name === 'weight' || name === 'height' ? Number(value) : value
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    // Remove password if empty
    const { password, ...baseData } = formData;
    const updateData = password ? { ...baseData, password } : baseData;
    
    onUpdate(updateData);
    setIsEditing(false);
  };

  const handleCancel = () => {
    setFormData({
      name: user?.name || '',
      email: user?.email || '',
      age: user?.age || 25,
      gender: user?.gender || 'male',
      weight: user?.weight || 70,
      height: user?.height || 170,
      activity_level: user?.activity_level || 'moderate',
      diet_preference: user?.diet_preference || 'balanced',
      health_goals: user?.health_goals || '',
      password: ''
    });
    setIsEditing(false);
  };

  if (!user) return null;

  return (
    <div className="max-w-2xl mx-auto">
      <div className="card">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-3">
            <div className="bg-primary-100 p-3 rounded-full">
              <User className="h-6 w-6 text-primary-600" />
            </div>
            <div>
              <h2 className="text-2xl font-bold text-gray-900">Profile</h2>
              <p className="text-gray-600">Manage your personal information</p>
            </div>
          </div>
          {!isEditing && (
            <button
              onClick={() => setIsEditing(true)}
              className="btn-secondary flex items-center space-x-2"
            >
              <Edit3 className="h-4 w-4" />
              <span>Edit Profile</span>
            </button>
          )}
        </div>

        {error && (
          <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
            <p className="text-red-600">{error}</p>
          </div>
        )}

        {isEditing ? (
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Name */}
              <div>
                <label htmlFor="name" className="block text-sm font-medium text-gray-700 mb-2">
                  Full Name *
                </label>
                <input
                  type="text"
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  required
                  className="input-field"
                />
              </div>

              {/* Email */}
              <div>
                <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-2">
                  Email Address *
                </label>
                <input
                  type="email"
                  id="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  required
                  className="input-field"
                />
              </div>

              {/* Age */}
              <div>
                <label htmlFor="age" className="block text-sm font-medium text-gray-700 mb-2">
                  Age *
                </label>
                <input
                  type="number"
                  id="age"
                  name="age"
                  value={formData.age}
                  onChange={handleChange}
                  required
                  min="1"
                  max="120"
                  className="input-field"
                />
              </div>

              {/* Gender */}
              <div>
                <label htmlFor="gender" className="block text-sm font-medium text-gray-700 mb-2">
                  Gender *
                </label>
                <select
                  id="gender"
                  name="gender"
                  value={formData.gender}
                  onChange={handleChange}
                  required
                  className="input-field"
                >
                  <option value="male">Male</option>
                  <option value="female">Female</option>
                  <option value="other">Other</option>
                </select>
              </div>

              {/* Weight */}
              <div>
                <label htmlFor="weight" className="block text-sm font-medium text-gray-700 mb-2">
                  Weight (kg) *
                </label>
                <input
                  type="number"
                  id="weight"
                  name="weight"
                  value={formData.weight}
                  onChange={handleChange}
                  required
                  min="20"
                  max="300"
                  step="0.1"
                  className="input-field"
                />
              </div>

              {/* Height */}
              <div>
                <label htmlFor="height" className="block text-sm font-medium text-gray-700 mb-2">
                  Height (cm)
                </label>
                <input
                  type="number"
                  id="height"
                  name="height"
                  value={formData.height}
                  onChange={handleChange}
                  min="100"
                  max="250"
                  className="input-field"
                />
              </div>

              {/* Activity Level */}
              <div>
                <label htmlFor="activity_level" className="block text-sm font-medium text-gray-700 mb-2">
                  Activity Level
                </label>
                <select
                  id="activity_level"
                  name="activity_level"
                  value={formData.activity_level}
                  onChange={handleChange}
                  className="input-field"
                >
                  <option value="sedentary">Sedentary (little/no exercise)</option>
                  <option value="light">Lightly active (light exercise 1-3 days/week)</option>
                  <option value="moderate">Moderately active (moderate exercise 3-5 days/week)</option>
                  <option value="active">Very active (hard exercise 6-7 days/week)</option>
                  <option value="very_active">Super active (very hard exercise & physical job)</option>
                </select>
              </div>

              {/* Diet Preference */}
              <div>
                <label htmlFor="diet_preference" className="block text-sm font-medium text-gray-700 mb-2">
                  Diet Preference
                </label>
                <select
                  id="diet_preference"
                  name="diet_preference"
                  value={formData.diet_preference}
                  onChange={handleChange}
                  className="input-field"
                >
                  <option value="balanced">Balanced</option>
                  <option value="vegetarian">Vegetarian</option>
                  <option value="vegan">Vegan</option>
                  <option value="keto">Ketogenic</option>
                  <option value="paleo">Paleo</option>
                  <option value="mediterranean">Mediterranean</option>
                  <option value="low_carb">Low Carb</option>
                  <option value="high_protein">High Protein</option>
                </select>
              </div>
            </div>

            {/* Health Goals */}
            <div>
              <label htmlFor="health_goals" className="block text-sm font-medium text-gray-700 mb-2">
                Health Goals
              </label>
              <textarea
                id="health_goals"
                name="health_goals"
                value={formData.health_goals}
                onChange={handleChange}
                rows={3}
                className="input-field"
                placeholder="e.g., Weight loss, muscle gain, maintain health, etc."
              />
            </div>

            {/* Password */}
            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700 mb-2">
                New Password (leave blank to keep current)
              </label>
              <input
                type="password"
                id="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                className="input-field"
                placeholder="Enter new password"
              />
            </div>

            <div className="flex justify-end space-x-4 pt-4">
              <button
                type="button"
                onClick={handleCancel}
                className="btn-secondary flex items-center space-x-2"
              >
                <X className="h-4 w-4" />
                <span>Cancel</span>
              </button>
              <button
                type="submit"
                disabled={loading}
                className="btn-primary flex items-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Save className="h-4 w-4" />
                <span>{loading ? 'Saving...' : 'Save Changes'}</span>
              </button>
            </div>
          </form>
        ) : (
          <div className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div>
                <h3 className="text-sm font-medium text-gray-500">Name</h3>
                <p className="mt-1 text-lg text-gray-900">{user.name}</p>
              </div>
              <div>
                <h3 className="text-sm font-medium text-gray-500">Email</h3>
                <p className="mt-1 text-lg text-gray-900">{user.email}</p>
              </div>
              <div>
                <h3 className="text-sm font-medium text-gray-500">Age</h3>
                <p className="mt-1 text-lg text-gray-900">{user.age} years</p>
              </div>
              <div>
                <h3 className="text-sm font-medium text-gray-500">Gender</h3>
                <p className="mt-1 text-lg text-gray-900 capitalize">{user.gender}</p>
              </div>
              <div>
                <h3 className="text-sm font-medium text-gray-500">Weight</h3>
                <p className="mt-1 text-lg text-gray-900">{user.weight} kg</p>
              </div>
              <div>
                <h3 className="text-sm font-medium text-gray-500">Height</h3>
                <p className="mt-1 text-lg text-gray-900">{user.height ? `${user.height} cm` : 'Not specified'}</p>
              </div>
              <div>
                <h3 className="text-sm font-medium text-gray-500">Activity Level</h3>
                <p className="mt-1 text-lg text-gray-900 capitalize">{user.activity_level?.replace('_', ' ')}</p>
              </div>
              <div>
                <h3 className="text-sm font-medium text-gray-500">Diet Preference</h3>
                <p className="mt-1 text-lg text-gray-900 capitalize">{user.diet_preference?.replace('_', ' ')}</p>
              </div>
            </div>
            {user.health_goals && (
              <div>
                <h3 className="text-sm font-medium text-gray-500">Health Goals</h3>
                <p className="mt-1 text-lg text-gray-900">{user.health_goals}</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default Profile;
