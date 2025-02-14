import requests
import pytest

BASE_URL = "https://reqres.in/api"

@pytest.mark.parametrize("page", [1, 2])
def test_get_users_list(page):
    response = requests.get(f"{BASE_URL}/users", params={"page": page})
    assert response.status_code == 200
    assert "data" in response.json()
    assert isinstance(response.json()["data"], list)


def test_get_single_user():
    user_id = 2
    response = requests.get(f"{BASE_URL}/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["data"]["id"] == user_id


def test_get_nonexistent_user():
    response = requests.get(f"{BASE_URL}/users/23")
    assert response.status_code == 404


def test_create_user():
    payload = {"name": "John", "job": "QA Engineer"}
    response = requests.post(f"{BASE_URL}/users", json=payload)
    assert response.status_code == 201
    assert response.json()["name"] == payload["name"]
    assert response.json()["job"] == payload["job"]


def test_create_user_empty_body():
    response = requests.post(f"{BASE_URL}/users", json={})
    assert response.status_code in [400, 201]


def test_update_user():
    user_id = 2
    payload = {"name": "Jane", "job": "Software Engineer"}
    response = requests.put(f"{BASE_URL}/users/{user_id}", json=payload)
    assert response.status_code == 200
    assert response.json()["name"] == payload["name"]
    assert response.json()["job"] == payload["job"]


def test_update_nonexistent_user():
    user_id = 999
    payload = {"name": "Ghost", "job": "Unknown"}
    response = requests.put(f"{BASE_URL}/users/{user_id}", json=payload)
    assert response.status_code in [404, 200]


def test_delete_user():
    user_id = 2
    response = requests.delete(f"{BASE_URL}/users/{user_id}")
    assert response.status_code == 204


def test_delete_nonexistent_user():
    user_id = 999
    response = requests.delete(f"{BASE_URL}/users/{user_id}")
    assert response.status_code in [204, 404]


def test_register_success():
    payload = {"email": "eve.holt@reqres.in", "password": "pistol"}
    response = requests.post(f"{BASE_URL}/register", json=payload)
    assert response.status_code == 200
    assert "id" in response.json()
    assert "token" in response.json()


def test_register_failure():
    payload = {"email": "sydney@fife"}  # Без пароля
    response = requests.post(f"{BASE_URL}/register", json=payload)
    assert response.status_code == 400
    assert "error" in response.json()


def test_register_empty_body():
    response = requests.post(f"{BASE_URL}/register", json={})
    assert response.status_code == 400
    assert "error" in response.json()


def test_login_success():
    payload = {"email": "eve.holt@reqres.in", "password": "cityslicka"}
    response = requests.post(f"{BASE_URL}/login", json=payload)
    assert response.status_code == 200
    assert "token" in response.json()


def test_login_failure():
    payload = {"email": "peter@klaven"}  # Без пароля
    response = requests.post(f"{BASE_URL}/login", json=payload)
    assert response.status_code == 400
    assert "error" in response.json()


def test_login_empty_body():
    response = requests.post(f"{BASE_URL}/login", json={})
    assert response.status_code == 400
    assert "error" in response.json()


def test_delayed_response():
    response = requests.get(f"{BASE_URL}/users", params={"delay": 3})
    assert response.status_code == 200
    assert "data" in response.json()
