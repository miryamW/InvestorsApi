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

# Mock data for operations
mock_operations = [
    Operation(id=1, sum=100.0, userId=1, type=Operation_type.EXPENSE, date=datetime.now()),
    Operation(id=2, sum=500.0, userId=1, type=Operation_type.REVENUE, date=datetime.now())
    # Add more mock data as needed
]


# Fixture to provide mock operations data
@pytest.fixture
def mock_operations_data():
    """
    Fixture to provide mock operations data for testing.

    Returns:
        list: A list of mock Operation objects.
    """
    return mock_operations


# Fixture to patch the operations_service methods
@pytest.fixture(autouse=True)
def mock_operations_service():
    """
    Fixture to patch the operations_service methods with AsyncMock.

    Yields:
        tuple: A tuple containing the patched get_all_operations and get_all_operations_between_dates methods.
    """
    with patch('app.services.operations_service.get_all_operations', new_callable=AsyncMock) as mock_get_all_operations:
        with patch('app.services.operations_service.get_all_operations_between_dates',
                   new_callable=AsyncMock) as mock_get_all_operations_between_dates:
            yield mock_get_all_operations, mock_get_all_operations_between_dates


# Test the fetch_operations function
@pytest.mark.asyncio
async def test_fetch_operations(mock_operations_service, mock_operations_data):
    """
    Test fetching all operations for a given user.

    Args:
        mock_operations_service (tuple): The patched operations_service methods.
        mock_operations_data (list): The mock operations data.
    """
    mock_get_all_operations, _ = mock_operations_service
    mock_get_all_operations.return_value = mock_operations_data

    user_id = 1
    operations = await fetch_operations(user_id)
    assert operations == mock_operations_data


# Test the fetch_operations function with date range
@pytest.mark.asyncio
async def test_fetch_operations_with_dates(mock_operations_service, mock_operations_data):
    """
    Test fetching operations for a given user within a date range.

    Args:
        mock_operations_service (tuple): The patched operations_service methods.
        mock_operations_data (list): The mock operations data.
    """
    _, mock_get_all_operations_between_dates = mock_operations_service
    mock_get_all_operations_between_dates.return_value = mock_operations_data

    user_id = 1
    start_date = '2023-01-01'
    end_date = '2023-01-31'
    operations = await fetch_operations(user_id, start_date, end_date)
    assert operations == mock_operations_data


# Test the calculate_sums function
def test_calculate_sums(mock_operations_data):
    """
    Test calculating the sum of operations for a given type.

    Args:
        mock_operations_data (list): The mock operations data.
    """
    result = calculate_sums(mock_operations_data, Operation_type.REVENUE)
    assert result == 500

    result = calculate_sums(mock_operations_data, Operation_type.EXPENSE)
    assert result == 100


# Test the get_expenses_and_revenues_by_month function
@pytest.mark.asyncio
async def test_get_expenses_and_revenues_by_month(mock_operations_service, mock_operations_data):
    """
    Test fetching expenses and revenues by month for a given user.

    Args:
        mock_operations_service (tuple): The patched operations_service methods.
        mock_operations_data (list): The mock operations data.
    """
    mock_get_all_operations, _ = mock_operations_service
    mock_get_all_operations.return_value = mock_operations_data

    user_id = 1
    expenses, revenues = await get_expenses_and_revenues_by_month(user_id, '05')
    assert revenues[4] == 500
    assert expenses[4] == 100


# Test the get_expenses_against_revenues_by_month function
@pytest.mark.asyncio
async def test_get_expenses_against_revenues_by_month(mock_operations_service, mock_operations_data):
    """
    Test fetching expenses against revenues by month for a given user.

    Args:
        mock_operations_service (tuple): The patched operations_service methods.
        mock_operations_data (list): The mock operations data.
    """
    mock_get_all_operations, _ = mock_operations_service
    mock_get_all_operations.return_value = mock_operations_data

    user_id = 1
    response = await get_expenses_against_revenues_by_month(user_id, '05')
    assert isinstance(response, StreamingResponse)


# Test the get_expenses_against_revenues_by_month_all_year function
@pytest.mark.asyncio
async def test_get_expenses_against_revenues_by_month_all_year(mock_operations_service, mock_operations_data):
    """
    Test fetching expenses against revenues for the entire year for a given user.

    Args:
        mock_operations_service (tuple): The patched operations_service methods.
        mock_operations_data (list): The mock operations data.
    """
    mock_get_all_operations, _ = mock_operations_service
    mock_get_all_operations.return_value = mock_operations_data

    user_id = 1
    response = await get_expenses_against_revenues_by_month_all_year(user_id)
    assert isinstance(response, StreamingResponse)


# Test the get_yearly_graph function
@pytest.mark.asyncio
async def test_get_yearly_graph(mock_operations_service, mock_operations_data):
    """
    Test fetching the yearly graph for a given user.

    Args:
        mock_operations_service (tuple): The patched operations_service methods.
        mock_operations_data (list): The mock operations data.
    """
    mock_get_all_operations, _ = mock_operations_service
    mock_get_all_operations.return_value = mock_operations_data

    user_id = 1
    response = await get_yearly_graph(user_id)
    assert isinstance(response, StreamingResponse)


# Test the get_balance_divide_to_months function
@pytest.mark.asyncio
async def test_get_balance_divide_to_months(mock_operations_service, mock_operations_data):
    """
    Test calculating the monthly balances for a given user.

    Args:
        mock_operations_service (tuple): The patched operations_service methods.
        mock_operations_data (list): The mock operations data.
    """
    mock_get_all_operations, _ = mock_operations_service
    mock_get_all_operations.return_value = mock_operations_data

    user_id = 1
    balances = await get_balance_divide_to_months(user_id)
    assert balances[4] == 400  # Revenue - Expense for January


# Test the get_balances_yearly_graph function
@pytest.mark.asyncio
async def test_get_balances_yearly_graph(mock_operations_service, mock_operations_data):
    """
    Test fetching the yearly balances graph for a given user.

    Args:
        mock_operations_service (tuple): The patched operations_service methods.
        mock_operations_data (list): The mock operations data.
    """
    mock_get_all_operations, _ = mock_operations_service
    mock_get_all_operations.return_value = mock_operations_data

    user_id = 1
    response = await get_balances_yearly_graph(user_id)
    assert isinstance(response, StreamingResponse)


# Test the get_balance_yearly_bar function
@pytest.mark.asyncio
async def test_get_balance_yearly_bar(mock_operations_service, mock_operations_data):
    """
    Test fetching the yearly balance bar chart for a given user.

    Args:
        mock_operations_service (tuple): The patched operations_service methods.
        mock_operations_data (list): The mock operations data.
    """
    mock_get_all_operations, _ = mock_operations_service
    mock_get_all_operations.return_value = mock_operations_data

    user_id = 1
    response = await get_balance_yearly_bar(user_id)
    assert isinstance(response, StreamingResponse)
