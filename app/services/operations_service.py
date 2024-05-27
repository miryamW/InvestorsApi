from datetime import datetime
from pymongo import DESCENDING
from app.models.operation import Operation
from app.services.db_service import operations


async def get_operation_by_id(operation_id):
    """
    Retrieve an operation by its ID.

    Args:
        operation_id (int): The ID of the operation to retrieve.

    Returns:
        Operation: The operation object if found, else None.
    """

    operation = await operations.find_one({"id": operation_id})
    if operation:
        return Operation(**operation)
    return None


async def get_all_operations(user_id: int):
    """
    Retrieve all operations for a specific user.

    Args:
        user_id (int): The ID of the user.

    Returns:
        List[Operation]: A list of operation objects.
    """

    cursor = operations.find({"userId": user_id})
    all_operations = await cursor.to_list(None)
    return [Operation(**operation) for operation in all_operations]


async def get_all_operations_between_dates(user_id: int, start_date: str, end_date: str):
    """
    Retrieve all operations for a specific user between a date range.

    Args:
        user_id (int): The ID of the user.
        start_date (str): The start date of the range in format 'YYYY-MM-DD'.
        end_date (str): The end date of the range in format 'YYYY-MM-DD'.

    Returns:
        List[Operation]: A list of operation objects.
    """

    start_date_time = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_time = datetime.strptime(end_date, "%Y-%m-%d")
    cursor = operations.find(
        {"userId": user_id, "date": {"$gte": start_date_time, "$lte": end_date_time}}
    )
    operations_in_range_list = await cursor.to_list(None)

    return [Operation(**operation) for operation in operations_in_range_list]


async def add_operation(operation: Operation):
    """
    Add an operation to the database.

    Args:
        operation (Operation): The operation object to add.

    Returns:
        bool: True if operation added successfully, else False.
    """

    operation_id = await get_operation_id()
    operations.insert_one({
        "id": operation_id,
        "sum": operation.sum,
        "userId": operation.userId,
        "type": operation.type.value,
        "date": operation.date
    })
    new_operation_created = await operations.find_one({"id": operation_id})
    if new_operation_created:
        return True
    return False


async def update_operation(operation_id: int, operation: Operation):
    """
    Update properties of an operation.

    Args:
        operation_id (int): The ID of the operation to update.
        operation (Operation): The updated operation object.

    Returns:
        bool: True if operation updated successfully, else False.
    """

    await operations.update_one({"id": operation_id}, {
        "$set": {"sum": operation.sum, "userId": operation.userId, "type": operation.type.value,
                 "date": operation.date}})
    updated_operation = operations.find_one({"id": operation_id})
    if updated_operation:
        return True
    return False


async def delete_operation(operation_id: int):
    """
    Delete an operation.

    Args:
        operation_id (int): The ID of the operation to delete.

    Returns:
        bool: True if operation deleted successfully, else False.
    """

    await operations.delete_one({"id": operation_id})
    if get_operation_by_id(operation_id):
        return True
    return False


async def get_operation_id():
    """
    Get the next available operation ID.

    Returns:
        int: The next operation ID.
    """

    max_id_operation = await operations.find_one({}, sort=[("id", DESCENDING)])
    if max_id_operation:
        return max_id_operation["id"] + 1
    else:
        return 1
