"""Tests for student enrollment endpoint (POST /activities/{activity_name}/signup)."""

import pytest


class TestEnrollment:
    """Test suite for the POST /activities/{name}/signup endpoint."""

    def test_signup_success(self, client, reset_activities, test_email):
        """Student can successfully sign up for an activity."""
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": test_email}
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert test_email in data["message"]
        assert "Chess Club" in data["message"]

    def test_signup_adds_participant(self, client, reset_activities, test_email):
        """Signup successfully adds the student to the activity's participant list."""
        # Verify student not yet enrolled
        response = client.get("/activities")
        initial_count = len(response.json()["Chess Club"]["participants"])
        
        # Sign up the student
        client.post(
            "/activities/Chess Club/signup",
            params={"email": test_email}
        )
        
        # Verify student was added
        response = client.get("/activities")
        final_count = len(response.json()["Chess Club"]["participants"])
        assert final_count == initial_count + 1
        assert test_email in response.json()["Chess Club"]["participants"]

    def test_signup_nonexistent_activity_returns_404(self, client, reset_activities, test_email):
        """Attempting to sign up for non-existent activity returns 404."""
        response = client.post(
            "/activities/Nonexistent Activity/signup",
            params={"email": test_email}
        )
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_signup_duplicate_email_returns_400(self, client, reset_activities):
        """Attempting to sign up with already-enrolled email returns 400."""
        # Use an already enrolled student
        existing_email = "michael@mergington.edu"
        response = client.post(
            "/activities/Chess Club/signup",
            params={"email": existing_email}
        )
        assert response.status_code == 400
        assert "already signed up" in response.json()["detail"]

    def test_signup_full_activity_returns_400(self, client, full_activity, test_email):
        """Attempting to sign up for full activity returns 400."""
        response = client.post(
            f"/activities/{full_activity}/signup",
            params={"email": test_email}
        )
        assert response.status_code == 400
        assert "full" in response.json()["detail"].lower()

    def test_signup_fills_activity_to_capacity(self, client, reset_activities):
        """Can sign up students until activity reaches capacity."""
        # Use Tennis Club which has max 12, currently has 2
        activity_name = "Tennis Club"
        capacity = 12
        currently_enrolled = 2
        
        # Sign up 10 more students (to reach capacity)
        for i in range(currently_enrolled, capacity):
            email = f"student{i}@mergington.edu"
            response = client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )
            assert response.status_code == 200
        
        # Verify we're at capacity
        response = client.get("/activities")
        assert len(response.json()[activity_name]["participants"]) == capacity
        
        # Try to sign up one more - should fail
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": "overflow@mergington.edu"}
        )
        assert response.status_code == 400

    def test_signup_with_multiple_activities(self, client, reset_activities, test_email):
        """Student can sign up for multiple different activities."""
        # Sign up for first activity
        response1 = client.post(
            "/activities/Chess Club/signup",
            params={"email": test_email}
        )
        assert response1.status_code == 200
        
        # Sign up for second activity
        response2 = client.post(
            "/activities/Programming Class/signup",
            params={"email": test_email}
        )
        assert response2.status_code == 200
        
        # Verify in both activities
        response = client.get("/activities")
        assert test_email in response.json()["Chess Club"]["participants"]
        assert test_email in response.json()["Programming Class"]["participants"]
