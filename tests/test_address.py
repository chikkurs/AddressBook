"""
tests/test_address.py

Run tests using:

pytest -v

or

pytest tests/test_address.py -v
"""

from fastapi.testclient import TestClient
from main import app

# Create test client
client = TestClient(app)


# --------------------------------------------------
# Root Endpoint Tests
# --------------------------------------------------

def test_root_endpoint():
    """
    Verify application is running.
    """

    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Address Book API is running"
    }


# --------------------------------------------------
# Create Address Tests
# --------------------------------------------------

def test_create_address():
    """
    Verify a new address can be created successfully.
    """

    payload = {
        "name": "Vimalrss",
        "email": "vimal12@test.com",
        "phone": "9999999749",
        "latitude": 8.8932,
        "longitude": 76.6141,
        "street": "MG Road",
        "city": "Kollam",
        "country": "India",
    }

    response = client.post(
        "/addresses/",
        json=payload
    )

    assert response.status_code == 201

    data = response.json()

    assert data["name"] == payload["name"]
    assert data["email"] == payload["email"]
    assert data["phone"] == payload["phone"]


def test_create_address_missing_required_field():
    """
    Verify validation error occurs
    when mandatory fields are missing.
    """

    payload = {
        "email": "test@test.com",
        "phone": "8888888888",
        "latitude": 8.89,
        "longitude": 76.61
    }

    response = client.post(
        "/addresses/",
        json=payload
    )

    assert response.status_code == 422


# --------------------------------------------------
# Duplicate Validation Tests
# --------------------------------------------------

def test_duplicate_email():
    """
    Verify duplicate email is rejected.
    """

    payload = {
        "name": "User1",
        
        "street": "MG Road",
        "city": "Kollam",
        "country": "India",
        "email": "duplicate@test.com",
        "phone": "1111111111",
        "latitude": 8.89,
        "longitude": 76.61
    }

    client.post("/addresses/", json=payload)

    payload["phone"] = "2222222222"

    response = client.post(
        "/addresses/",
        json=payload
    )

    assert response.status_code == 400


def test_duplicate_phone():
    """
    Verify duplicate phone number is rejected.
    """

    payload = {
        "name": "User2",
        "street": "MG Road",
        "city": "Kollam",
        "country": "India",
        "email": "user2@test.com",
        "phone": "3333333333",
        "latitude": 8.89,
        "longitude": 76.61
    }

    client.post("/addresses/", json=payload)

    payload["email"] = "new@test.com"

    response = client.post(
        "/addresses/",
        json=payload
    )

    assert response.status_code == 400


# --------------------------------------------------
# Get Address Tests
# --------------------------------------------------

def test_get_all_addresses():
    """
    Verify all addresses can be fetched.
    """

    response = client.get("/addresses/")

    assert response.status_code == 200


def test_get_invalid_address():
    """
    Verify 404 is returned
    for non-existing address.
    """

    response = client.get(
        "/addresses/99999"
    )

    assert response.status_code == 404

    assert response.json()["detail"] == (
        "Address not found"
    )


# --------------------------------------------------
# Update Address Tests
# --------------------------------------------------

def test_update_invalid_address():
    """
    Verify update fails
    when address does not exist.
    """

    response = client.patch(
        "/addresses/99999",
        json={"name": "Updated Name"}
    )

    assert response.status_code == 404


# --------------------------------------------------
# Delete Address Tests
# --------------------------------------------------

def test_delete_invalid_address():
    """
    Verify delete fails
    when address does not exist.
    """

    response = client.delete(
        "/addresses/99999"
    )

    assert response.status_code == 404

    assert response.json()["detail"] == (
        "Address not found"
    )


# --------------------------------------------------
# Nearby Search Tests
# --------------------------------------------------

def test_nearby_search_invalid_params():
    """
    Verify FastAPI validation works
    for invalid query parameters.
    """

    response = client.get(
        "/addresses/nearby/search",
        params={
            "latitude": "abc",
            "longitude": 76.61,
            "distance_km": 5
        }
    )

    assert response.status_code == 422


def test_nearby_search_no_results():
    """
    Verify empty list is returned
    when no address is nearby.
    """

    response = client.get(
        "/addresses/nearby/search",
        params={
            "latitude": 0,
            "longitude": 0,
            "distance_km": 1
        }
    )

    assert response.status_code == 200

    assert isinstance(
        response.json(),
        list
    )