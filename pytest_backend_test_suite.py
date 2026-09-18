import sys
import os
from fastapi.testclient import TestClient

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app

client = TestClient(app)

def test_read_root():
    """Verify that the root endpoint returns operational status."""
    response = client.get("/")
    assert response.status_code == 200
    assert "running" in response.json()["message"]

def test_get_subscriptions():
    """Verify fetching subscription items from SQLite DB."""
    response = client.get("/api/subscriptions")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_subscription():
    """Verify creating a new subscription record."""
    payload = {
        "id": "pytest-sub-101",
        "name": "Automated Test Plan",
        "category": "Software/SaaS",
        "cycle": "Monthly",
        "cost": 12.99,
        "nextDate": "2026-10-15",
        "paymentMethod": "Test Card",
        "status": "Active",
        "isTrial": True,
        "notes": "PyTest created entry"
    }
    response = client.post("/api/subscriptions", json=payload)
    assert response.status_code == 200
    assert response.json()["name"] == "Automated Test Plan"

def test_delete_subscription():
    """Verify deleting the test subscription record."""
    response = client.delete("/api/subscriptions/pytest-sub-101")
    assert response.status_code == 200
    assert "deleted" in response.json()["message"]