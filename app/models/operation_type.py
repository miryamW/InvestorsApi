from enum import Enum, unique

@unique
class Operation_type(str, Enum):
    """
    Enumeration representing the type of operation.

    Attributes:
    - EXPENSE: Represents an expense operation.
    - REVENUE: Represents a revenue operation.
    """

    EXPENSE = "expense",
    REVENUE = "revenue"
