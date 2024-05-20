from datetime import datetime
from fastapi import HTTPException
from pymongo import DESCENDING
from app.models.operation import Operation
from app.services.db_service import operations
from app.services import users_service

"""get operation by id"""


async def get_operation_by_id(operation_id):
    operation =await  operations.find_one({"id": operation_id})
    return Operation(**operation)


"""get all operations for specific user"""


async def get_all_operations(user_id: int):
    all_operations = await operations.find({"userId": user_id})
    operations_list = [Operation(**operation) for operation in list(all_operations)]
    return operations_list


"""get all operations for specific user between dates range"""


async def get_all_operations_between_dates(user_id: int, start_date: str, end_date: str):
    start_date_time = datetime.strptime(start_date, "%Y-%m-%d")
    end_date_time = datetime.strptime(end_date, "%Y-%m-%d")
    operations_in_range = await operations.find({"userId": user_id, "date": {"$gte": start_date_time, "$lte": end_date_time}})
    operations_in_range_list = [Operation(**operation) for operation in list(operations_in_range)]
    return operations_in_range_list


"""add operation to db"""


async def add_operation(operation: Operation):
    operation_id = await get_operation_id()
    operations.insert_one({
        "id": operation_id,
        "sum": operation.sum,
        "userId": operation.userId,
        "type": operation.type.value,
        "date": datetime.now()
    })
    new_operation_created = await operations.find_one({"id": operation_id})
    if new_operation_created:
        return True
    return False


"""update operation properties"""


async def update_operation(operation_id: int, operation: Operation):
    await operations.update_one({"id": operation_id}, {
        "$set": {"sum": operation.sum, "userId": operation.userId, "type": operation.type, "date": operation.date}})
    updated_operation = operations.find_one({"sum": operation.sum, "userId": operation.userId, "type": operation.type,
                                                 "date": operation.date})
    if updated_operation:
        return True
    return False


"""delete operation"""


async def delete_operation(operation_id: int):
    await operations.delete_one({"id": operation_id})
    if get_operation_by_id(operation_id):
        return True
    return False


"""get next operation id"""


async def get_operation_id():
    max_id_operation = await operations.find_one({}, sort=[("id", DESCENDING)])
    if max_id_operation:
        return max_id_operation["id"] + 1
    else:
        return 1
