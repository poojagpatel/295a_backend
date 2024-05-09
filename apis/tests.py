import pytest
import json
from your_flask_app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_get_earthquakes_success(client):
    response = client.get("/api/eq")
    assert response.status_code == 200
    data = json.loads(response.data.decode("utf-8"))
    assert isinstance(data, list)


def test_pagination_functionality(client):
    response_page1 = client.get("/api/eq?page=1&page_size=10")
    data_page1 = json.loads(response_page1.data.decode("utf-8"))
    response_page2 = client.get("/api/eq?page=2&page_size=10")
    data_page2 = json.loads(response_page2.data.decode("utf-8"))
    assert len(data_page1) == 10
    assert len(data_page2) == 10
    # Add more assertions for pagination


def test_error_handling_invalid_page_parameters(client):
    response = client.get("/api/eq?page=invalid&page_size=invalid")
    assert response.status_code == 400
    error_data = json.loads(response.data.decode("utf-8"))
    assert "error" in error_data


def test_error_handling_exception_during_retrieval(client, monkeypatch):
    def mock_exception(*args, **kwargs):
        raise Exception("Mocked exception during data retrieval")

    monkeypatch.setattr("your_flask_app.get_earthquakes", mock_exception)
    response = client.get("/api/eq")
    assert response.status_code == 500
    error_data = json.loads(response.data.decode("utf-8"))
    assert "error" in error_data


def test_response_format(client):
    response = client.get("/api/eq")
    data = json.loads(response.data.decode("utf-8"))
    for record in data:
        assert "uniqueID" in record
        assert "Type" in record
        assert "Time" in record
        assert "Title" in record
        assert "Description" in record
        assert "Url" in record
        assert "latitude" in record
        assert "longitude" in record
        assert "intensity" in record
        # Add more assertions for data types and formats


def test_get_earthquake_by_code_success(client):
    # Assuming the code exists in the database
    response = client.get("/api/eq/your_code_here")
    assert response.status_code == 200
    data = json.loads(response.data.decode("utf-8"))
    assert "uniqueID" in data


def test_get_earthquake_by_code_not_found(client):
    # Assuming the code does not exist in the database
    response = client.get("/api/eq/non_existing_code")
    assert response.status_code == 404
    error_data = json.loads(response.data.decode("utf-8"))
    assert "message" in error_data
    assert error_data["message"] == "Earthquake not found"


def test_get_wildfires_success(client):
    response = client.get("/api/wf")
    assert response.status_code == 200
    data = json.loads(response.data.decode("utf-8"))
    assert isinstance(data, list)


def test_pagination_functionality_wildfires(client):
    response_page1 = client.get("/api/wf?page=1&page_size=10")
    data_page1 = json.loads(response_page1.data.decode("utf-8"))
    response_page2 = client.get("/api/wf?page=2&page_size=10")
    data_page2 = json.loads(response_page2.data.decode("utf-8"))
    assert len(data_page1) == 10
    assert len(data_page2) == 10
    # Add more assertions for pagination


def test_error_handling_invalid_page_parameters_wildfires(client):
    response = client.get("/api/wf?page=invalid&page_size=invalid")
    assert response.status_code == 400
    error_data = json.loads(response.data.decode("utf-8"))
    assert "error" in error_data


def test_error_handling_exception_during_retrieval_wildfires(client, monkeypatch):
    def mock_exception(*args, **kwargs):
        raise Exception("Mocked exception during data retrieval")

    monkeypatch.setattr("your_flask_app.get_wildfires", mock_exception)
    response = client.get("/api/wf")
    assert response.status_code == 500
    error_data = json.loads(response.data.decode("utf-8"))
    assert "error" in error_data


def test_response_format_wildfires(client):
    response = client.get("/api/wf")
    data = json.loads(response.data.decode("utf-8"))
    for record in data:
        assert "uniqueID" in record
        assert "Type" in record
        assert "Time" in record
        assert "Title" in record
        assert "Description" in record
        assert "Url" in record
        assert "latitude" in record
        assert "longitude" in record
        assert "intensity" in record
        # Add more assertions for data types and formats


def test_get_wildfire_by_code_success(client):
    # Assuming the code exists in the database
    response = client.get("/api/wf/your_code_here")
    assert response.status_code == 200
    data = json.loads(response.data.decode("utf-8"))
    assert "uniqueID" in data


def test_get_wildfire_by_code_not_found(client):
    # Assuming the code does not exist in the database
    response = client.get("/api/wf/non_existing_code")
    assert response.status_code == 404
    error_data = json.loads(response.data.decode("utf-8"))
    assert "message" in error_data
    assert error_data["message"] == "Wildfire not found"


def test_response_format_wildfire_by_code(client):
    # Assuming the code exists in the database
    response = client.get("/api/wf/your_code_here")
    data = json.loads(response.data.decode("utf-8"))
    assert "uniqueID" in data
    assert "Type" in data
    assert "Time" in data
    assert "Title" in data
    assert "Description" in data
    assert "Url" in data
    assert "latitude" in data
    assert "longitude" in data
    assert "intensity" in data
    # Add more assertions for data types and formats


