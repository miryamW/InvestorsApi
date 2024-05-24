import io
from datetime import datetime

from starlette.responses import StreamingResponse

from app.models.operation import Operation
from app.models.operation_type import Operation_type
from app.services import operations_service

import matplotlib.pyplot as plt

months_names = [
    'January', 'February', 'March', 'April', 'May', 'June',
    'July', 'August', 'September', 'October', 'November', 'December'
]
months_length = [31,28,31,30,31,30,31,31,30,31,30,31]


async def get_expenses_against_revenues_by_month(user_id: int, month: str):
    data = await operations_service.get_all_operations_between_dates(user_id, f"{datetime.now().year}-{month}-1",
                                                                     f"{datetime.now().year}-{month}-{months_length[int(month)-1]}")
    revenues = []
    expenses = []
    for operation_ in data:
        if operation_.type == Operation_type.REVENUE:
            revenues.append(operation_.sum)
        if operation_.type == Operation_type.EXPENSE:
            expenses.append(operation_.sum)
    expenses = sum(expenses)
    revenues = sum(revenues)
    months = [months_names[int(month)]]
    return get_bar_expenses_vs_revenues_by_months([expenses], [revenues], months)


async def get_expenses_against_revenues_by_month_all_years(user_id: int):
    (expenses, revenues) = await get_expenses_and_revenues_divide_to_months(user_id)
    return get_bar_expenses_vs_revenues_by_months(expenses, revenues, months_names)


async def get_yearly_graph(user_id: int):
    (expenses, revenues) = await get_expenses_and_revenues_divide_to_months(user_id)
    fig, ax = plt.subplots()
    ax.plot(months_names, expenses, label='Expenses', marker='o')
    ax.plot(months_names, revenues, label='Revenues', marker='o')

    ax.set_xlabel('Month')
    ax.set_ylabel('Value')
    ax.set_title('Monthly Expenses vs Revenues')
    ax.legend()

    # Rotate the x-axis labels for better readability
    plt.xticks(rotation=45)

    # Save the plot to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    return StreamingResponse(io.BytesIO(buf.read()), media_type="image/png")

def get_bar_expenses_vs_revenues_by_months(expenses: list, revenues: list, months: list):
    fig, ax = plt.subplots()
    bar_width = 0.35
    index = range(len(months))

    bar1 = ax.bar(index, expenses, bar_width, label='Expenses')
    bar2 = ax.bar([i + bar_width for i in index], revenues, bar_width, label='Revenues')
    plt.xticks(rotation=45)

    ax.set_xlabel('Month')
    ax.set_ylabel('Value')
    ax.set_title('Monthly Expenses vs Revenues')
    ax.set_xticks([i + bar_width / 2 for i in index])
    ax.set_xticklabels(months)
    ax.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)

    return StreamingResponse(io.BytesIO(buf.read()), media_type="image/png")


async def get_expenses_and_revenues_divide_to_months(user_id: int):
    data = await operations_service.get_all_operations(user_id)
    revenues = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    expenses = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    for operation_ in data:
        if Operation(**operation_).type == Operation_type.REVENUE:
            revenues[Operation(**operation_).date.month-1] = Operation(**operation_).sum + revenues[Operation(**operation_).date.month]
        if Operation(**operation_).type == Operation_type.EXPENSE:
            expenses[Operation(**operation_).date.month-1] = Operation(**operation_).sum + expenses[Operation(**operation_).date.month]
    return expenses, revenues
