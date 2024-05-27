from pymongo import DESCENDING
from app.services.db_service import synchronise_users
from app.models.user import User
from app.services.db_service import users


async def signin(user: User):
    """
    Sign in a user with the provided username and password.

    Args:
        user (User): The user object containing username and password.

    Returns:
        bool: True if sign in successful, False otherwise.
    """

    existing_user = await users.find_one({"username": user.username, "password": user.password})
    if existing_user:
        return True
    return False


async def signup(new_user: User):
    """
    Sign up a new user with the provided username and password.

    Args:
        new_user (User): The user object containing username and password for the new user.

    Returns:
        bool: True if sign up successful, False otherwise.
    """

    user_id = await get_user_id()
    users.insert_one({
        "id": user_id,
        "username": new_user.username,
        "password": new_user.password
    })
    new_user_created = await users.find_one({"id": user_id})
    if new_user_created:
        return True
    return False


async def update_user_profile(user_id: int, user: User):
    """
    Update user's details with the provided user ID.

    Args:
        user_id (int): The ID of the user to update.
        user (User): The user object containing updated details.

    Returns:
        User: The updated user object.
    """

    await users.update_one({"id": user_id}, {"$set": {"username": user.username, "password": user.password}})
    user_updated = await users.find_one({"id": user_id, "username": user.username, "password": user.password})
    return User(**user_updated)


async def get_user_id():
    """
    Get the next available user ID.

    Returns:
        int: The next available user ID.
    """

    max_id_user = await users.find_one({}, sort=[("id", DESCENDING)])
    if max_id_user:
        return max_id_user["id"] + 1
    else:
        return 1


def get_user_by_id(user_id: int):
    """
    Retrieve a user by their ID.

    Args:
        user_id (int): The ID of the user to retrieve.

    Returns:
        dict: The user document from the database.
    """

    return synchronise_users.find_one({"id": user_id})
