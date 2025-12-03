import pytest
from fastapi.testclient import TestClient

from app import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"hint": "Try it under /docs."}

def test_profile_intro():
    response = client.get("/profile")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "skills" in data
    assert isinstance(data["skills"], list)

def test_profile_edit_forbidden():
    response = client.post("/profile/edit", json={
        "name": "New Name"
    })
    assert response.status_code == 403  # Forbidden