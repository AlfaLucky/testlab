import requests
import pytest

# API URL и ключ
BASE_URL = "https://api.thedogapi.com/v1"
API_KEY = "your_api_key_here"
HEADERS = {"x-api-key": API_KEY}


def test_get_breeds():
    """ Проверка получения списка пород собак """
    response = requests.get(f"{BASE_URL}/breeds", headers=HEADERS)

    assert response.status_code == 200, "Ошибка: код ответа не 200"

    data = response.json()
    assert isinstance(data, list), "Ответ не является списком"
    assert len(data) > 0, "Список пород пуст"
    assert "name" in data[0], "У породы нет имени"


def test_search_breed():
    """ Проверка поиска породы по названию """
    breed_name = "Labrador"
    response = requests.get(f"{BASE_URL}/breeds/search?q={breed_name}", headers=HEADERS)

    assert response.status_code == 200, "Ошибка: код ответа не 200"

    data = response.json()
    assert isinstance(data, list), "Ответ не является списком"
    assert len(data) > 0, "Порода не найдена"
    assert breed_name.lower() in data[0]["name"].lower(), "Имя породы не совпадает"


def test_get_random_image():
    """ Проверка получения случайного изображения собаки """
    response = requests.get(f"{BASE_URL}/images/search", headers=HEADERS)

    assert response.status_code == 200, "Ошибка: код ответа не 200"

    data = response.json()
    assert isinstance(data, list) and len(data) > 0, "Ответ не содержит изображений"
    assert "url" in data[0], "В ответе нет URL изображения"


def test_upload_image():
    """ Проверка загрузки изображения собаки """
    image_path = "dog.jpg"  # Заранее положи тестовое изображение в эту директорию
    with open(image_path, "rb") as img:
        files = {"file": img}
        response = requests.post(f"{BASE_URL}/images/upload", headers=HEADERS, files=files)

    assert response.status_code == 201, "Ошибка: изображение не загрузилось"

    data = response.json()
    assert "id" in data, "Ответ не содержит ID загруженного изображения"


# 🔹 Негативные тесты 🔹

def test_invalid_api_key():
    """ Проверка ошибки авторизации (неверный API-ключ) """
    headers = {"x-api-key": "invalid_key"}
    response = requests.get(f"{BASE_URL}/breeds", headers=headers)

    assert response.status_code == 403, "Ожидался код 403 (запрещено)"
    assert "message" in response.json(), "Ответ не содержит сообщения об ошибке"


def test_search_nonexistent_breed():
    """ Проверка поиска несуществующей породы """
    breed_name = "NonexistentDogBreed"
    response = requests.get(f"{BASE_URL}/breeds/search?q={breed_name}", headers=HEADERS)

    assert response.status_code == 200, "Ошибка: код ответа не 200"
    data = response.json()
    assert isinstance(data, list), "Ответ не является списком"
    assert len(data) == 0, "Найдено что-то, хотя породы не существует"


def test_get_image_with_invalid_param():
    """ Проверка запроса случайного изображения с некорректным параметром """
    response = requests.get(f"{BASE_URL}/images/search?limit=invalid", headers=HEADERS)

    assert response.status_code == 400, "Ожидался код 400 (неправильный запрос)"
    assert "message" in response.json(), "Ответ не содержит сообщения об ошибке"


def test_upload_invalid_file():
    """ Проверка загрузки не изображения (например, текстового файла) """
    invalid_file_path = "test.txt"
    with open(invalid_file_path, "w") as file:
        file.write("This is not an image.")

    with open(invalid_file_path, "rb") as file:
        files = {"file": file}
        response = requests.post(f"{BASE_URL}/images/upload", headers=HEADERS, files=files)

    assert response.status_code == 400, "Ожидался код 400 (неверный формат файла)"
    assert "message" in response.json(), "Ответ не содержит сообщения об ошибке"
