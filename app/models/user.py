from pydantic import BaseModel, constr


class User(BaseModel):
    id: int
    username: constr(min_length=1, pattern='^[a-zA-Z]+$')
    password: constr(min_length=8, pattern='^[^\\s]+$')
