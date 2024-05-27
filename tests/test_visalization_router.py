import pytest
from fastapi.testclient import TestClient
from app.routes.visualization_router import visualization_router

# Create a test client for the visualization router.
client = TestClient(visualization_router)


# Test the endpoint for retrieving the monthly budget.
def test_get_monthlyBudget():
    """
    Test the endpoint for retrieving the monthly budget for a given user and month.
    """
    response = client.get(f"/monthlyBudget/{1}/{1}")
    assert response.status_code == 200


# Test the endpoint for retrieving yearly expenses vs revenues bar chart.
def test_get_yearlyExpensesVsRevenuesBar():
    """
    Test the endpoint for retrieving yearly expenses vs revenues bar chart for a given user.
    """
    response = client.get(f"/yearlyExpensesVsRevenuesBar/{1}")
    assert response.status_code == 200


# Test the endpoint for retrieving yearly expenses vs revenues graph.
def test_get_yearlyExpensesVsRevenuesGraph():
    """
    Test the endpoint for retrieving yearly expenses vs revenues graph for a given user.
    """
    response = client.get(f"/yearlyExpensesVsRevenuesGraph/{1}")
    assert response.status_code == 200


# Test the endpoint for retrieving yearly balance graph.
def test_get_yearlyBalanceGraph():
    """
    Test the endpoint for retrieving yearly balance graph for a given user.
    """
    response = client.get(f"/yearlyBalanceGraph/{1}")
    assert response.status_code == 200


# Test the endpoint for retrieving yearly balance bar chart.
def test_get_yearlyBalanceBar():
    """
    Test the endpoint for retrieving yearly balance bar chart for a given user.
    """
    response = client.get(f"/yearlyBalanceBar/{1}")
    assert response.status_code == 200
