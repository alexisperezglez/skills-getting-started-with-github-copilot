"""Tests for root redirect endpoint (GET /)."""

import pytest


class TestRedirect:
    """Test suite for the GET / endpoint."""

    def test_root_redirects_to_static_index(self, client):
        """GET / should redirect to the static index HTML."""
        response = client.get("/", follow_redirects=False)
        assert response.status_code in [307, 308]  # Temporary redirect
        assert response.headers["location"].endswith("/static/index.html")

    def test_root_redirect_is_accessible(self, client):
        """Following the redirect from GET / should return the index page."""
        response = client.get("/", follow_redirects=True)
        assert response.status_code == 200
        # The static file should contain HTML
        assert "text/html" in response.headers.get("content-type", "")
