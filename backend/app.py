import json
import os
from datetime import datetime, timedelta

import bcrypt
import google.generativeai as genai
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, ValidationError, fields

# Import enhanced modules
from config import get_config, validate_config
from security import SecurityManager, configure_security
from monitoring import setup_monitoring

# Get environment-specific configuration
environment = os.getenv('FLASK_ENV', 'development')
config_class = get_config(environment)

# Create Flask app with configuration
app = Flask(__name__)
app.config.from_object(config_class)

# Validate configuration
config_validation = validate_config()
if config_validation['errors']:
    for error in config_validation['errors']:
        app.logger.error(f"Configuration error: {error}")
    if environment == 'production':
        raise RuntimeError("Invalid configuration for production environment")

if config_validation['warnings']:
    for warning in config_validation['warnings']:
        app.logger.warning(f"Configuration warning: {warning}")

# Initialize extensions
db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)

# Initialize security
security_manager = configure_security(app, environment)

# Initialize monitoring
monitor, profiler = setup_monitoring(app)

# Configure CORS
CORS(app, origins=app.config['CORS_ORIGINS'], supports_credentials=True)

# Configure Gemini AI
genai.configure(api_key=app.config['GEMINI_API_KEY'])


# Database Models
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    weight = db.Column(db.Numeric(5, 2), nullable=False)
    height = db.Column(db.Numeric(5, 2))
    activity_level = db.Column(db.String(50))
    diet_preference = db.Column(db.String(50))
    health_goals = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def set_password(self, password):
        """Hash and set password"""
        password_bytes = password.encode("utf-8")
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password_bytes, salt).decode("utf-8")

    def check_password(self, password):
        """Check if provided password matches hash"""
        password_bytes = password.encode("utf-8")
        hash_bytes = self.password_hash.encode("utf-8")
        return bcrypt.checkpw(password_bytes, hash_bytes)

    def __repr__(self):
        return f"<User {self.email}>"


class DietPlan(db.Model):
    __tablename__ = "diet_plans"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    plan_name = db.Column(db.String(255))
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    total_calories = db.Column(db.Integer)
    plan_data = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    user = db.relationship("User", backref=db.backref("diet_plans", lazy=True))

    def __repr__(self):
        return f"<DietPlan {self.plan_name} for {self.user.email}>"


class MealLog(db.Model):
    __tablename__ = "meal_logs"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    diet_plan_id = db.Column(db.Integer, db.ForeignKey("diet_plans.id"), nullable=True)
    meal_date = db.Column(db.Date, nullable=False)
    meal_type = db.Column(db.String(50), nullable=False)  # breakfast, lunch, dinner, snack
    meal_name = db.Column(db.String(255), nullable=False)
    calories = db.Column(db.Integer)
    protein = db.Column(db.Numeric(5, 2))
    carbs = db.Column(db.Numeric(5, 2))
    fat = db.Column(db.Numeric(5, 2))
    consumed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship("User", backref=db.backref("meal_logs", lazy=True))
    diet_plan = db.relationship("DietPlan", backref=db.backref("meal_logs", lazy=True))
    
    def __repr__(self):
        return f"<MealLog {self.meal_name} for {self.user.email}>"


# Marshmallow Schemas
class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User

    id = ma.auto_field()
    name = ma.auto_field()
    email = ma.auto_field()
    age = ma.auto_field()
    gender = ma.auto_field()
    weight = ma.auto_field()
    height = ma.auto_field()
    activity_level = ma.auto_field()
    diet_preference = ma.auto_field()
    health_goals = ma.auto_field()
    created_at = ma.auto_field()


class DietPlanSchema(ma.SQLAlchemySchema):
    class Meta:
        model = DietPlan

    id = ma.auto_field()
    user_id = ma.auto_field()
    plan_name = ma.auto_field()
    start_date = ma.auto_field()
    end_date = ma.auto_field()
    total_calories = ma.auto_field()
    plan_data = ma.auto_field()
    created_at = ma.auto_field()


# Initialize schemas
user_schema = UserSchema()
users_schema = UserSchema(many=True)
diet_plan_schema = DietPlanSchema()
diet_plans_schema = DietPlanSchema(many=True)


