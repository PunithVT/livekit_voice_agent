"""Pytest configuration and fixtures"""
import os
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
import asyncio

# Set test environment variables
os.environ["LIVEKIT_API_KEY"] = "test_api_key"
os.environ["LIVEKIT_API_SECRET"] = "test_api_secret"
os.environ["LIVEKIT_URL"] = "ws://localhost:7880"
os.environ["OPENAI_API_KEY"] = "test_openai_key"

from server import app
from db_driver import DatabaseDriver


@pytest.fixture(scope="session")
def event_loop():
    """Create an event loop for the test session"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def test_app():
    """Create a test FastAPI application"""
    return app


@pytest.fixture
def client(test_app):
    """Create a test client"""
    return TestClient(test_app)


@pytest.fixture
async def async_client(test_app):
    """Create an async test client"""
    async with AsyncClient(app=test_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def test_db():
    """Create a test database"""
    db = DatabaseDriver(db_path=":memory:")
    yield db


@pytest.fixture
def sample_user():
    """Sample user data"""
    return {
        "name": "Test User",
        "room": "test-room-123"
    }


@pytest.fixture
def sample_subtopic():
    """Sample subtopic data"""
    return {
        "topic": "Mathematics",
        "subtopic": "Algebra",
        "content": "Algebra is a branch of mathematics that uses symbols..."
    }
