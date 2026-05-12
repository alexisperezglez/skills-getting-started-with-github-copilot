"""Tests for activity listing endpoint (GET /activities)."""

import pytest


class TestActivityListing:
    """Test suite for the GET /activities endpoint."""

    def test_get_activities_returns_all_activities(self, client, reset_activities):
        """GET /activities should return all activities."""
        response = client.get("/activities")
        assert response.status_code == 200
        data = response.json()
        
        # Verify all expected activities are present
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Tennis Club",
            "Drama Club",
            "Art Studio",
            "Debate Team",
            "Science Club"
        ]
        for activity_name in expected_activities:
            assert activity_name in data

    def test_get_activities_response_structure(self, client, reset_activities):
        """GET /activities returns data with correct structure for each activity."""
        response = client.get("/activities")
        data = response.json()
        
        # Check that each activity has required fields
        for activity_name, activity_data in data.items():
            assert isinstance(activity_data, dict)
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data
            assert isinstance(activity_data["participants"], list)

    def test_get_activities_participant_count_reflects_enrollment(self, client, reset_activities):
        """GET /activities shows correct participant count."""
        response = client.get("/activities")
        data = response.json()
        
        # Verify participant counts match expectations
        assert len(data["Chess Club"]["participants"]) == 2
        assert "michael@mergington.edu" in data["Chess Club"]["participants"]
        assert "daniel@mergington.edu" in data["Chess Club"]["participants"]
        
        assert len(data["Programming Class"]["participants"]) == 2
        assert len(data["Basketball Team"]["participants"]) == 1

    def test_get_activities_returns_json(self, client, reset_activities):
        """GET /activities returns valid JSON."""
        response = client.get("/activities")
        assert response.headers["content-type"].startswith("application/json")
        # Should not raise an exception
        data = response.json()
        assert isinstance(data, dict)
