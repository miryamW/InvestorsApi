from fastapi import APIRouter, Request
from utils.log import log
from app.services import visualization_service

visualization_router = APIRouter()


@visualization_router.get("/monthlyBudget/{user_id}/{month}")
@log
async def month_budget(request: Request, user_id: int, month: str):
    """
    Retrieves a bar chart comparing expenses and revenues for a specific month.

    Parameters:
    - user_id (int): The ID of the user.
    - month (str): The specific month in 'MM' format.

    Returns:
    - StreamingResponse: Response containing the bar chart image.
    """
    return await visualization_service.get_expenses_against_revenues_by_month(user_id, month)


@visualization_router.get("/yearlyExpensesVsRevenuesBar/{user_id}")
@log
async def year_divide_to_months_budget(request: Request, user_id: int):
    """
    Retrieves a bar chart comparing expenses and revenues for each month of the year.

    Parameters:
    - user_id (int): The ID of the user.

    Returns:
    - StreamingResponse: Response containing the bar chart image.
    """
    return await visualization_service.get_expenses_against_revenues_by_month_all_year(user_id)


@visualization_router.get("/yearlyExpensesVsRevenuesGraph/{user_id}")
@log
async def yearly_graph(request: Request, user_id: int):
    """
    Retrieves a line plot comparing monthly expenses and revenues for the year.

    Parameters:
    - user_id (int): The ID of the user.

    Returns:
    - StreamingResponse: Response containing the line plot image.
    """
    return await visualization_service.get_yearly_graph(user_id)


@visualization_router.get("/yearlyBalanceGraph/{user_id}")
@log
async def yearly_balance_graph(request: Request, user_id: int):
    """
    Retrieves a line plot showing the monthly balance for the year.

    Parameters:
    - user_id (int): The ID of the user.

    Returns:
    - StreamingResponse: Response containing the line plot image.
    """
    return await visualization_service.get_balances_yearly_graph(user_id)


@visualization_router.get("/yearlyBalanceBar/{user_id}")
@log
async def yearly_balance_bar(request: Request, user_id: int):
    """
    Retrieves a bar chart showing the monthly balance for the year.

    Parameters:
    - user_id (int): The ID of the user.

    Returns:
    - StreamingResponse: Response containing the bar chart image.
    """
    return await visualization_service.get_balance_yearly_bar(user_id)
