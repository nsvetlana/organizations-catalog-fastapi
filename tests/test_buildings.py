import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_buildings_empty():
    """
    Test that a GET request to the buildings endpoint returns an empty list when no buildings exist.
    """
    response = client.get("/buildings/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_and_get_building():
    """
    Test creating a building and retrieving it.
    """
    building_data = {
        "address": "123 Main St, Test City",
        "latitude": 40.7128,
        "longitude": -74.0060
    }
    # Create a new building.
    post_response = client.post("/buildings/", json=building_data)
    assert post_response.status_code == 201
    created_building = post_response.json()
    assert created_building["address"] == building_data["address"]

    building_id = created_building["id"]
    get_response = client.get(f"/buildings/{building_id}")
    assert get_response.status_code == 200
    fetched_building = get_response.json()
    assert fetched_building["id"] == building_id

def test_get_buildings_by_bounds():
    """
    Create a building and retrieve it using geographical boundary filtering.
    """
    building_data = {
        "address": "456 Sample Rd, Bounds City",
        "latitude": 45.0,
        "longitude": -75.0
    }
    # Insert the building record.
    client.post("/buildings/", json=building_data)

    # Query boundaries that include the building.
    params = {
        "lat_min": 44.0,
        "lat_max": 46.0,
        "lon_min": -76.0,
        "lon_max": -74.0
    }
    response = client.get("/buildings/bounds", params=params)
    assert response.status_code == 200
    buildings = response.json()
    assert any(b["address"] == building_data["address"] for b in buildings)
