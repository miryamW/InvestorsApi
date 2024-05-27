import pytest
from fastapi.testclient import TestClient
from app.routes.operation_router import operation_router
from app.services import operations_service
import pytest_asyncio
import httpx

# Create a TestClient instance for the operation_router.
client = TestClient(operation_router)


# Define an async fixture that provides an operation ID.
@pytest_asyncio.fixture
async def operation_id():
    """
    Async fixture to get an operation ID from the operations_service.

    Yields:
        int: The ID of the operation.
    """
    id = await operations_service.get_operation_id()
    yield id


# Test the operation addition functionality.
def test_add_operation():
    """
    Test the operation addition endpoint.
    """
    response = client.post("/", json={
        "id": 1,
        "sum": 230.5,
        "userId": 1,
        "type": 'revenue',
        "date": "2024-01-22T15:49:07.376+00:00"
    })
    assert response.status_code == 200


# Test the functionality to get all operations for a user.
def test_get_operations():
    """
    Test the endpoint to get all operations for a user.
    """
    response = client.get("/allOperations/1")
    assert response.status_code == 200


# Test the functionality to get a specific operation.
@pytest.mark.asyncio
async def test_get_operation(operation_id):
    """
    Test the endpoint to get a specific operation by ID.

    Args:
        operation_id (int): The ID of the operation provided by the operation_id fixture.
    """
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8080/operations") as async_client:
        response = await async_client.get(f"/{operation_id - 1}")
    assert response.status_code == 200


# Test the functionality to update a specific operation.
@pytest.mark.asyncio
async def test_update_operation(operation_id):
    """
    Test the endpoint to update a specific operation by ID.

    Args:
        operation_id (int): The ID of the operation provided by the operation_id fixture.
    """
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8080/operations") as async_client:
        response = await async_client.put(f"/{operation_id - 1}", json={
            "id": 1,
            "sum": 230.5,
            "userId": 1,
            "type": 'revenue',
            "date": "2024-01-22T15:49:07.376+00:00"
        })
    assert response.status_code == 200


# Test the functionality to get operations within a specific term.
def test_get_term():
    """
    Test the endpoint to get operations within a specific term.
    """
    response = client.get("/1/2024-05-01/2024-05-30")
    assert response.status_code == 200


# Test the functionality to delete a specific operation.
@pytest.mark.asyncio
async def test_delete_operation(operation_id):
    """
    Test the endpoint to delete a specific operation by ID.

    Args:
        operation_id (int): The ID of the operation provided by the operation_id fixture.
    """
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8080/operations") as async_client:
        response = await async_client.delete(f"/{operation_id - 1}")
    assert response.status_code == 200
