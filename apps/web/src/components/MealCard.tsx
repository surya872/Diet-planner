import React from 'react';
import { Meal } from '../types';
// Removed unused imports

interface MealCardProps {
  meal: Meal;
}

const MealCard: React.FC<MealCardProps> = ({ meal }) => {
  const getMealIcon = (mealType: string) => {
    switch (mealType.toLowerCase()) {
      case 'breakfast':
        return '🌅';
      case 'lunch':
        return '🌞';
      case 'dinner':
        return '🌙';
      case 'snack':
        return '🍎';
      default:
        return '🍽️';
    }
  };

  const getMealColor = (mealType: string) => {
    switch (mealType.toLowerCase()) {
      case 'breakfast':
        return 'bg-orange-50 border-orange-200';
      case 'lunch':
        return 'bg-yellow-50 border-yellow-200';
      case 'dinner':
        return 'bg-blue-50 border-blue-200';
      case 'snack':
        return 'bg-green-50 border-green-200';
      default:
        return 'bg-gray-50 border-gray-200';
    }
  };

  return (
    <div className={`border rounded-lg p-4 ${getMealColor(meal.meal_type)}`}>
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-2">
          <span className="text-2xl">{getMealIcon(meal.meal_type)}</span>
          <div>
            <h3 className="font-semibold text-gray-900 capitalize">
              {meal.meal_type}
            </h3>
            <p className="text-sm text-gray-600">{meal.meal_name}</p>
          </div>
        </div>
        <div className="text-right">
          <div className="text-lg font-bold text-gray-900">
            {meal.total_calories} cal
          </div>
          <div className="text-xs text-gray-500">Total</div>
        </div>
      </div>

      {/* Food Items */}
      <div className="space-y-3 mb-4">
        {meal.foods.map((food, index) => (
          <div key={index} className="flex items-center justify-between p-2 bg-white rounded border">
            <div className="flex-1">
              <div className="font-medium text-gray-900">{food.name}</div>
              <div className="text-sm text-gray-500">{food.portion}</div>
            </div>
            <div className="text-right">
              <div className="font-medium text-gray-900">{food.calories} cal</div>
              <div className="text-xs text-gray-500">
                P: {food.protein}g | C: {food.carbs}g | F: {food.fat}g
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Nutrition Summary */}
      <div className="grid grid-cols-3 gap-2 pt-3 border-t border-gray-200">
        <div className="text-center">
          <div className="text-sm font-medium text-gray-900">{meal.total_protein}g</div>
          <div className="text-xs text-gray-500">Protein</div>
        </div>
        <div className="text-center">
          <div className="text-sm font-medium text-gray-900">{meal.total_carbs}g</div>
          <div className="text-xs text-gray-500">Carbs</div>
        </div>
        <div className="text-center">
          <div className="text-sm font-medium text-gray-900">{meal.total_fat}g</div>
          <div className="text-xs text-gray-500">Fat</div>
        </div>
      </div>
    </div>
  );
};

export default MealCard;
