import React from 'react';
import { DietPlanData } from '../types';
import { Target, Zap, Scale } from 'lucide-react';

interface NutritionSummaryProps {
  totalCalories: number;
  planData: DietPlanData;
}

const NutritionSummary: React.FC<NutritionSummaryProps> = ({ totalCalories, planData }) => {
  // Calculate average daily nutrition
  const calculateAverages = () => {
    if (!planData.daily_plans || planData.daily_plans.length === 0) {
      return { protein: 0, carbs: 0, fat: 0 };
    }

    let totalProtein = 0;
    let totalCarbs = 0;
    let totalFat = 0;
    let dayCount = 0;

    planData.daily_plans.forEach(day => {
      day.meals.forEach(meal => {
        totalProtein += meal.total_protein;
        totalCarbs += meal.total_carbs;
        totalFat += meal.total_fat;
      });
      dayCount++;
    });

    return {
      protein: Math.round(totalProtein / dayCount),
      carbs: Math.round(totalCarbs / dayCount),
      fat: Math.round(totalFat / dayCount)
    };
  };

  const averages = calculateAverages();

  return (
    <div className="card">
      <h2 className="text-xl font-bold text-gray-900 mb-6">Nutrition Summary</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        {/* Daily Calories */}
        <div className="text-center p-4 bg-primary-50 rounded-lg">
          <div className="flex items-center justify-center w-12 h-12 bg-primary-100 rounded-full mx-auto mb-3">
            <Target className="w-6 h-6 text-primary-600" />
          </div>
          <div className="text-2xl font-bold text-gray-900">{totalCalories}</div>
          <div className="text-sm text-gray-600">Daily Calories</div>
        </div>

        {/* Average Protein */}
        <div className="text-center p-4 bg-blue-50 rounded-lg">
          <div className="flex items-center justify-center w-12 h-12 bg-blue-100 rounded-full mx-auto mb-3">
            <Scale className="w-6 h-6 text-blue-600" />
          </div>
          <div className="text-2xl font-bold text-gray-900">{averages.protein}g</div>
          <div className="text-sm text-gray-600">Avg Protein</div>
        </div>

        {/* Average Carbs */}
        <div className="text-center p-4 bg-yellow-50 rounded-lg">
          <div className="flex items-center justify-center w-12 h-12 bg-yellow-100 rounded-full mx-auto mb-3">
            <Zap className="w-6 h-6 text-yellow-600" />
          </div>
          <div className="text-2xl font-bold text-gray-900">{averages.carbs}g</div>
          <div className="text-sm text-gray-600">Avg Carbs</div>
        </div>

        {/* Average Fat */}
        <div className="text-center p-4 bg-green-50 rounded-lg">
          <div className="flex items-center justify-center w-12 h-12 bg-green-100 rounded-full mx-auto mb-3">
            <Scale className="w-6 h-6 text-green-600" />
          </div>
          <div className="text-2xl font-bold text-gray-900">{averages.fat}g</div>
          <div className="text-sm text-gray-600">Avg Fat</div>
        </div>
      </div>

      {/* Macro Distribution */}
      <div className="mt-6 pt-6 border-t border-gray-200">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Macro Distribution</h3>
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-gray-700">Protein</span>
            <div className="flex items-center space-x-2">
              <div className="w-32 bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-blue-500 h-2 rounded-full" 
                  style={{ width: `${(averages.protein * 4 / totalCalories) * 100}%` }}
                ></div>
              </div>
              <span className="text-sm text-gray-600 w-12 text-right">
                {Math.round((averages.protein * 4 / totalCalories) * 100)}%
              </span>
            </div>
          </div>
          
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-gray-700">Carbohydrates</span>
            <div className="flex items-center space-x-2">
              <div className="w-32 bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-yellow-500 h-2 rounded-full" 
                  style={{ width: `${(averages.carbs * 4 / totalCalories) * 100}%` }}
                ></div>
              </div>
              <span className="text-sm text-gray-600 w-12 text-right">
                {Math.round((averages.carbs * 4 / totalCalories) * 100)}%
              </span>
            </div>
          </div>
          
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-gray-700">Fat</span>
            <div className="flex items-center space-x-2">
              <div className="w-32 bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-green-500 h-2 rounded-full" 
                  style={{ width: `${(averages.fat * 9 / totalCalories) * 100}%` }}
                ></div>
              </div>
              <span className="text-sm text-gray-600 w-12 text-right">
                {Math.round((averages.fat * 9 / totalCalories) * 100)}%
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default NutritionSummary;
