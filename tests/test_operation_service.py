import os
import sys
import pytest
from datetime import datetime, timedelta
from app.services import operations_service, users_service
from app.models.operation import Operation
from app.models.operation_type import Operation_type

# Add the parent directory to the system path to allow imports from it.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# Define a fixture that provides sample operation data.
@pytest.fixture
def operation_data():
    """
    Fixture to provide sample operation data for testing.

    Returns:
        Operation: An Operation object with predefined attributes.
    """
    return Operation(id=1, sum=100.0, userId=3, type=Operation_type.EXPENSE, date=datetime.now())


# Test the addition of a new operation.
@pytest.mark.asyncio
async def test_add_operation(operation_data):
    """
    Test the service function to add a new operation.

    Args:
        operation_data (Operation): Sample operation data provided by the operation_data fixture.
    """
    result = await operations_service.add_operation(operation_data)
    assert result is True


# Test adding an operation with an invalid (negative) sum.
@pytest.mark.asyncio
async def test_add_operation_not_valid_sum():
    """
    Test adding an operation with an invalid (negative) sum.
    """
    with pytest.raises(ValueError, match='cannot get negative sum'):
        await operations_service.add_operation(
            Operation(id=1, sum=-56, userId=1, type=Operation_type.EXPENSE, date=datetime.now()))


# Test adding an operation with a non-existent user ID.
@pytest.mark.asyncio
async def test_add_operation_not_valid_userId():
    """
    Test adding an operation with a non-existent user ID.
    """
    last_user_id = await users_service.get_user_id() - 1
    with pytest.raises(ValueError, match='user does not exist'):
        await operations_service.add_operation(
            Operation(id=1, sum=-56, userId=last_user_id + 10, type=Operation_type.EXPENSE, date=datetime.now()))


# Test updating an existing operation.
@pytest.mark.asyncio
async def test_update_operation(operation_data):
    """
    Test the service function to update an existing operation.

    Args:
        operation_data (Operation): Sample operation data provided by the operation_data fixture.
    """
    result = await operations_service.update_operation(operation_data.id, operation_data)
    assert result is True


# Test updating an operation with an invalid (negative) sum.
@pytest.mark.asyncio
async def test_update_operation_not_valid_sum():
    """
    Test updating an operation with an invalid (negative) sum.
    """
    last_operation_id = await operations_service.get_operation_id() - 1
    with pytest.raises(ValueError, match='cannot get negative sum'):
        await operations_service.update_operation(last_operation_id,
                                                  Operation(id=last_operation_id, sum=-56, userId=1,
                                                            type=Operation_type.EXPENSE, date=datetime.now()))


# Test updating an operation with a non-existent user ID.
@pytest.mark.asyncio
async def test_update_operation_not_valid_userId():
    """
    Test updating an operation with a non-existent user ID.
    """
    last_user_id = await users_service.get_user_id() - 1
    last_operation_id = await operations_service.get_operation_id() - 1
    with pytest.raises(ValueError, match='user does not exist'):
        await operations_service.update_operation(last_operation_id,
                                                  Operation(id=1, sum=-56, userId=last_user_id + 10,
                                                            type=Operation_type.EXPENSE, date=datetime.now()))


# Test retrieving an operation by its ID.
@pytest.mark.asyncio
async def test_get_operation_by_id(operation_data):
    """
    Test retrieving an operation by its ID.

    Args:
        operation_data (Operation): Sample operation data provided by the operation_data fixture.
    """
    current_id = await operations_service.get_operation_id()
    result = await operations_service.get_operation_by_id(current_id - 1)
    assert {k: v for k, v in result.__dict__.items() if k != "date"} == {
        "id": current_id - 1,
        "sum": operation_data.sum,
        "userId": operation_data.userId,
        "type": operation_data.type
    }


# Test retrieving all operations for a specific user.
@pytest.mark.asyncio
async def test_get_all_operations(operation_data):
    """
    Test retrieving all operations for a specific user.

    Args:
        operation_data (Operation): Sample operation data provided by the operation_data fixture.
    """
    current_id = await operations_service.get_operation_id() - 1
    result = await operations_service.get_all_operations(3)
    assert current_id in (v["id"] for v in result)


# Test retrieving operations between two dates for a specific user.
@pytest.mark.asyncio
async def test_get_operations_between_two_dates_for_user(operation_data):
    """
    Test retrieving operations between two dates for a specific user.

    Args:
        operation_data (Operation): Sample operation data provided by the operation_data fixture.
    """
    current_id = await operations_service.get_operation_id() - 1
    result = await operations_service.get_all_operations_between_dates(
        operation_data.userId,
        (operation_data.date - timedelta(days=1)).strftime('%Y-%m-%d'),
        (operation_data.date + timedelta(days=1)).strftime('%Y-%m-%d')
    )
    assert current_id in (v.id for v in result)


# Test deleting an operation.
@pytest.mark.asyncio
async def test_delete():
    """
    Test the service function to delete an operation.
    """
    current_id = await operations_service.get_operation_id()
    result = await operations_service.delete_operation(current_id)
    assert result is True
