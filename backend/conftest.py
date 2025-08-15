"""
Pytest configuration and fixtures for the Diet Planner backend.
"""
import os
import tempfile
import pytest
from datetime import datetime, timedelta
from app import app, db, User, DietPlan, MealLog
import factory


@pytest.fixture(scope='function')
def test_app():
    """Create and configure a test app instance."""
    # Just use the existing app but create separate test tables
    app.config['TESTING'] = True
    app.config['JWT_SECRET_KEY'] = 'test-jwt-secret'
    app.config['SECRET_KEY'] = 'test-secret-key'
    app.config['WTF_CSRF_ENABLED'] = False
    
    with app.app_context():
        # Create tables if they don't exist (PostgreSQL will be used)
        db.create_all()
        yield app
        # Don't drop tables - just clean data in teardown


@pytest.fixture
def client(test_app):
    """Create a test client."""
    return test_app.test_client()


@pytest.fixture
def app_context(test_app):
    """Create an application context."""
    with test_app.app_context():
        yield test_app


@pytest.fixture
def db_session(app_context):
    """Create a database session for testing."""
    # Clean up any existing test data
    db.session.query(DietPlan).delete()
    db.session.query(MealLog).delete()
    db.session.query(User).delete()
    db.session.commit()
    
    yield db.session
    
    # Clean up after test
    db.session.rollback()
    db.session.query(DietPlan).delete()
    db.session.query(MealLog).delete()
    db.session.query(User).delete()
    db.session.commit()


# Factories for test data generation
class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory for creating test users."""
    
    class Meta:
        model = User
        sqlalchemy_session_persistence = 'commit'
    
    name = factory.Faker('name')
    email = factory.Faker('email')
    age = factory.Faker('random_int', min=18, max=80)
    gender = factory.Faker('random_element', elements=['male', 'female', 'other'])
    weight = factory.Faker('random_int', min=40, max=150)
    height = factory.Faker('random_int', min=140, max=200)
    activity_level = factory.Faker('random_element', 
                                  elements=['sedentary', 'light', 'moderate', 'active', 'very_active'])
    diet_preference = factory.Faker('random_element',
                                   elements=['balanced', 'vegetarian', 'vegan', 'keto', 'paleo'])
    health_goals = factory.Faker('text', max_nb_chars=200)
    password_hash = factory.LazyFunction(lambda: _hash_password("password123"))


def _hash_password(password):
    """Helper function to hash password for factory."""
    import bcrypt
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt).decode('utf-8')


class DietPlanFactory(factory.alchemy.SQLAlchemyModelFactory):
    """Factory for creating test diet plans."""
    
    class Meta:
        model = DietPlan
        sqlalchemy_session_persistence = 'commit'
    
    user = factory.SubFactory(UserFactory)
    plan_name = factory.Faker('sentence', nb_words=3)
    start_date = factory.Faker('date_this_month')
    end_date = factory.LazyAttribute(lambda obj: obj.start_date + timedelta(days=7))
    total_calories = factory.Faker('random_int', min=1200, max=3000)
    plan_data = factory.LazyFunction(lambda: {
        "daily_plans": [
            {
                "day": f"Day {i+1}",
                "date": (datetime.now() + timedelta(days=i)).isoformat(),
                "meals": [
                    {
                        "meal_type": "Breakfast",
                        "name": "Test Breakfast",
                        "foods": [
                            {
                                "name": "Oatmeal",
                                "portion": "1 cup",
                                "calories": 150,
                                "protein": 5,
                                "carbs": 30,
                                "fat": 3
                            }
                        ]
                    }
                ]
            } for i in range(7)
        ]
    })


@pytest.fixture
def sample_user(db_session):
    """Create a sample user for testing."""
    UserFactory._meta.sqlalchemy_session = db_session
    user = UserFactory()
    db_session.commit()
    return user


@pytest.fixture
def sample_diet_plan(db_session, sample_user):
    """Create a sample diet plan for testing."""
    DietPlanFactory._meta.sqlalchemy_session = db_session
    diet_plan = DietPlanFactory(user=sample_user)
    db_session.commit()
    return diet_plan


@pytest.fixture
def auth_headers(client, sample_user):
    """Get authentication headers for a user."""
    login_data = {
        'email': sample_user.email,
        'password': 'password123'
    }
    response = client.post('/api/login', json=login_data)
    token = response.get_json()['access_token']
    return {'Authorization': f'Bearer {token}'}


@pytest.fixture
def mock_gemini_response():
    """Mock Gemini API response for testing."""
    return {
        "plan_name": "Test 7-Day Balanced Diet Plan",
        "daily_plans": [
            {
                "day": "Day 1",
                "date": datetime.now().isoformat(),
                "meals": [
                    {
                        "meal_type": "Breakfast",
                        "name": "Healthy Oatmeal Bowl",
                        "foods": [
                            {
                                "name": "Oatmeal",
                                "portion": "1 cup",
                                "calories": 150,
                                "protein": 5,
                                "carbs": 30,
                                "fat": 3
                            },
                            {
                                "name": "Banana",
                                "portion": "1 medium",
                                "calories": 105,
                                "protein": 1,
                                "carbs": 27,
                                "fat": 0
                            }
                        ]
                    }
                ]
            }
        ]
    }
