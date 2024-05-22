from datetime import datetime
from pydantic import BaseModel, field_validator
from app.services import users_service
from app.models.operation_type import Operation_type


class Operation(BaseModel):
    id: int
    sum: float
    userId: int
    type: Operation_type
    date: datetime

    @field_validator('sum')
    def check_sum(cls, sum):
        if sum < 0:
            raise ValueError('cannot get negative sum')
        return sum

    @field_validator('userId')
    def check_user_id(cls, userId):
        user = users_service.get_user_by_id(userId)
        if not user:
            raise ValueError('user does not exist')
        return userId


class Config:
    use_enum_values = True
