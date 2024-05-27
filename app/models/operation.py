from datetime import datetime
from pydantic import BaseModel, Field, validator, field_validator
from app.services import users_service
from app.models.operation_type import Operation_type


class Operation(BaseModel):
    """
    Represents an operation.

    Attributes:
    - id (int): The unique identifier for the operation.
    - sum (float): The monetary value of the operation.
    - userId (int): The ID of the user associated with the operation.
    - type (Operation_type): The type of the operation (expense or revenue).
    - date (datetime): The date and time when the operation occurred.
    """

    id: int
    sum: float
    userId: int
    type: Operation_type
    date: datetime

    @field_validator('sum')
    def check_sum(cls, sum):
        """
        Validates that the sum of the operation is non-negative.

        Parameters:
        - sum (float): The sum of the operation.

        Raises:
        - ValueError: If the sum is negative.

        Returns:
        - float: The validated sum.
        """
        if sum < 0:
            raise ValueError('Sum cannot be negative')
        return sum

    @field_validator('userId')
    def check_user_id(cls, userId):
        """
        Validates that the user associated with the operation exists.

        Parameters:
        - userId (int): The ID of the user.

        Raises:
        - ValueError: If the user does not exist.

        Returns:
        - int: The validated user ID.
        """
        user = users_service.get_user_by_id(userId)
        if not user:
            raise ValueError('User does not exist')
        return userId

    class Config:
        use_enum_values = True
