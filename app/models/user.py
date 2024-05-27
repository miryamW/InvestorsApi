from pydantic import BaseModel, constr


class User(BaseModel):
    """
    Model representing a user entity.

    Attributes:
    - id (int): The unique identifier of the user.
    - username (str): The username of the user. It must have at least one character and consist of only letters.
    - password (str): The password of the user. It must have at least eight characters and no whitespace.
    """

    id: int
    username: constr(min_length=1, pattern='^[a-zA-Z]+$')
    password: constr(min_length=8, pattern='^[^\\s]+$')
