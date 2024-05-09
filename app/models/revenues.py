

from dataclasses import Field
from typing import Optional

from pydantic import BaseModel


class Revenue(BaseModel):
    id: int
    sum: float
    userId: str