def validate_user_data(data, is_update=False):
    """Validate user data with comprehensive checks"""
    # Validate required fields with proper validation
    # For updates, most fields are optional (except password which is handled separately)
    if is_update:
        validation_rules = {
            "name": {"required": False, "min_length": 2, "max_length": 100},
            "email": {"required": False, "min_length": 5, "max_length": 255},
            "password": {"required": False, "min_length": 6, "max_length": 100},
            "age": {"required": False, "min_value": 1, "max_value": 120},
            "gender": {
                "required": False,
                "min_length": 4,
                "allowed_values": ["male", "female", "other"],
            },
            "weight": {"required": False, "min_value": 20, "max_value": 300},
        }
    else:
        validation_rules = {
            "name": {"required": True, "min_length": 2, "max_length": 100},
            "email": {"required": True, "min_length": 5, "max_length": 255},
            "password": {"required": True, "min_length": 6, "max_length": 100},
            "age": {"required": True, "min_value": 1, "max_value": 120},
            "gender": {
                "required": True,
                "min_length": 4,
                "allowed_values": ["male", "female", "other"],
            },
            "weight": {"required": True, "min_value": 20, "max_value": 300},
        }

    for field, rules in validation_rules.items():
        # Check if field is missing
        if field not in data:
            if rules.get("required", False):
                return f"Missing required field: {field}"
            else:
                continue

        value = data[field]

        # Check for empty values
        if value is None or (isinstance(value, str) and value.strip() == ""):
            return f"{field.title()} cannot be empty"

        # String validation
        if isinstance(value, str):
            value = value.strip()
            data[field] = value  # Update with trimmed value

            if "min_length" in rules and len(value) < rules["min_length"]:
                return f"{field.title()} must be at least {rules['min_length']} characters long"

            if "max_length" in rules and len(value) > rules["max_length"]:
                return f"{field.title()} must be at most {rules['max_length']} characters long"

            if "allowed_values" in rules and value.lower() not in rules["allowed_values"]:
                return f"{field.title()} must be one of: {', '.join(rules['allowed_values'])}"

        # Numeric validation
        elif isinstance(value, (int, float)):
            if "min_value" in rules and value < rules["min_value"]:
                return f"{field.title()} must be at least {rules['min_value']}"

            if "max_value" in rules and value > rules["max_value"]:
                return f"{field.title()} must be at most {rules['max_value']}"

        # Type validation
        else:
            if field in ["age", "weight"]:
                try:
                    value = float(value)
                    data[field] = value
                    if "min_value" in rules and value < rules["min_value"]:
                        return f"{field.title()} must be at least {rules['min_value']}"
                    if "max_value" in rules and value > rules["max_value"]:
                        return f"{field.title()} must be at most {rules['max_value']}"
                except (ValueError, TypeError):
                    return f"{field.title()} must be a valid number"

    # Email format validation (only if email is provided)
    if "email" in data:
        import re
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_pattern, data["email"]):
            return "Please enter a valid email address"

    # Validate optional fields if provided
    optional_fields = {
        "height": {"min_value": 100, "max_value": 250},
        "health_goals": {"max_length": 500},
        "activity_level": {
            "allowed_values": ["sedentary", "light", "moderate", "active", "very_active"]
        },
        "diet_preference": {
            "allowed_values": [
                "balanced",
                "vegetarian",
                "vegan",
                "keto",
                "paleo",
                "mediterranean",
                "low_carb",
                "high_protein",
            ]
        },
    }

    for field, rules in optional_fields.items():
        if field in data and data[field] is not None:
            value = data[field]

            # Skip validation if empty string (optional field)
            if isinstance(value, str) and value.strip() == "":
                data[field] = None
                continue

            # String validation for optional fields
            if isinstance(value, str):
                value = value.strip()
                data[field] = value

                if "max_length" in rules and len(value) > rules["max_length"]:
                    return f"{field.replace('_', ' ').title()} must be at most {rules['max_length']} characters long"

                if "allowed_values" in rules and value.lower() not in rules["allowed_values"]:
                    return f"{field.replace('_', ' ').title()} must be one of: {', '.join(rules['allowed_values'])}"

            # Numeric validation for height
            elif field == "height":
                try:
                    value = float(value)
                    data[field] = value
                    if "min_value" in rules and value < rules["min_value"]:
                        return f"Height must be at least {rules['min_value']} cm"
                    if "max_value" in rules and value > rules["max_value"]:
                        return f"Height must be at most {rules['max_value']} cm"
                except (ValueError, TypeError):
                    return "Height must be a valid number"

    return None  # No validation errors


def calculate_bmr(weight, height, age, gender):
    """Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation"""
    if gender.lower() == "male":
        bmr = 10 * float(weight) + 6.25 * float(height) - 5 * age + 5
    else:
        bmr = 10 * float(weight) + 6.25 * float(height) - 5 * age - 161
    return round(bmr)


