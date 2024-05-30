from fastapi import APIRouter, HTTPException, Request
from utils.log import log
from app.services import users_service
from app.models.user import User

user_router = APIRouter()


@user_router.post("/sign_in")
@log
async def signin(request: Request, user: User):
    """
    Signs in a user with the provided credentials.

    Parameters:
    - request (Request): The incoming request.
    - user (User): The user data including username and password.

    Returns:
    - str: Success message if sign-in is successful.

    Raises:
    - HTTPException: If the user does not exist.
    """
    is_sign_in = await users_service.signin(user)
    if is_sign_in:
        return "You were signed in successfully"
    raise HTTPException(status_code=404, detail="This user does not exist")


@user_router.post("/sign_up")
@log
async def signup(request: Request, user: User):
    """
    Registers a new user with the provided details.

    Parameters:
    - request (Request): The incoming request.
    - user (User): The user data including username and password.

    Returns:
    - str: Success message if sign-up is successful.

    Raises:
    - HTTPException: If one or more details are invalid.
    """
    is_sign_up = await users_service.signup(user)
    if is_sign_up:
        return "You were signed up successfully"
    raise HTTPException(status_code=400, detail="One or more of your details was not valid, please try again")


@user_router.put("/{user_id}")
@log
async def update_profile(request: Request, user_id: int, user: User):
    """
    Updates the profile of an existing user.

    Parameters:
    - request (Request): The incoming request.
    - user_id (int): The ID of the user to update.
    - user (User): The updated user data including username and password.

    Returns:
    - str: Success message if the profile is updated successfully.

    Raises:
    - HTTPException: If one or more details are invalid.
    """
    is_updated = await users_service.update_user_profile(user_id, user)
    if is_updated:
        return "Your profile was updated successfully"
    raise HTTPException(status_code=400, detail="One or more of your details was not valid, please try again")
