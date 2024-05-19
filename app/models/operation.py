from datetime import datetime
from pydantic import BaseModel


class Revenue(BaseModel):
    id: int
    sum: float
    userId: str
    date: datetime
