import pytest


class TestSignup:
    """Tests for POST /activities/{activity_name}/signup endpoint."""

    def test_signup_success(self, client, sample_activity, new_activity_email):
        """Test successful signup for an activity."""
        response = client.post(
            f"/activities/{sample_activity}/signup",
            params={"email": new_activity_email}
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert new_activity_email in data["message"]

    def test_signup_participant_added_to_list(self, client, sample_activity, new_activity_email):
        """Test that a participant is added to the activity's participant list."""
        # Get initial participant count
        response = client.get("/activities")
        initial_participants = response.json()[sample_activity]["participants"]
        initial_count = len(initial_participants)

        # Sign up the new participant
        client.post(
            f"/activities/{sample_activity}/signup",
            params={"email": new_activity_email}
        )

        # Verify participant was added
        response = client.get("/activities")
        updated_participants = response.json()[sample_activity]["participants"]
        assert new_activity_email in updated_participants
        assert len(updated_participants) == initial_count + 1

    def test_signup_duplicate_fails(self, client, sample_activity):
        """Test that signing up the same email twice fails."""
        existing_participant = "michael@mergington.edu"

        # Try to sign up someone already registered
        response = client.post(
            f"/activities/{sample_activity}/signup",
            params={"email": existing_participant}
        )
        assert response.status_code == 400
        data = response.json()
        assert "Already registered" in data["detail"]

    def test_signup_nonexistent_activity_fails(self, client, new_activity_email):
        """Test that signup for a non-existent activity fails."""
        response = client.post(
            "/activities/Nonexistent Activity/signup",
            params={"email": new_activity_email}
        )
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    @pytest.mark.parametrize("email,activity", [
        ("alice@mergington.edu", "Chess Club"),
        ("bob@mergington.edu", "Programming Class"),
        ("charlie@mergington.edu", "Drama Club"),
    ])
    def test_signup_multiple_participants_and_activities(self, client, email, activity):
        """Test signup for multiple participants and activities."""
        response = client.post(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert response.status_code == 200

        # Verify participant was added
        response = client.get("/activities")
        assert email in response.json()[activity]["participants"]


class TestUnregister:
    """Tests for DELETE /activities/{activity_name}/signup endpoint."""

    def test_unregister_success(self, client, sample_activity):
        """Test successful unregistration from an activity."""
        participant_to_remove = "michael@mergington.edu"

        response = client.delete(
            f"/activities/{sample_activity}/signup",
            params={"email": participant_to_remove}
        )
        assert response.status_code == 200
        data = response.json()
        assert "Unregistered" in data["message"]

    def test_unregister_participant_removed_from_list(self, client, sample_activity):
        """Test that a participant is removed from the activity's participant list."""
        participant_to_remove = "michael@mergington.edu"

        # Get initial participant count
        response = client.get("/activities")
        initial_participants = response.json()[sample_activity]["participants"]
        initial_count = len(initial_participants)
        assert participant_to_remove in initial_participants

        # Remove the participant
        client.delete(
            f"/activities/{sample_activity}/signup",
            params={"email": participant_to_remove}
        )

        # Verify participant was removed
        response = client.get("/activities")
        updated_participants = response.json()[sample_activity]["participants"]
        assert participant_to_remove not in updated_participants
        assert len(updated_participants) == initial_count - 1

    def test_unregister_nonexistent_participant_fails(self, client, sample_activity):
        """Test that removing a non-registered participant fails."""
        response = client.delete(
            f"/activities/{sample_activity}/signup",
            params={"email": "nonexistent@mergington.edu"}
        )
        assert response.status_code == 400
        data = response.json()
        assert "not registered" in data["detail"]

    def test_unregister_nonexistent_activity_fails(self, client):
        """Test that removal from a non-existent activity fails."""
        response = client.delete(
            "/activities/Nonexistent Activity/signup",
            params={"email": "test@mergington.edu"}
        )
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    @pytest.mark.parametrize("email,activity", [
        ("michael@mergington.edu", "Chess Club"),
        ("emma@mergington.edu", "Programming Class"),
        ("lucas@mergington.edu", "Tennis Club"),
    ])
    def test_unregister_multiple_participants(self, client, email, activity):
        """Test unregistration for multiple participants across activities."""
        # Verify participant exists
        response = client.get("/activities")
        assert email in response.json()[activity]["participants"]

        # Remove participant
        response = client.delete(
            f"/activities/{activity}/signup",
            params={"email": email}
        )
        assert response.status_code == 200

        # Verify participant was removed
        response = client.get("/activities")
        assert email not in response.json()[activity]["participants"]


class TestSignupAndUnregisterIntegration:
    """Integration tests for signup and unregister workflows."""

    def test_signup_then_unregister(self, client, sample_activity, new_activity_email):
        """Test signing up and then unregistering in sequence."""
        # Sign up
        response = client.post(
            f"/activities/{sample_activity}/signup",
            params={"email": new_activity_email}
        )
        assert response.status_code == 200

        # Verify added
        response = client.get("/activities")
        assert new_activity_email in response.json()[sample_activity]["participants"]

        # Unregister
        response = client.delete(
            f"/activities/{sample_activity}/signup",
            params={"email": new_activity_email}
        )
        assert response.status_code == 200

        # Verify removed
        response = client.get("/activities")
        assert new_activity_email not in response.json()[sample_activity]["participants"]

    def test_signup_multiple_then_unregister_one(self, client):
        """Test signing up multiple times then unregistering one."""
        activity = "Chess Club"
        email1 = "test1@mergington.edu"
        email2 = "test2@mergington.edu"

        # Sign up both
        client.post(f"/activities/{activity}/signup", params={"email": email1})
        client.post(f"/activities/{activity}/signup", params={"email": email2})

        # Verify both added
        response = client.get("/activities")
        participants = response.json()[activity]["participants"]
        assert email1 in participants
        assert email2 in participants
        count_after_signup = len(participants)

        # Remove one
        client.delete(f"/activities/{activity}/signup", params={"email": email1})

        # Verify only one was removed
        response = client.get("/activities")
        participants = response.json()[activity]["participants"]
        assert email1 not in participants
        assert email2 in participants
        assert len(participants) == count_after_signup - 1
