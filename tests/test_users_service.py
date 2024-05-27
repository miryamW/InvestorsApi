import os
import sys
import pytest
from app.models.user import User
from app.services import users_service

# Add the parent directory to the system path to allow imports from it.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# Define a fixture that provides sample user data.
@pytest.fixture
def user_data():
    """
    Fixture to provide sample user data for testing.

    Returns:
        User: A User object with predefined attributes.
    """
    return User(id=1, username="Miryam", password="Mv1813243")


# Test the user signup functionality.
@pytest.mark.asyncio
@pytest.mark.order(1)
async def test_signup(user_data):
    """
    Test the user signup service function.

    Args:
        user_data (User): Sample user data provided by the user_data fixture.
    """
    assert await users_service.signup(user_data) is True


# Test signing up with an invalid (empty) username.
@pytest.mark.asyncio
@pytest.mark.order(2)
async def test_signup_not_valid_username(user_data):
    """
    Test signing up with an invalid (empty) username.
    """
    with pytest.raises(ValueError, match='String should have at least 1 character'):
        await users_service.signup(User(id=1, username="", password="yjuhtgfe34"))


# Test the user signin functionality.
@pytest.mark.asyncio
@pytest.mark.order(3)
async def test_signin(user_data):
    """
    Test the user signin service function.

    Args:
        user_data (User): Sample user data provided by the user_data fixture.
    """
    assert await users_service.signin(user_data) is True


# Test signing in with an invalid (empty) username.
@pytest.mark.asyncio
@pytest.mark.order(4)
async def test_signin_not_valid_username(user_data):
    """
    Test signing in with an invalid (empty) username.
    """
    with pytest.raises(ValueError, match='String should have at least 1 character'):
        await users_service.signin(User(id=1, username="", password="yjuhtgfe34"))


# Test signing up with an invalid (empty) password.
@pytest.mark.asyncio
@pytest.mark.order(5)
async def test_signup_not_valid_password(user_data):
    """
    Test signing up with an invalid (empty) password.
    """
    with pytest.raises(ValueError, match='String should have at least 8 character'):
        await users_service.signup(User(id=1, username="Noam", password=""))


# Test updating the user profile.
@pytest.mark.asyncio
@pytest.mark.order(6)
async def test_update_user_profile(user_data):
    """
    Test updating the user profile service function.

    Args:
        user_data (User): Sample user data provided by the user_data fixture.
    """
    assert await users_service.update_user_profile(user_data.id, user_data) == user_data


# Test signing in with an invalid (empty) password.
@pytest.mark.asyncio
@pytest.mark.order(7)
async def test_signin_not_valid_password(user_data):
    """
    Test signing in with an invalid (empty) password.
    """
    with pytest.raises(ValueError, match='String should have at least 8 character'):
        await users_service.signin(User(id=1, username="Noam", password=""))


# Test updating the user profile with an invalid (empty) username.
@pytest.mark.asyncio
@pytest.mark.order(8)
async def test_update_not_valid_username(user_data):
    """
    Test updating the user profile with an invalid (empty) username.
    """
    last_user_id = await users_service.get_user_id() - 1
    with pytest.raises(ValueError, match='String should have at least 1 character'):
        await users_service.update_user_profile(last_user_id, User(id=last_user_id, username="", password="yjuhtgfe34"))


# Test updating the user profile with an invalid (empty) password.
@pytest.mark.asyncio
@pytest.mark.order(9)
async def test_update_not_valid_password(user_data):
    """
    Test updating the user profile with an invalid (empty) password.
    """
    last_user_id = await users_service.get_user_id() - 1
    with pytest.raises(ValueError, match='String should have at least 8 character'):
        await users_service.update_user_profile(last_user_id, User(id=last_user_id, username="Noam", password=""))
