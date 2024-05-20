from pymongo import DESCENDING

from app.models.user import User
from app.services.db_service import users

"""sign in with user name and password"""


async def signin(user: User):
    existing_user = await users.find_one({"username": user.username, "password": user.password})
    if existing_user:
        return True
    return False


"""sign up user"""


async def signup(new_user: User):
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


"""update user's details"""


async def update_user_profile(user_id: int, user: User):
    await users.update_one({"id": user_id}, {"$set": {"username": user.username, "password": user.password}})
    user_updated = users.find_one({"id": user_id, "username": user.username, "password": user.password})
    return user_updated


"""get the next user id that available"""


async def get_user_id():
    max_id_user = await users.find_one({}, sort=[("id", DESCENDING)])
    if max_id_user:
        return max_id_user["id"] + 1
    else:
        return 1


""""get user by id"""


async def get_user_by_id(user_id: int):
    return await users.find_one({"id": user_id})
