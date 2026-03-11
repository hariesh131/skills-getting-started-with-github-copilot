import pytest
from fastapi.testclient import TestClient
from src.app import app


# Store the original activities data
ORIGINAL_ACTIVITIES = {
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
        "description": "Competitive basketball team for varsity and intramural play",
        "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 15,
        "participants": ["alex@mergington.edu"]
    },
    "Tennis Club": {
        "description": "Tennis training and friendly matches",
        "schedule": "Wednesdays and Saturdays, 3:00 PM - 4:30 PM",
        "max_participants": 10,
        "participants": ["lucas@mergington.edu", "isabella@mergington.edu"]
    },
    "Art Studio": {
        "description": "Painting, drawing, and sculpture techniques",
        "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
        "max_participants": 15,
        "participants": ["grace@mergington.edu"]
    },
    "Drama Club": {
        "description": "Theater performances and acting workshops",
        "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
        "max_participants": 20,
        "participants": ["noah@mergington.edu", "ava@mergington.edu"]
    },
    "Debate Team": {
        "description": "Competitive debate and public speaking skills",
        "schedule": "Thursdays, 3:30 PM - 5:00 PM",
        "max_participants": 12,
        "participants": ["mia@mergington.edu"]
    },
    "Science Club": {
        "description": "Hands-on experiments and STEM exploration",
        "schedule": "Wednesdays, 3:30 PM - 4:30 PM",
        "max_participants": 18,
        "participants": ["ethan@mergington.edu", "zoe@mergington.edu"]
    }
}


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the activities database before each test."""
    from src.app import activities
    
    # Clear and restore original data
    activities.clear()
    activities.update({name: {
        "description": data["description"],
        "schedule": data["schedule"],
        "max_participants": data["max_participants"],
        "participants": data["participants"].copy()  # Create a copy of the list
    } for name, data in ORIGINAL_ACTIVITIES.items()})
    
    yield


@pytest.fixture
def client():
    """Provide a TestClient for making requests to the API."""
    return TestClient(app)


@pytest.fixture
def sample_email():
    """Provide a sample email for testing."""
    return "test@mergington.edu"


@pytest.fixture
def sample_activity():
    """Provide a sample activity name for testing."""
    return "Chess Club"


@pytest.fixture
def new_activity_email():
    """Provide an email for signup that doesn't exist in activities yet."""
    return "newstudent@mergington.edu"
