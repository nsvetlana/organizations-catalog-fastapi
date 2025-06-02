import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db.session import SessionLocal

client = TestClient(app)

@pytest.fixture(scope="function")
def db_session():
    """
    Returns a new database session for each test.
    Ideally, use a test database to avoid contaminating production data.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()

def test_read_organizations_empty():
    """
    Test that a GET request to the organizations endpoint returns an empty list when no organizations are present.
    """
    response = client.get("/organizations/")
    assert response.status_code == 200
    assert response.json() == []

def test_create_and_read_organization():
    """
    Test organization creation and subsequent retrieval.
    """
    org_data = {
        "name": "ООО Рога и Копыта",
        "building_id": 1,
        "phone_numbers": [{"number": "2-222-222"}]
    }
    # Create an organization.
    post_response = client.post("/organizations/", json=org_data)
    assert post_response.status_code == 201
    created_org = post_response.json()
    assert created_org["name"] == org_data["name"]
    assert created_org["building_id"] == org_data["building_id"]
    assert len(created_org["phone_numbers"]) == 1

    # Retrieve the created organization by ID.
    org_id = created_org["id"]
    get_response = client.get(f"/organizations/{org_id}")
    assert get_response.status_code == 200
    fetched_org = get_response.json()
    assert fetched_org["name"] == org_data["name"]
