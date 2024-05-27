import pytest
from fastapi.testclient import TestClient

from app.models.user import User
from app.routes.user_router import user_router
from app.services import users_service
import pytest_asyncio
import httpx

# Create a TestClient instance for the user_router.
client = TestClient(user_router)


# Define a fixture that provides sample user data.
@pytest.fixture
def user_data():
    """
    Fixture to provide sample user data for testing.

    Returns:
        User: A User object with predefined attributes.
    """
    return User(id=1, username="test", password="test12345678")


# Define an async fixture that provides a user ID.
@pytest_asyncio.fixture
async def user_id():
    """
    Async fixture to get a user ID from the users_service.

    Returns:
        int: The ID of the user.
    """
    id = await users_service.get_user_id()
    return id


# Test the user signup functionality.
def test_signup(user_data):
    """
    Test the user signup endpoint.

    Args:
        user_data (User): Sample user data provided by the user_data fixture.
    """
    response = client.post("/signUp", json=user_data.__dict__)
    assert response.status_code == 200


# Test the user signin functionality.
def test_signin(user_data):
    """
    Test the user signin endpoint.

    Args:
        user_data (User): Sample user data provided by the user_data fixture.
    """
    response = client.post("/signIn", json=user_data.__dict__)
    assert response.status_code == 200


# Test the user profile update functionality.
@pytest.mark.asyncio
async def test_update_profile(user_id, user_data):
    """
    Test the user profile update endpoint.

    Args:
        user_id (int): The ID of the user provided by the user_id fixture.
        user_data (User): Sample user data provided by the user_data fixture.
    """
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8080/users") as async_client:
        response = await async_client.put(f"/{user_id - 1}",
                                          json=user_data.__dict__)
    assert response.status_code == 200
