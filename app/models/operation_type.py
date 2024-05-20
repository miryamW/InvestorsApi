import json
from enum import Enum, unique


@unique
class Operation_type(str, Enum):
    EXPENSE = "expense",
    REVENUE = "revenue"
