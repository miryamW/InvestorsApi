from typing import Optional

from fastapi import APIRouter, Request, Query, HTTPException
from utils.log import log
from app.services import visualization_service

visualization_router = APIRouter()


@visualization_router.get("/expenses_vs_revenues/{user_id}/{visual_type}/")
@log
async def year_divide_to_months_budget(request: Request, user_id: int, visual_type: str,
                                       month: Optional[str] = Query(None,
                                                                    description="Optional search query parameter")):
    """
    Retrieves a visualization comparing expenses and revenues for each month of the year.

    Parameters:
    - user_id (int): The ID of the user.
    - visual_type (str): The type of visualization - graph/bar chart.
    - month (str):  optional: specific month or all year (if not have month).

    Returns:
    - StreamingResponse: Response containing visualization image.
    """
    if visual_type == "bar" and month is None:
        return await visualization_service.get_expenses_against_revenues_by_month_all_year(user_id)
    if visual_type == "graph" and month is None:
        return await visualization_service.get_yearly_graph(user_id)
    if month is not None:
        return await visualization_service.get_expenses_against_revenues_by_month(user_id, month)
    else:
        raise HTTPException(status_code=404, detail="not valid url")


@visualization_router.get("/balance/{user_id}/{visual_type}}")
@log
async def yearly_balance_graph(request: Request, user_id: int, visual_type: str):
    """
    Retrieves a line plot showing the monthly balance for the year.

    Parameters:
    - user_id (int): The ID of the user.
    -type (str): The type of visualization - graph/bar chart.

    Returns:
    - StreamingResponse: Response containing the line plot image.
    """
    if visual_type == "bar":
        return await visualization_service.get_balance_yearly_bar(user_id)
    if visual_type == "graph":
        return await visualization_service.get_balances_yearly_graph(user_id)
    else:
        raise HTTPException(status_code=404, detail="not valid url")
