import React from 'react';
import { User, DietPlan } from '../types';
import MealCard from './MealCard';
import NutritionSummary from './NutritionSummary';
import LoadingSpinner from './LoadingSpinner';

interface DietPlanViewProps {
  user: User;
  dietPlan: DietPlan | null;
  onGeneratePlan: () => void;
  error: string | null;
  loading?: boolean;
}

const DietPlanView: React.FC<DietPlanViewProps> = ({ 
  user, 
  dietPlan, 
  onGeneratePlan, 
  error,
  loading = false
}) => {
  // Show full loading screen when loading and no diet plan exists
  if (loading && !dietPlan) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="card text-center">
          <div className="py-12">
            <LoadingSpinner />
            <h2 className="text-2xl font-bold text-gray-900 mt-6 mb-4">
              Generating Your Diet Plan
            </h2>
            <p className="text-gray-600 max-w-md mx-auto">
              Our AI is creating a personalized 1-week meal plan based on your preferences, health goals, and nutritional needs. This may take a moment...
            </p>
          </div>
        </div>
      </div>
    );
  }

  if (!dietPlan) {
    return (
      <div className="max-w-4xl mx-auto">
        <div className="card text-center">
          <div className="mb-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Welcome back, {user.name}!
            </h2>
            <p className="text-gray-600 mb-8">
              Ready to get your personalized 1-week diet plan? Our AI will create a meal plan 
              tailored to your preferences and health goals.
            </p>
            
            {error && (
              <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
                <p className="text-red-600">{error}</p>
              </div>
            )}
            
            <button
              onClick={onGeneratePlan}
              disabled={loading}
              className="btn-primary text-lg py-3 px-8 disabled:opacity-50 disabled:cursor-not-allowed relative"
            >
              {loading ? (
                <div className="flex items-center space-x-2">
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  <span>Generating Plan...</span>
                </div>
              ) : (
                'Generate My Diet Plan'
              )}
            </button>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-left">
            <div className="text-center">
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🎯</span>
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">Personalized</h3>
              <p className="text-sm text-gray-600">
                Tailored to your age, weight, activity level, and diet preferences
              </p>
            </div>
            
            <div className="text-center">
              <div className="w-16 h-16 bg-success-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">🤖</span>
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">AI-Powered</h3>
              <p className="text-sm text-gray-600">
                Generated using advanced AI to ensure nutritional balance
              </p>
            </div>
            
            <div className="text-center">
              <div className="w-16 h-16 bg-yellow-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-2xl">📅</span>
              </div>
              <h3 className="font-semibold text-gray-900 mb-2">7-Day Plan</h3>
              <p className="text-sm text-gray-600">
                Complete week of meals with breakfast, lunch, dinner, and snacks
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto">
      {/* Header */}
      <div className="card mb-8">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">
              {dietPlan.plan_name}
            </h1>
            <p className="text-gray-600">
              {new Date(dietPlan.start_date).toLocaleDateString()} - {new Date(dietPlan.end_date).toLocaleDateString()}
            </p>
          </div>
          <button
            onClick={onGeneratePlan}
            disabled={loading}
            className="btn-primary mt-4 md:mt-0 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {loading ? (
              <div className="flex items-center space-x-2">
                <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                <span>Generating...</span>
              </div>
            ) : (
              'Generate New Plan'
            )}
          </button>
        </div>
      </div>

      {/* Nutrition Summary */}
      <div className="mb-8">
        <NutritionSummary 
          totalCalories={dietPlan.total_calories}
          planData={dietPlan.plan_data}
        />
      </div>

      {/* Daily Plans */}
      <div className="space-y-8">
        {dietPlan.plan_data.daily_plans.map((dailyPlan, dayIndex) => (
          <div key={dayIndex} className="card">
            <div className="mb-6">
              <h2 className="text-2xl font-bold text-gray-900 mb-2">
                {dailyPlan.day}
              </h2>
              <p className="text-gray-600">
                {new Date(dailyPlan.date).toLocaleDateString('en-US', { 
                  weekday: 'long', 
                  year: 'numeric', 
                  month: 'long', 
                  day: 'numeric' 
                })}
              </p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              {dailyPlan.meals.map((meal, mealIndex) => (
                <MealCard key={mealIndex} meal={meal} />
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default DietPlanView;
