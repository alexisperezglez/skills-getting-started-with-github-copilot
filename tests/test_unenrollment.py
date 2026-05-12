"""Tests for student unenrollment endpoint (POST /activities/{activity_name}/unregister)."""

import pytest


class TestUnenrollment:
    """Test suite for the POST /activities/{name}/unregister endpoint."""

    def test_unregister_success(self, client, reset_activities):
        """Student can successfully unregister from an activity."""
        email = "michael@mergington.edu"
        response = client.post(
            "/activities/Chess Club/unregister",
            params={"email": email}
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert "Chess Club" in data["message"]

    def test_unregister_removes_participant(self, client, reset_activities):
        """Unregister successfully removes student from activity's participant list."""
        email = "michael@mergington.edu"
        
        # Verify student is enrolled
        response = client.get("/activities")
        initial_count = len(response.json()["Chess Club"]["participants"])
        assert email in response.json()["Chess Club"]["participants"]
        
        # Unregister
        client.post(
            "/activities/Chess Club/unregister",
            params={"email": email}
        )
        
        # Verify student was removed
        response = client.get("/activities")
        final_count = len(response.json()["Chess Club"]["participants"])
        assert final_count == initial_count - 1
        assert email not in response.json()["Chess Club"]["participants"]

    def test_unregister_nonexistent_activity_returns_404(self, client, reset_activities):
        """Attempting to unregister from non-existent activity returns 404."""
        response = client.post(
            "/activities/Nonexistent Activity/unregister",
            params={"email": "student@mergington.edu"}
        )
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_unregister_not_enrolled_returns_400(self, client, reset_activities):
        """Attempting to unregister without enrollment returns 400."""
        # Use an email not enrolled in Chess Club
        response = client.post(
            "/activities/Chess Club/unregister",
            params={"email": "not.enrolled@mergington.edu"}
        )
        assert response.status_code == 400
        assert "not registered" in response.json()["detail"].lower()

    def test_unregister_frees_up_spot(self, client, full_activity):
        """Unregistering frees up a spot in a full activity."""
        activity_name = full_activity
        enrolled_email = "student1@mergington.edu"
        new_email = "new.student@mergington.edu"
        
        # Verify full
        response = client.get("/activities")
        initial_count = len(response.json()[activity_name]["participants"])
        assert initial_count == 2  # At capacity
        
        # Unregister one student
        response = client.post(
            f"/activities/{activity_name}/unregister",
            params={"email": enrolled_email}
        )
        assert response.status_code == 200
        
        # Verify spot is freed
        response = client.get("/activities")
        assert len(response.json()[activity_name]["participants"]) == 1
        
        # New student should now be able to sign up
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": new_email}
        )
        assert response.status_code == 200

    def test_unregister_from_multiple_activities(self, client, reset_activities):
        """Student can unregister from multiple activities independently."""
        email = "michael@mergington.edu"
        
        # Verify in Chess Club
        response = client.get("/activities")
        assert email in response.json()["Chess Club"]["participants"]
        
        # Unregister from Chess Club
        response = client.post(
            "/activities/Chess Club/unregister",
            params={"email": email}
        )
        assert response.status_code == 200
        
        # Verify removed from Chess Club
        response = client.get("/activities")
        assert email not in response.json()["Chess Club"]["participants"]
        
        # Sign up for another activity
        response = client.post(
            "/activities/Programming Class/signup",
            params={"email": email}
        )
        assert response.status_code == 200
        
        # Unregister from new activity
        response = client.post(
            "/activities/Programming Class/unregister",
            params={"email": email}
        )
        assert response.status_code == 200
        
        # Verify removed from all
        response = client.get("/activities")
        assert email not in response.json()["Programming Class"]["participants"]
