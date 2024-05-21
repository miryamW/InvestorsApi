import pytest
from app.models.user import User
from app.services import users_service


@pytest.fixture
def user_data():
    return User(id=1, username="Miryam", password="Mv1813243")


@pytest.mark.asyncio
async def test_signup(user_data):
    assert await users_service.signup(user_data) == True


@pytest.mark.asyncio
async def test_signup_not_valid_username(user_data):
    with pytest.raises(ValueError, match='String should have at least 1 character'):
        await users_service.signup(User(id=1, username="", password="yjuhtgfe34"))


@pytest.mark.asyncio
async def test_signin(user_data):
    assert await users_service.signin(user_data) == True


@pytest.mark.asyncio
async def test_signin_not_valid_username(user_data):
    with pytest.raises(ValueError, match='String should have at least 1 character'):
        await users_service.signin(User(id=1, username="", password="yjuhtgfe34"))


@pytest.mark.asyncio
async def test_signup_not_valid_password(user_data):
    with pytest.raises(ValueError, match='String should have at least 8 character'):
        await users_service.signup(User(id=1, username="Noam", password=""))


@pytest.mark.asyncio
async def test_update_user_profile(user_data):
    assert await users_service.update_user_profile(user_data.id, user_data) == user_data


@pytest.mark.asyncio
async def test_signin_not_valid_password(user_data):
    with pytest.raises(ValueError, match='String should have at least 8 character'):
        await users_service.signin(User(id=1, username="Noam", password=""))


@pytest.mark.asyncio
async def test_update_not_valid_username(user_data):
    last_user_id = await users_service.get_user_id() - 1
    with pytest.raises(ValueError, match='String should have at least 1 character'):
        await users_service.update_user_profile(last_user_id, User(id=last_user_id, username="", password="yjuhtgfe34"))


@pytest.mark.asyncio
async def test_update_not_valid_password(user_data):
    last_user_id = await users_service.get_user_id() - 1
    with pytest.raises(ValueError, match='String should have at least 8 character'):
        await users_service.update_user_profile(last_user_id,User(id=last_user_id, username="Noam", password=""))
