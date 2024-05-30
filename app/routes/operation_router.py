from typing import List
from fastapi import APIRouter, HTTPException, Request
from utils.log import log
from app.models.operation import Operation
from app.services import operations_service

operation_router = APIRouter()


@operation_router.get('/all_operations/{user_id}', response_model=List[Operation])
@log
async def get_operations(request: Request, user_id: int):
    """
    Retrieves all operations for a specific user.

    Parameters:
    - request (Request): The incoming request.
    - user_id (int): ID of the user whose operations are to be fetched.

    Returns:
    - List[Operation]: List of operations for the specified user.

    Raises:
    - HTTPException: If no operations are found for the user.
    """
    try:
        operations = await operations_service.get_all_operations(user_id)
    except Exception as e:
        raise e
    if operations:
        return operations
    else:
        raise HTTPException(status_code=404, detail="No operations found")


@operation_router.get('/{user_id}/{start_date}/{end_date}')
@log
async def get_term(request: Request, user_id: int, start_date: str, end_date: str):
    """
    Retrieves all operations for a specific user within a date range.

    Parameters:
    - request (Request): The incoming request.
    - user_id (int): ID of the user whose operations are to be fetched.
    - start_date (str): Start date of the range in 'YYYY-MM-DD' format.
    - end_date (str): End date of the range in 'YYYY-MM-DD' format.

    Returns:
    - List[Operation]: List of operations for the specified user within the date range.

    Raises:
    - HTTPException: If no operations are found for the user within the specified date range.
    """
    try:
        operations = await operations_service.get_all_operations_between_dates(user_id, start_date, end_date)
    except Exception as e:
        raise e
    if operations:
        return operations
    else:
        raise HTTPException(status_code=404, detail="No operations found")


@operation_router.get('/{operation_id}')
@log
async def get_operation(request: Request, operation_id: int):
    """
    Retrieves a specific operation by its ID.

    Parameters:
    - request (Request): The incoming request.
    - operation_id (int): ID of the operation to retrieve.

    Returns:
    - Operation: The operation with the specified ID.

    Raises:
    - HTTPException: If no operation is found with the provided ID.
    """
    try:
        operation = await operations_service.get_operation_by_id(operation_id)
    except Exception as e:
        raise e
    if operation:
        return operation
    else:
        raise HTTPException(status_code=404, detail="No operation found")


@operation_router.post("/")
@log
async def add_operation(request: Request, operation: Operation):
    """
    Adds a new operation.

    Parameters:
    - request (Request): The incoming request.
    - operation (Operation): The operation data to add.

    Returns:
    - str: Success message if the operation is added successfully.

    Raises:
    - HTTPException: If one or more details of the operation are invalid.
    """
    is_added = await operations_service.add_operation(operation)
    if is_added:
        return "Operation added successfully"
    raise HTTPException(status_code=400, detail="One or more details of the operation are invalid")


@operation_router.put("/{operation_id}")
@log
async def update_operation(request: Request, operation_id: int, operation: Operation):
    """
    Updates an existing operation.

    Parameters:
    - request (Request): The incoming request.
    - operation_id (int): ID of the operation to update.
    - operation (Operation): The updated operation data.

    Returns:
    - str: Success message if the operation is updated successfully.

    Raises:
    - HTTPException: If one or more details of the operation are invalid.
    """
    try:
        is_updated = await operations_service.update_operation(operation_id, operation)
    except Exception as e:
        raise e
    if is_updated:
        return "Operation updated successfully"
    raise HTTPException(status_code=400, detail="One or more details of the operation are invalid")


@operation_router.delete("/{operation_id}")
@log
async def delete_operation(request: Request, operation_id: int):
    """
    Deletes an operation.

    Parameters:
    - request (Request): The incoming request.
    - operation_id (int): ID of the operation to delete.

    Returns:
    - str: Success message if the operation is deleted successfully.

    Raises:
    - HTTPException: If the operation does not exist.
    """
    is_deleted = await operations_service.delete_operation(operation_id)
    if is_deleted:
        return "Operation deleted successfully"
    else:
        raise HTTPException(status_code=404, detail="This operation does not exist")
