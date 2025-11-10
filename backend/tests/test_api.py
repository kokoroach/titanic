from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_api_root():
    # Invoke health endpoint
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert "status" in response.json()
