from pymongo import DESCENDING
from app.services.db_service import synchronise_users
from app.models.user import User
from app.services.db_service import users


async def signin(user: User):
    """sign in with user name and password"""

    existing_user = await users.find_one({"username": user.username, "password": user.password})
    if existing_user:
        return True
    return False


async def signup(new_user: User):
    """sign up user"""

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
    """update user's details"""

    await users.update_one({"id": user_id}, {"$set": {"username": user.username, "password": user.password}})
    user_updated = await users.find_one({"id": user_id, "username": user.username, "password": user.password})
    return User(**user_updated)


async def get_user_id():
    """get the next user id that available"""

    max_id_user = await users.find_one({}, sort=[("id", DESCENDING)])
    if max_id_user:
        return max_id_user["id"] + 1
    else:
        return 1


def get_user_by_id(user_id: int):
    """"get user by id"""

    return synchronise_users.find_one({"id": user_id})
