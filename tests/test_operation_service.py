import os
import sys

import pytest
from datetime import datetime, timedelta
from app.services import operations_service, users_service
from app.models.operation import Operation
from app.models.operation_type import Operation_type

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def operation_data():
    return Operation(id=1, sum=100.0, userId=3, type=Operation_type.EXPENSE, date=datetime.now())


@pytest.mark.asyncio
async def test_add_operation(operation_data):
    result = await operations_service.add_operation(operation_data)
    assert result is True


@pytest.mark.asyncio
async def test_add_operation_not_valid_sum():
    with pytest.raises(ValueError, match='cannot get negative sum'):
        await operations_service.add_operation(
            Operation(id=1, sum=-56, userId=1, type=Operation_type.EXPENSE, date=datetime.now()))


@pytest.mark.asyncio
async def test_add_operation_not_valid_userId():
    last_user_id = await users_service.get_user_id() - 1
    with pytest.raises(ValueError, match='user does not exist'):
        await operations_service.add_operation(
            Operation(id=1, sum=-56, userId=last_user_id + 10, type=Operation_type.EXPENSE, date=datetime.now()))


@pytest.mark.asyncio
async def test_update_operation(operation_data):
    result = await operations_service.update_operation(operation_data.id, operation_data)
    assert result is True


@pytest.mark.asyncio
async def test_update_operation_not_valid_sum():
    last_operation_id = await operations_service.get_operation_id() - 1
    with pytest.raises(ValueError, match='cannot get negative sum'):
        await operations_service.update_operation(last_operation_id,
                                                  Operation(id=last_operation_id, sum=-56, userId=1,
                                                            type=Operation_type.EXPENSE, date=datetime.now()))


@pytest.mark.asyncio
async def test_update_operation_not_valid_userId():
    last_user_id = await users_service.get_user_id() - 1
    last_operation_id = await operations_service.get_operation_id() - 1
    with pytest.raises(ValueError, match='user does not exist'):
        await operations_service.update_operation(last_operation_id,
                                                  Operation(id=1, sum=-56, userId=last_user_id + 10,
                                                            type=Operation_type.EXPENSE, date=datetime.now()))


@pytest.mark.asyncio
async def test_get_operation_by_id(operation_data):
    date = operation_data.date
    current_id = await operations_service.get_operation_id()
    result = await operations_service.get_operation_by_id(current_id - 1)
    assert {k: v for k, v in result.__dict__.items() if k is not "date"} == {"id": current_id - 1,
                                                                             "sum": operation_data.sum,
                                                                             "userId": operation_data.userId,
                                                                             "type": operation_data.type}


@pytest.mark.asyncio
async def test_get_all_operations(operation_data):
    current_id = await operations_service.get_operation_id() - 1
    result = await operations_service.get_all_operations(3)
    assert current_id in (v["id"] for v in result)


@pytest.mark.asyncio
async def test_get_operations_between_two_dates_for_user(operation_data):
    current_id = await operations_service.get_operation_id() - 1
    result = await operations_service.get_all_operations_between_dates(operation_data.userId, (
            operation_data.date - timedelta(days=1)).strftime('%Y-%m-%d'), (operation_data.date + timedelta(
       days=1)).strftime('%Y-%m-%d'))
    assert current_id in (v.id for v in result)


@pytest.mark.asyncio
async def test_delete():
    current_id = await operations_service.get_operation_id()
    result = await operations_service.delete_operation(current_id)
    assert result is True
