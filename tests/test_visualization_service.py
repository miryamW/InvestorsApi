import pytest
from datetime import datetime
from unittest.mock import patch, AsyncMock
from starlette.responses import StreamingResponse
from app.models.operation import Operation
from app.models.operation_type import Operation_type
from app.services.visualization_service import (
    fetch_operations,
    calculate_sums,
    get_expenses_and_revenues_by_month,
    get_expenses_against_revenues_by_month,
    get_expenses_against_revenues_by_month_all_year,
    get_yearly_graph,
    get_balance_divide_to_months,
    get_balances_yearly_graph,
    get_balance_yearly_bar
)

# Mock data
mock_operations = [
    Operation(id=1, sum=100.0, userId=1, type=Operation_type.EXPENSE, date=datetime.now()),
    Operation(id=2, sum=500.0, userId=1, type=Operation_type.REVENUE, date=datetime.now())
    # Add more mock data as needed
]


# Fixture for mock operations
@pytest.fixture
def mock_operations_data():
    return mock_operations


# Patch the operations_service
@pytest.fixture(autouse=True)
def mock_operations_service():
    with patch('app.services.operations_service.get_all_operations', new_callable=AsyncMock) as mock_get_all_operations:
        with patch('app.services.operations_service.get_all_operations_between_dates',
                   new_callable=AsyncMock) as mock_get_all_operations_between_dates:
            yield mock_get_all_operations, mock_get_all_operations_between_dates


@pytest.mark.asyncio
async def test_fetch_operations(mock_operations_service, mock_operations_data):
    mock_get_all_operations, _ = mock_operations_service
    mock_get_all_operations.return_value = mock_operations_data

    user_id = 1
    operations = await fetch_operations(user_id)
    assert operations == mock_operations_data


@pytest.mark.asyncio
async def test_fetch_operations_with_dates(mock_operations_service, mock_operations_data):
    _, mock_get_all_operations_between_dates = mock_operations_service
    mock_get_all_operations_between_dates.return_value = mock_operations_data

    user_id = 1
    start_date = '2023-01-01'
    end_date = '2023-01-31'
    operations = await fetch_operations(user_id, start_date, end_date)
    assert operations == mock_operations_data


def test_calculate_sums(mock_operations_data):
    result = calculate_sums(mock_operations_data, Operation_type.REVENUE)
    assert result == 500

    result = calculate_sums(mock_operations_data, Operation_type.EXPENSE)
    assert result == 100


@pytest.mark.asyncio
async def test_get_expenses_and_revenues_by_month(mock_operations_service, mock_operations_data):
    mock_get_all_operations, _ = mock_operations_service
    mock_get_all_operations.return_value = mock_operations_data

    user_id = 1
    expenses, revenues = await get_expenses_and_revenues_by_month(user_id, '05')
    assert revenues[4] == 500
    assert expenses[4] == 100


@pytest.mark.asyncio
async def test_get_expenses_against_revenues_by_month(mock_operations_service, mock_operations_data):
    mock_get_all_operations, _ = mock_operations_service
    mock_get_all_operations.return_value = mock_operations_data

    user_id = 1
    response = await get_expenses_against_revenues_by_month(user_id, '05')
    assert isinstance(response, StreamingResponse)


@pytest.mark.asyncio
async def test_get_expenses_against_revenues_by_month_all_year(mock_operations_service, mock_operations_data):
    mock_get_all_operations, _ = mock_operations_service
    mock_get_all_operations.return_value = mock_operations_data

    user_id = 1
    response = await get_expenses_against_revenues_by_month_all_year(user_id)
    assert isinstance(response, StreamingResponse)


@pytest.mark.asyncio
async def test_get_yearly_graph(mock_operations_service, mock_operations_data):
    mock_get_all_operations, _ = mock_operations_service
    mock_get_all_operations.return_value = mock_operations_data

    user_id = 1
    response = await get_yearly_graph(user_id)
    assert isinstance(response, StreamingResponse)


@pytest.mark.asyncio
async def test_get_balance_divide_to_months(mock_operations_service, mock_operations_data):
    mock_get_all_operations, _ = mock_operations_service
    mock_get_all_operations.return_value = mock_operations_data

    user_id = 1
    balances = await get_balance_divide_to_months(user_id)
    assert balances[4] == 400  # Revenue - Expense for January


@pytest.mark.asyncio
async def test_get_balances_yearly_graph(mock_operations_service, mock_operations_data):
    mock_get_all_operations, _ = mock_operations_service
    mock_get_all_operations.return_value = mock_operations_data

    user_id = 1
    response = await get_balances_yearly_graph(user_id)
    assert isinstance(response, StreamingResponse)


@pytest.mark.asyncio
async def test_get_balance_yearly_bar(mock_operations_service, mock_operations_data):
    mock_get_all_operations, _ = mock_operations_service
    mock_get_all_operations.return_value = mock_operations_data

    user_id = 1
    response = await get_balance_yearly_bar(user_id)
    assert isinstance(response, StreamingResponse)
