"""
Unit tests for database models.
"""
from datetime import datetime

import pytest

from app import DietPlan, User


@pytest.mark.unit
@pytest.mark.database
class TestUserModel:
    """Test cases for User model."""

    def test_user_creation(self, db_session):
        """Test creating a user with valid data."""
        user = User(
            name="John Doe",
            email="john@example.com",
            age=30,
            gender="male",
            weight=75.5,
            height=180,
            activity_level="moderate",
            diet_preference="balanced",
            health_goals="Weight loss",
        )
        user.set_password("password123")

        db_session.add(user)
        db_session.commit()

        assert user.id is not None
        assert user.name == "John Doe"
        assert user.email == "john@example.com"
        assert user.age == 30
        assert user.gender == "male"
        assert user.weight == 75.5
        assert user.height == 180
        assert user.activity_level == "moderate"
        assert user.diet_preference == "balanced"
        assert user.health_goals == "Weight loss"
        assert user.password_hash is not None
        assert user.created_at is not None
        assert user.updated_at is not None

    def test_user_password_hashing(self, db_session):
        """Test password hashing and verification."""
        user = User(
            name="Jane Doe",
            email="jane@example.com",
            age=25,
            gender="female",
            weight=65,
        )

        # Test password setting
        user.set_password("mypassword")
        assert user.password_hash is not None
        assert user.password_hash != "mypassword"  # Should be hashed

        # Test password verification
        assert user.check_password("mypassword") is True
        assert user.check_password("wrongpassword") is False

    def test_user_email_uniqueness(self, db_session, sample_user):
        """Test that email addresses must be unique."""
        with pytest.raises(Exception):  # Should raise IntegrityError
            duplicate_user = User(
                name="Another User",
                email=sample_user.email,  # Same email
                age=25,
                gender="female",
                weight=60,
            )
            duplicate_user.set_password("password")
            db_session.add(duplicate_user)
            db_session.commit()

    def test_user_repr(self, db_session):
        """Test user string representation."""
        user = User(name="Test User", email="test@example.com", age=30, gender="male", weight=70)
        user.set_password("password123")  # Set password since it's required
        db_session.add(user)
        db_session.commit()

        assert str(user) == f"<User {user.email}>"


@pytest.mark.unit
@pytest.mark.database
class TestDietPlanModel:
    """Test cases for DietPlan model."""

    def test_diet_plan_creation(self, db_session, sample_user):
        """Test creating a diet plan with valid data."""
        plan_data = {"daily_plans": [{"day": "Day 1", "date": "2023-01-01", "meals": []}]}

        diet_plan = DietPlan(
            user_id=sample_user.id,
            plan_name="Test Plan",
            start_date=datetime(2023, 1, 1),
            end_date=datetime(2023, 1, 7),
            total_calories=2000,
            plan_data=plan_data,
        )

        db_session.add(diet_plan)
        db_session.commit()

        assert diet_plan.id is not None
        assert diet_plan.user_id == sample_user.id
        assert diet_plan.plan_name == "Test Plan"
        assert diet_plan.total_calories == 2000
        assert diet_plan.plan_data == plan_data
        assert diet_plan.created_at is not None

    def test_diet_plan_user_relationship(self, db_session, sample_diet_plan):
        """Test relationship between diet plan and user."""
        assert sample_diet_plan.user is not None
        assert sample_diet_plan.user.id == sample_diet_plan.user_id
        assert sample_diet_plan in sample_diet_plan.user.diet_plans

    def test_diet_plan_repr(self, db_session, sample_diet_plan):
        """Test diet plan string representation."""
        expected = f"<DietPlan {sample_diet_plan.plan_name} for {sample_diet_plan.user.email}>"
        assert str(sample_diet_plan) == expected
