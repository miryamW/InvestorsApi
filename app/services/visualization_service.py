
import io
from datetime import datetime
from starlette.responses import StreamingResponse
from app.models.operation_type import Operation_type
from app.services import operations_service
import matplotlib.pyplot as plt

months_names = ['January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December']
months_length = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


async def fetch_operations(user_id: int, start_date: str = None, end_date: str = None):
    if start_date and end_date:
        return await operations_service.get_all_operations_between_dates(user_id, start_date, end_date)
    return await operations_service.get_all_operations(user_id)


def calculate_sums(operations, operation_type):
    return sum(op.sum for op in operations if op.type == operation_type)


async def get_expenses_and_revenues_by_month(user_id: int, month: str = None):
    if month:
        year = datetime.now().year
        start_date = f"{year}-{month}-1"
        end_date = f"{year}-{month}-{months_length[int(month) - 1]}"
        data = await fetch_operations(user_id, start_date, end_date)
    else:
        data = await fetch_operations(user_id)

    expenses = [0] * 12
    revenues = [0] * 12

    for operation_ in data:
        month_index = operation_.date.month - 1
        if operation_.type == Operation_type.REVENUE:
            revenues[month_index] += operation_.sum
        if operation_.type == Operation_type.EXPENSE:
            expenses[month_index] += operation_.sum

    return expenses, revenues


def create_plot(x, y_data, labels, title, ylabel):
    fig, ax = plt.subplots()
    for y, label in zip(y_data, labels):
        ax.plot(x, y, label=label, marker='o')
    plt.xticks(rotation=45)
    ax.set_xlabel('Month')
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    return buf


def create_bar_chart(x, y_data, labels, title, ylabel):
    fig, ax = plt.subplots()
    bar_width = 0.35
    index = range(len(x))
    for i, (y, label) in enumerate(zip(y_data, labels)):
        ax.bar([p + i * bar_width for p in index], y, bar_width, label=label)
    plt.xticks(rotation=45)
    ax.set_xlabel('Month')
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks([p + bar_width for p in index])
    ax.set_xticklabels(x)
    ax.legend()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close(fig)
    return buf


async def get_expenses_against_revenues_by_month(user_id: int, month: str):
    expenses, revenues = await get_expenses_and_revenues_by_month(user_id, month)
    month_name = [months_names[int(month) - 1]]
    buf = create_bar_chart(month_name, [expenses, revenues], ['Expenses', 'Revenues'],
                           'Monthly Expenses vs Revenues', 'Value')
    return StreamingResponse(io.BytesIO(buf.read()), media_type="image/png")


async def get_expenses_against_revenues_by_month_all_year(user_id: int):
    expenses, revenues = await get_expenses_and_revenues_by_month(user_id)
    buf = create_bar_chart(months_names, [expenses, revenues], ['Expenses', 'Revenues'],
                           'Monthly Expenses vs Revenues', 'Value')
    return StreamingResponse(io.BytesIO(buf.read()), media_type="image/png")


async def get_yearly_graph(user_id: int):
    expenses, revenues = await get_expenses_and_revenues_by_month(user_id)
    buf = create_plot(months_names, [expenses, revenues], ['Expenses', 'Revenues'],
                      'Monthly Expenses vs Revenues', 'Value')
    return StreamingResponse(io.BytesIO(buf.read()), media_type="image/png")


async def get_balance_divide_to_months(user_id: int):
    expenses, revenues = await get_expenses_and_revenues_by_month(user_id)
    balances = [revenue - expense for expense, revenue in zip(expenses, revenues)]
    return balances


async def get_balances_yearly_graph(user_id: int):
    balances = await get_balance_divide_to_months(user_id)
    buf = create_plot(months_names, [balances], ['Balance'],
                      'Monthly Balance', 'Value')
    return StreamingResponse(io.BytesIO(buf.read()), media_type="image/png")


async def get_balance_yearly_bar(user_id: int):
    balances = await get_balance_divide_to_months(user_id)
    buf = create_bar_chart(months_names, [balances], ['Monthly Balance'],
                           'Monthly Balance', 'Value')
    return StreamingResponse(io.BytesIO(buf.read()), media_type="image/png")
