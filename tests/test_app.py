from fastapi.testclient import TestClient
from src.app import app, activities
import copy
import pytest


client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Restore the in-memory activities after each test."""
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(copy.deepcopy(original))


def test_get_activities():
    r = client.get("/activities")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, dict)
    assert "Basketball" in data


def test_signup_and_delete_flow():
    email = "pytest-user@example.com"

    # Sign up
    r = client.post(f"/activities/Basketball/signup?email={email}")
    assert r.status_code == 200
    assert email in activities["Basketball"]["participants"]

    # Duplicate signup should return 400
    r2 = client.post(f"/activities/Basketball/signup?email={email}")
    assert r2.status_code == 400

    # Delete participant
    r3 = client.delete(f"/activities/Basketball/participants?email={email}")
    assert r3.status_code == 200
    assert email not in activities["Basketball"]["participants"]


def test_delete_nonexistent_participant():
    email = "no-one@example.com"
    r = client.delete(f"/activities/Basketball/participants?email={email}")
    assert r.status_code == 404