def calculate_tdee(bmr, activity_level):
    """Calculate Total Daily Energy Expenditure"""
    activity_multipliers = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very_active": 1.9,
    }
    return round(bmr * activity_multipliers.get(activity_level.lower(), 1.55))


def generate_diet_plan_with_gemini(user_data):
    """Generate diet plan using Gemini AI"""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        # Calculate calories
        bmr = calculate_bmr(
            user_data["weight"], user_data["height"], user_data["age"], user_data["gender"]
        )
        tdee = calculate_tdee(bmr, user_data["activity_level"])

        # Create prompt for Gemini
        prompt = f"""
        Create a detailed 1-week diet plan for a {user_data['age']}-year-old {user_data['gender']} person.
        
        User Details:
        - Weight: {user_data['weight']} kg
        - Height: {user_data['height']} cm
        - Activity Level: {user_data['activity_level']}
        - Diet Preference: {user_data['diet_preference']}
        - Health Goals: {user_data['health_goals']}
        - Daily Calorie Target: {tdee} calories
        
        Requirements:
        1. Create a 7-day meal plan with breakfast, lunch, dinner, and 2 snacks
        2. Each meal should include specific foods, portions, and calorie counts
        3. Ensure the plan is {user_data['diet_preference']} friendly
        4. Include nutritional information (protein, carbs, fat) for each meal
        5. Provide variety and ensure meals are practical and easy to prepare
        6. Consider the health goals mentioned
        
        Return the response as a JSON object with the following structure:
        {{
            "total_calories_per_day": {tdee},
            "daily_plans": [
                {{
                    "day": "Day 1",
                    "date": "YYYY-MM-DD",
                    "meals": [
                        {{
                            "meal_type": "breakfast",
                            "meal_name": "Meal Name",
                            "foods": [
                                {{
                                    "name": "Food Item",
                                    "portion": "100g",
                                    "calories": 150,
                                    "protein": 10,
                                    "carbs": 20,
                                    "fat": 5
                                }}
                            ],
                            "total_calories": 300,
                            "total_protein": 15,
                            "total_carbs": 25,
                            "total_fat": 8
                        }}
                    ]
                }}
            ]
        }}
        
        Make sure the JSON is valid and well-formatted.
        """

        response = model.generate_content(prompt)

        # Parse the response and extract JSON
        response_text = response.text

        # Try to extract JSON from the response
        try:
            # Look for JSON in the response
            start_idx = response_text.find("{")
            end_idx = response_text.rfind("}") + 1
            json_str = response_text[start_idx:end_idx]
            diet_plan = json.loads(json_str)
            return diet_plan
        except json.JSONDecodeError:
            # If JSON parsing fails, create a structured response
            return {
                "total_calories_per_day": tdee,
                "daily_plans": [],
                "raw_response": response_text,
            }

    except Exception as e:
        print(f"Error generating diet plan: {str(e)}")
        print(f"Error type: {type(e)}")
        print(f"Error details: {e}")
        return None


