from fastapi.testclient import TestClient
from app.main import app

# Create a TestClient instance
client = TestClient(app)

def test_ping():
    # Send a GET request to the /api/v1/ping endpoint with authentication
    response = client.get("/api/v1/ping")
    # Assert that the status code is 200 (OK)
    assert response.status_code == 200
    
    # Assert that the response JSON matches the expected output
    assert response.json() == {"result": "pong"}