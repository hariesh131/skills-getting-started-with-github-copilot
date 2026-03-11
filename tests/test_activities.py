import pytest


def test_get_activities_success(client):
    """Test successful retrieval of all activities."""
    response = client.get("/activities")
    assert response.status_code == 200
    activities = response.json()
    assert isinstance(activities, dict)
    assert len(activities) > 0


def test_get_activities_structure(client):
    """Test that activities have expected structure."""
    response = client.get("/activities")
    activities = response.json()
    
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_name, str)
        assert "description" in activity_data
        assert "schedule" in activity_data
        assert "max_participants" in activity_data
        assert "participants" in activity_data
        assert isinstance(activity_data["participants"], list)
        assert isinstance(activity_data["max_participants"], int)


def test_get_activities_contains_expected_activities(client):
    """Test that the expected activities are present in the response."""
    response = client.get("/activities")
    activities = response.json()
    
    expected_activities = [
        "Chess Club",
        "Programming Class",
        "Gym Class",
        "Basketball Team",
        "Tennis Club",
        "Art Studio",
        "Drama Club",
        "Debate Team",
        "Science Club"
    ]
    
    for expected in expected_activities:
        assert expected in activities, f"Expected activity '{expected}' not found"


@pytest.mark.parametrize("activity_name", [
    "Chess Club",
    "Programming Class",
    "Gym Class",
    "Debate Team"
])
def test_get_activities_contains_valid_participants(client, activity_name):
    """Test that activities contain valid participant emails."""
    response = client.get("/activities")
    activities = response.json()
    
    activity = activities[activity_name]
    for participant in activity["participants"]:
        assert isinstance(participant, str)
        assert "@" in participant, f"Invalid email format: {participant}"
