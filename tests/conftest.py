"""Pytest configuration and shared fixtures for FastAPI backend tests."""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Provide a test client with a fresh app instance.
    
    Returns a TestClient for making API requests during tests.
    Note: Since the app uses module-level in-memory storage, each test
    should reset the activities state as needed.
    """
    return TestClient(app)


@pytest.fixture
def reset_activities():
    """Reset activities to a known state for each test.
    
    Clears all activities and repopulates with fresh sample data.
    This ensures test isolation since the app uses in-memory storage.
    """
    # Clear existing activities
    activities.clear()
    
    # Repopulate with sample data
    activities.update({
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball league and practice",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["james@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Tennis instruction and matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["alex@mergington.edu", "jordan@mergington.edu"]
        },
        "Drama Club": {
            "description": "Perform in theatrical productions and build stage skills",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 25,
            "participants": ["grace@mergington.edu"]
        },
        "Art Studio": {
            "description": "Painting, drawing, and sculpture techniques",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["maya@mergington.edu", "lucas@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop argumentation and public speaking skills",
            "schedule": "Mondays and Fridays, 3:30 PM - 4:30 PM",
            "max_participants": 16,
            "participants": ["noah@mergington.edu"]
        },
        "Science Club": {
            "description": "Explore scientific experiments and discovery",
            "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["ava@mergington.edu", "ethan@mergington.edu"]
        }
    })
    yield
    # Cleanup after test
    activities.clear()


@pytest.fixture
def test_email():
    """Provide a test email address for signup tests."""
    return "test.student@mergington.edu"


@pytest.fixture
def full_activity():
    """Provide an activity that is at capacity to test full capacity scenario."""
    activities.clear()
    activities.update({
        "Full Activity": {
            "description": "An activity at capacity",
            "schedule": "Monday, 3:00 PM",
            "max_participants": 2,
            "participants": ["student1@mergington.edu", "student2@mergington.edu"]
        }
    })
    yield "Full Activity"
    activities.clear()
