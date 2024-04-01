from fastapi.testclient import TestClient
import ens_fake_weather_data.constants as cst

def get_test_client(monkeypatch, sampling_frequency, percentage_missing_data):

    # First patch the environment variables
    monkeypatch.setenv(cst.SAMPLING_FREQUENCY, sampling_frequency)
    monkeypatch.setenv(cst.PERCENTAGE_MISSING_DATA, percentage_missing_data)

    # Then, import the FastAPI app
    from ens_fake_weather_data.main import app
    client = TestClient(app=app)
    return client

def test_endpoint_weather(monkeypatch):
    """Test that endpoint weather behaves as expected."""
    test_client = get_test_client(monkeypatch=monkeypatch, sampling_frequency="1h", percentage_missing_data="0")

    # Query with missing inputs
    response = test_client.get("/weather")
    assert response.status_code == 422  # Unprocessable entity

    # Query with correct inputs
    query_params = {
        "start_date": "2024-01-01",
        "end_date": "2025-01-01",
        "latitude": 40.5,
        "longitude": 130,
    }
    response = test_client.get("/weather", params=query_params)
    assert response.status_code == 200

    # Check that the response has the correct amount of data.
    # Since 2024 is a leap year, we expect : 366*24 + 1 records exactly (the aditional one is 2025-01-01 midnight).
    assert len(response.json()) == 366*24 + 1
    assert "2025-01-01 00:00:00" in response.json()

    
