from fastapi import APIRouter, Request
from starlette.responses import StreamingResponse

from app.middlewares.log import log
from app.services import visualization_service

visualization_router = APIRouter()


@visualization_router.get("/monthlyBudget/{user_id}/{month}")
@log
async def month_budget(request: Request, user_id: int, month: str):
    buf = await visualization_service.get_expenses_against_revenues_by_month(user_id, month)
    return StreamingResponse(buf, media_type="img/png")


@visualization_router.get("/yearDivideByMonthsBudget/{user_id}")
@log
async def year_divide_to_months_budget(request: Request, user_id: int):
    buf = await visualization_service.get_expenses_against_revenues_by_month_all_years(user_id)
    return StreamingResponse(buf, media_type="img/png")


@visualization_router.get("/yearlyGraph/{user_id}")
@log
async def yearly_graph(request: Request, user_id: int):
    buf = await visualization_service.get_yearly_graph(user_id)
    return StreamingResponse(buf, media_type="img/png")
