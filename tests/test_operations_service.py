from datetime import datetime
from app.models.operation import Operation
from app.services import operations_service
import asyncio
import pytest

pytest_plugins = ('pytest_asyncio',)


@pytest.mark.asyncio
async def test_add_operation():
    assert await operations_service.add_operation(Operation(**{"id": 0, "sum": 123.45, "userId": 1,
                                                               "type": "expense", "date": datetime.now()})) == True
