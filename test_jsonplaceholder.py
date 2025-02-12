import requests
import pytest

BASE_URL = "https://jsonplaceholder.typicode.com/posts"

@pytest.fixture
def new_post():
    payload = {"title": "foo", "body": "bar", "userId": 1}
    response = requests.post(BASE_URL, json=payload)
    assert response.status_code == 201  # Проверяем, что пост успешно создан
    return response.json()

def test_get_posts():
    response = requests.get(BASE_URL)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_single_post():
    response = requests.get(f"{BASE_URL}/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "title" in data

def test_create_post(new_post):
    assert new_post["title"] == "foo"
    assert new_post["body"] == "bar"
    assert new_post["userId"] == 1
    assert "id" in new_post

def test_update_post():
    payload = {"title": "updated title", "body": "updated body", "userId": 1}
    response = requests.put(f"{BASE_URL}/1", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "updated title"
    assert data["body"] == "updated body"

def test_delete_post():
    response = requests.delete(f"{BASE_URL}/1")
    assert response.status_code == 200
