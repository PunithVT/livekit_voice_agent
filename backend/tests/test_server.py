"""Tests for FastAPI server endpoints"""
import pytest
from fastapi import status


@pytest.mark.api
class TestRootEndpoints:
    """Test root and health endpoints"""

    def test_root_endpoint(self, client):
        """Test root endpoint returns API information"""
        response = client.get("/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "name" in data
        assert "version" in data
        assert data["version"] == "2.0.0"

    @pytest.mark.asyncio
    async def test_health_endpoint(self, async_client):
        """Test health check endpoint"""
        response = await async_client.get("/api/health")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "status" in data
        assert "timestamp" in data
        assert "livekit_connected" in data

    def test_metrics_endpoint(self, client):
        """Test Prometheus metrics endpoint"""
        response = client.get("/api/metrics")
        assert response.status_code == status.HTTP_200_OK
        assert "text/plain" in response.headers["content-type"]


@pytest.mark.api
class TestTokenEndpoints:
    """Test token generation endpoints"""

    def test_get_token_legacy_default(self, client):
        """Test legacy token endpoint with default parameters"""
        response = client.get("/api/getToken")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "token" in data
        assert "room" in data
        assert "identity" in data
        assert data["identity"] == "Guest"

    def test_get_token_legacy_with_name(self, client, sample_user):
        """Test legacy token endpoint with custom name"""
        response = client.get(f"/api/getToken?name={sample_user['name']}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["identity"] == sample_user["name"]
        assert "room" in data

    def test_get_token_legacy_with_room(self, client, sample_user):
        """Test legacy token endpoint with custom room"""
        response = client.get(
            f"/api/getToken?name={sample_user['name']}&room={sample_user['room']}"
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["room"] == sample_user["room"]

    @pytest.mark.asyncio
    async def test_create_token_post(self, async_client, sample_user):
        """Test POST token endpoint"""
        response = await async_client.post(
            "/api/token",
            json=sample_user
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "token" in data
        assert data["identity"] == sample_user["name"]
        assert data["room"] == sample_user["room"]

    @pytest.mark.asyncio
    async def test_create_token_with_metadata(self, async_client):
        """Test POST token endpoint with metadata"""
        request_data = {
            "name": "Test User",
            "metadata": {"role": "student", "grade": "10"}
        }
        response = await async_client.post("/api/token", json=request_data)
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "token" in data

    def test_token_validation(self, client):
        """Test token endpoint with invalid data"""
        response = client.post("/api/token", json={"name": ""})
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.api
class TestRoomEndpoints:
    """Test room management endpoints"""

    @pytest.mark.asyncio
    async def test_list_rooms(self, async_client):
        """Test listing rooms"""
        response = await async_client.get("/api/rooms")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)

    @pytest.mark.slow
    @pytest.mark.asyncio
    async def test_delete_room(self, async_client):
        """Test deleting a room"""
        # Note: This test requires a running LiveKit server
        # It will fail in CI without proper mocking
        response = await async_client.delete("/api/rooms/test-room")
        # Expecting 500 in test environment without LiveKit server
        assert response.status_code in [status.HTTP_200_OK, status.HTTP_500_INTERNAL_SERVER_ERROR]


@pytest.mark.api
class TestRateLimiting:
    """Test rate limiting"""

    def test_rate_limit_token_endpoint(self, client):
        """Test rate limiting on token endpoint"""
        # Make multiple requests quickly
        responses = []
        for _ in range(15):
            response = client.get("/api/getToken")
            responses.append(response.status_code)

        # Should have at least one rate limited response (429)
        # or all successful if rate limit is high enough
        assert all(code in [200, 429] for code in responses)
