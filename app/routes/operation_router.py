from typing import List
from fastapi import APIRouter, HTTPException, Request
from app.middlewares.log import log
from app.models.operation import Operation
from app.services import operations_service

operation_router = APIRouter()


@operation_router.get('/operations/{user_id}', response_model=List[Operation])
@log
async def get_operations(request: Request, user_id):
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
    try:
        operations = await operations_service.get_all_operations_between_dates(user_id, start_date, end_date)
    except Exception as e:
        raise e
    if operations:
        return operations
    else:
        raise HTTPException(status_code=404, detail="No operations found")


@operation_router.get('/{id}')
@log
async def get_operation(request: Request, operation_id: int):
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
    is_added = await operations_service.add_operation(operation)
    if is_added:
        return "operation added successfully"
    raise HTTPException(status_code=404, detail="one or more of your details was not valid, please try again")


@operation_router.put("/{id}")
@log
async def update_operation(request: Request, operation_id: int, operation: Operation):
    try:
        is_updated = await operations_service.update_operation(operation_id, operation)
    except Exception as e:
        raise e
    if is_updated:
        return "operation were updated successfully"
    raise HTTPException(status_code=400, detail="one or more of your details was not valid, please try again")


@operation_router.delete("/{id}")
@log
async def delete_operation(request: Request, operation_id: int):
    is_deleted = await operations_service.delete_operation(operation_id)
    if is_deleted:
        return "operation were deleted successfully"
    else:
        raise HTTPException(status_code=400, detail="this operation is not exist yes")
