export interface FileAttachment {
  filename: string;
  url: string;
  id: number;
}

interface User {
  first_name: string;
  last_name: string;
  email: string;
  last_login: string;
  username: string;
}
export interface Staff {
  id: number;
  gender: string;
  age: number;
  contact_one: string;
  nationality: string;
  img: string | FileAttachment;
  specialization: string;
  years_of_experience: string;
  languages: string[];
  bio: string | null;
}

export interface StaffTwo extends Staff {
  user: string;
}

export interface Client {
  id: number;
  gender: string;
  age: number;
  address: string | null;
  contact_one: string;
  nationality: string;
  img: string | FileAttachment;
  allergies: string[];
  health_conditions: string[];
}

export interface StaffUserData extends Staff, User {
  current_year_start_date: string;
  current_year_end_date: string;
  role: string;
}

export interface ClientUserData extends Client, User {
  current_year_start_date: string;
  current_year_end_date: string;
  role: string;
}

export interface Message {
  id: string;
  sender: string
  message: string
}
export interface ConsultationOne {
  id: number;
  name: string;
  purpose: string
  staff: StaffTwo;
  date: string;
  time: string;
  type: string;
  follow_up: {id: number; name: string;} | null;
  created_at: string;
  updated_at: string;
}

export interface DrugStock {
  id: number;
  name: string;
  quantity: number;
  order_quantity: number;
  price: number;
  is_prescription_required: boolean;
}

export interface Drug {
  id: number;
  name: string;
  generic_name: string
  brand: string
  description: string;
  dosage_form: string[];
  route: string[];
  pharm_class: string[];
  indications: string;
  side_effects: string;
  precautions: string;
  active_ingredients: string[];
  warnings: string;
  storage: string;
  manufacturer: string
  stocks: DrugStock[];
  is_prescription_required: boolean;
  img_url?: string | null;
}
export interface OrderItem {
  id: number;
  drug: {
    id: number;
    name: string;
  }
  quantity: number;
  total_price: number;
  price: number;
  prescription_image: string | null;
}
export interface Order {
  id: number;
  status: string;
  address: string;
  items: OrderItem[];
  total_price: number;
  date: string;
}

export interface DietPlanItem {
  day: number;
  date: string;
  meals: {
    [mealType: string]: string[];
  };
  notes: string;
}

export interface DietPlan {
  id: number;
  goal: string
  diet_type: "regular" | "vegetarian" | "vegan" | "keto";
  duration_days: number;
  meal_types: string[]; 
  activity_level: "sedentary" | "lightly_active" | "moderately_active" | "very_active" | "extra_active";
  preferred_foods: string[];
  end_date: string;
  plans: DietPlanItem[]
}