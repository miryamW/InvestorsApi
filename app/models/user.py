from dataclasses import Field
from typing import Optional

from pydantic import BaseModel


class User(BaseModel):
    id: int
    username: str
    password: str
