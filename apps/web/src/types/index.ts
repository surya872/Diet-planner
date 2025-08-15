export interface User {
  id: number;
  name: string;
  email: string;
  age: number;
  gender: string;
  weight: number;
  height?: number;
  activity_level?: string;
  diet_preference?: string;
  health_goals?: string;
  created_at: string;
  updated_at: string;
}

export interface Food {
  name: string;
  portion: string;
  calories: number;
  protein: number;
  carbs: number;
  fat: number;
}

export interface Meal {
  meal_type: string;
  meal_name: string;
  foods: Food[];
  total_calories: number;
  total_protein: number;
  total_carbs: number;
  total_fat: number;
}

export interface DailyPlan {
  day: string;
  date: string;
  meals: Meal[];
}

export interface DietPlanData {
  total_calories_per_day: number;
  daily_plans: DailyPlan[];
}

export interface DietPlan {
  id: number;
  user_id: number;
  plan_name: string;
  start_date: string;
  end_date: string;
  total_calories: number;
  plan_data: DietPlanData;
  created_at: string;
  updated_at: string;
}

export interface UserFormData {
  name: string;
  email: string;
  age: number;
  gender: string;
  weight: number;
  height?: number;
  activity_level?: string;
  diet_preference?: string;
  health_goals?: string;
}