def test_error_handling_not_found_wildfire_by_code(client):
    # Assuming the code does not exist in the database
    response = client.get("/api/wf/non_existing_code")
    assert response.status_code == 404
    error_data = json.loads(response.data.decode("utf-8"))
    assert "message" in error_data
    assert error_data["message"] == "Wildfire not found"


def test_error_handling_invalid_code_wildfire_by_code(client):
    # Assuming an invalid code format is provided
    response = client.get("/api/wf/invalid_code_format")
    assert response.status_code == 400
    error_data = json.loads(response.data.decode("utf-8"))
    assert "error" in error_data


def test_error_handling_exception_during_retrieval_wildfire_by_code(
    client, monkeypatch
):
    def mock_exception(*args, **kwargs):
        raise Exception("Mocked exception during data retrieval")

    monkeypatch.setattr("your_flask_app.get_wildfire_by_code", mock_exception)
    response = client.get("/api/wf/your_code_here")
    assert response.status_code == 500
    error_data = json.loads(response.data.decode("utf-8"))
    assert "error" in error_data


def test_get_weather_misc_success(client):
    response = client.get("/api/weather")
    assert response.status_code == 200
    data = json.loads(response.data.decode("utf-8"))
    assert isinstance(data, list)


def test_pagination_functionality_weather_misc(client):
    response_page1 = client.get("/api/weather?page=1&page_size=10")
    data_page1 = json.loads(response_page1.data.decode("utf-8"))
    response_page2 = client.get("/api/weather?page=2&page_size=10")
    data_page2 = json.loads(response_page2.data.decode("utf-8"))
    assert len(data_page1) == 10
    assert len(data_page2) == 10
    # Add more assertions for pagination


def test_error_handling_invalid_page_parameters_weather_misc(client):
    response = client.get("/api/weather?page=invalid&page_size=invalid")
    assert response.status_code == 400
    error_data = json.loads(response.data.decode("utf-8"))
    assert "error" in error_data


def test_error_handling_exception_during_retrieval_weather_misc(client, monkeypatch):
    def mock_exception(*args, **kwargs):
        raise Exception("Mocked exception during data retrieval")

    monkeypatch.setattr("your_flask_app.get_weather_misc", mock_exception)
    response = client.get("/api/weather")
    assert response.status_code == 500
    error_data = json.loads(response.data.decode("utf-8"))
    assert "error" in error_data


def test_get_weather_by_code_success(client):
    # Assuming the code exists in the database
    response = client.get("/api/weather/your_code_here")
    assert response.status_code == 200
    data = json.loads(response.data.decode("utf-8"))
    assert "properties" in data


def test_get_weather_by_code_not_found(client):
    # Assuming the code does not exist in the database
    response = client.get("/api/weather/non_existing_code")
    assert response.status_code == 404
    error_data = json.loads(response.data.decode("utf-8"))
    assert "message" in error_data
    assert error_data["message"] == "Weather record not found"


def test_error_handling_invalid_code_weather_by_code(client):
    # Assuming an invalid code format is provided
    response = client.get("/api/weather/invalid_code_format")
    assert response.status_code == 400
    error_data = json.loads(response.data.decode("utf-8"))
    assert "error" in error_data


def test_error_handling_exception_during_retrieval_weather_by_code(client, monkeypatch):
    def mock_exception(*args, **kwargs):
        raise Exception("Mocked exception during data retrieval")

    monkeypatch.setattr("your_flask_app.get_weather_by_code", mock_exception)
    response = client.get("/api/weather/your_code_here")
    assert response.status_code == 500
    error_data = json.loads(response.data.decode("utf-8"))
    assert "error" in error_data


def test_chat_with_event_success(client):
    # Assuming valid event and question data
    data = {
        "event": {"event_data": "your_event_data_here"},
        "question": "give me some events related earthquakes",
    }
    response = client.post("/api/event_chat", json=data)
    assert response.status_code == 200
    data = json.loads(response.data.decode("utf-8"))
    assert "chat_response" in data


def test_chat_with_event_no_event_found(client):
    # Assuming no event found in the database with the provided event ID
    data = {"event": None, "question": "give me some events related earthquakes"}
    response = client.post("/api/event_chat", json=data)
    assert response.status_code == 404
    error_data = json.loads(response.data.decode("utf-8"))
    assert "error" in error_data


def test_chat_with_event_no_data_provided(client):
    # Assuming no data provided in the request
    response = client.post("/api/event_chat")
    assert response.status_code == 400
    error_data = json.loads(response.data.decode("utf-8"))
    assert "error" in error_data


def test_ask_success(client):
    # Assuming valid question data
    data = {"question": "give me some events related earthquakes"}
    response = client.post("/api/ask", json=data)
    assert response.status_code == 200
    data = json.loads(response.data.decode("utf-8"))
    assert "answer" in data


def test_ask_no_question_provided(client):
    # Assuming no question provided in the request
    response = client.post("/api/ask")
    assert response.status_code == 400
    error_data = json.loads(response.data.decode("utf-8"))
    assert "error" in error_data