# API Routes
@app.route("/api/register", methods=["POST"])
def register():
    """Register a new user"""
    try:
        data = request.get_json()

        # Validate user data
        validation_error = validate_user_data(data)
        if validation_error:
            return jsonify({"error": validation_error}), 400

        # Check if user already exists
        existing_user = User.query.filter_by(email=data["email"]).first()
        if existing_user:
            return jsonify({"error": "User with this email already exists"}), 409

        # Create new user
        new_user = User(
            name=data["name"],
            email=data["email"],
            age=data["age"],
            gender=data["gender"],
            weight=data["weight"],
            height=data.get("height"),
            activity_level=data.get("activity_level", "moderate"),
            diet_preference=data.get("diet_preference", "balanced"),
            health_goals=data.get("health_goals", ""),
        )

        # Set password
        new_user.set_password(data["password"])

        db.session.add(new_user)
        db.session.commit()

        # Create access token
        access_token = create_access_token(identity=new_user.id)

        return (
            jsonify(
                {
                    "message": "User registered successfully",
                    "access_token": access_token,
                    "user": user_schema.dump(new_user),
                }
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route("/api/login", methods=["POST"])
@security_manager.limiter.limit("5 per minute")  # Rate limit login attempts
def login():
    """Login user with enhanced security"""
    try:
        data = request.get_json()
        client_ip = request.remote_addr
        
        # Validate required fields
        if "email" not in data or "password" not in data:
            return jsonify({"error": "Email and password are required"}), 400

        email = data["email"].lower().strip()
        
        # Check rate limiting
        if not security_manager.rate_limit_login_attempts(email, client_ip):
            app.logger.warning(f"Rate limit exceeded for login attempt: {email} from {client_ip}")
            return jsonify({"error": "Too many login attempts. Please try again later."}), 429

        # Check if user exists
        user = User.query.filter_by(email=email).first()
        if not user:
            security_manager.record_failed_login(email, client_ip)
            app.logger.warning(f"Login attempt for non-existent user: {email} from {client_ip}")
            return jsonify({"error": "Invalid email or password"}), 401

        # Check password
        if not user.check_password(data["password"]):
            security_manager.record_failed_login(email, client_ip)
            app.logger.warning(f"Failed login attempt for user: {email} from {client_ip}")
            return jsonify({"error": "Invalid email or password"}), 401

        # Successful login - create access token
        access_token = create_access_token(identity=user.id)
        
        app.logger.info(f"Successful login for user: {email} from {client_ip}")

        return (
            jsonify(
                {
                    "message": "Login successful",
                    "access_token": access_token,
                    "user": user_schema.dump(user),
                }
            ),
            200,
        )

    except Exception as e:
        app.logger.error(f"Login error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/api/profile", methods=["GET"])
@jwt_required()
def get_profile():
    """Get current user profile"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get_or_404(current_user_id)
        return user_schema.dump(user), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/profile", methods=["PUT"])
@jwt_required()
def update_profile():
    """Update current user profile"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get_or_404(current_user_id)
        data = request.get_json()

        # Remove password from validation if not provided
        if "password" not in data or not data["password"]:
            data.pop("password", None)

        # Validate user data (for update)
        validation_error = validate_user_data(data, is_update=True)
        if validation_error:
            return jsonify({"error": validation_error}), 400

        # Check if email is being changed and already exists
        if "email" in data and data["email"] != user.email:
            existing_user = User.query.filter_by(email=data["email"]).first()
            if existing_user:
                return jsonify({"error": "Email already exists"}), 409

        # Update user fields
        updatable_fields = [
            "name",
            "email",
            "age",
            "gender",
            "weight",
            "height",
            "activity_level",
            "diet_preference",
            "health_goals",
        ]

        for field in updatable_fields:
            if field in data:
                setattr(user, field, data[field])

        # Update password if provided
        if "password" in data and data["password"]:
            user.set_password(data["password"])

        user.updated_at = datetime.utcnow()
        db.session.commit()

        return (
            jsonify({"message": "Profile updated successfully", "user": user_schema.dump(user)}),
            200,
        )

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route("/api/diet-plan", methods=["POST"])
@jwt_required()
def generate_diet_plan():
    """Generate a new diet plan"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get_or_404(current_user_id)

        # Generate diet plan using Gemini
        user_data = {
            "age": user.age,
            "gender": user.gender,
            "weight": float(user.weight),
            "height": float(user.height) if user.height else 170,
            "activity_level": user.activity_level or "moderate",
            "diet_preference": user.diet_preference or "balanced",
            "health_goals": user.health_goals or "Maintain healthy weight",
        }

        diet_plan_data = generate_diet_plan_with_gemini(user_data)

        if not diet_plan_data:
            return jsonify({"error": "Failed to generate diet plan"}), 500

        # Calculate start and end dates (1 week from today)
        start_date = datetime.now().date()
        end_date = start_date + timedelta(days=6)

        # Create diet plan record
        new_diet_plan = DietPlan(
            user_id=user.id,
            plan_name=f"1-Week {user.diet_preference.title()} Diet Plan",
            start_date=start_date,
            end_date=end_date,
            total_calories=diet_plan_data.get("total_calories_per_day", 2000),
            plan_data=diet_plan_data,
        )

        db.session.add(new_diet_plan)
        db.session.commit()

        return diet_plan_schema.dump(new_diet_plan), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route("/api/diet-plans", methods=["GET"])
@jwt_required()
def get_user_diet_plans():
    """Get all diet plans for current user"""
    try:
        current_user_id = get_jwt_identity()
        diet_plans = (
            DietPlan.query.filter_by(user_id=current_user_id)
            .order_by(DietPlan.created_at.desc())
            .all()
        )
        return diet_plans_schema.dump(diet_plans), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/diet-plan/<int:plan_id>", methods=["GET"])
@jwt_required()
def get_diet_plan(plan_id):
    """Get a specific diet plan"""
    try:
        current_user_id = get_jwt_identity()
        diet_plan = DietPlan.query.filter_by(id=plan_id, user_id=current_user_id).first()
        if not diet_plan:
            return jsonify({"error": "Diet plan not found"}), 404
        return diet_plan_schema.dump(diet_plan), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5001, debug=True)
