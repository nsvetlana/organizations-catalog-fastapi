import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_activities_empty():
    """
    Ensure GET /activities returns an empty list when no activities exist.
    """
    response = client.get("/activities/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_and_get_nested_activities():
    """
    Test creating nested activities up to the allowed depth (3 levels)
    and ensure that creating an activity beyond this depth fails.
    """
    # Create a root activity.
    root_data = {"name": "Root Activity"}
    root_response = client.post("/activities/", json=root_data)
    assert root_response.status_code == 201
    root = root_response.json()
    root_id = root["id"]

    # Create a child (Level 2)
    child_data = {"name": "Child Activity", "parent_id": root_id}
    child_response = client.post("/activities/", json=child_data)
    assert child_response.status_code == 201
    child = child_response.json()
    child_id = child["id"]

    # Create a grandchild (Level 3)
    grandchild_data = {"name": "Grandchild Activity", "parent_id": child_id}
    grandchild_response = client.post("/activities/", json=grandchild_data)
    assert grandchild_response.status_code == 201
    grandchild = grandchild_response.json()

    # Attempt creating a great-grandchild (Level 4) should fail.
    great_grandchild_data = {"name": "Great-Grandchild Activity", "parent_id": grandchild["id"]}
    great_grandchild_response = client.post("/activities/", json=great_grandchild_data)
    assert great_grandchild_response.status_code == 400
    assert "Maximum nesting level of 3 exceeded" in great_grandchild_response.json()["detail"]
