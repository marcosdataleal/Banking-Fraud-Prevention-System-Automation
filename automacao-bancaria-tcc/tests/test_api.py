from fastapi.testclient import TestClient

from bankflow.api import app


def test_api_home():
    client = TestClient(app)

    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["projeto"] == "BankFlow Auditor"
