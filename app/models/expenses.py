from dataclasses import Field
from typing import Optional

from pydantic import BaseModel


class Expense(BaseModel):
    id: int
    sum: float
    userId: int
