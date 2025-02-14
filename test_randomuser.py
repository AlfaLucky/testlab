import pytest
import requests

BASE_URL = "https://randomuser.me/api/"

@pytest.mark.parametrize("results", [1, 5, 10, 20, 50])
def test_generate_users(results):
    """Позитивный тест: генерация случайных пользователей"""
    response = requests.get(BASE_URL, params={"results": results})
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert len(data["results"]) == results

@pytest.mark.parametrize("gender", ["male", "female"])
def test_filter_by_gender(gender):
    """Позитивный тест: фильтрация по полу"""
    response = requests.get(BASE_URL, params={"gender": gender})
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    for user in data["results"]:
        assert user["gender"] == gender

@pytest.mark.parametrize("nat", ["us", "gb", "fr", "de", "au", "br"])
def test_filter_by_nationality(nat):
    """Позитивный тест: фильтрация по национальности"""
    response = requests.get(BASE_URL, params={"nat": nat})
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    for user in data["results"]:
        assert user["nat"].lower() == nat.lower()

@pytest.mark.parametrize("fields", ["name,email", "dob,phone", "location", "login,picture"])
def test_include_fields(fields):
    """Позитивный тест: включение только определенных полей в ответ"""
    response = requests.get(BASE_URL, params={"inc": fields})
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    for user in data["results"]:
        included_fields = fields.split(",")
        assert all(field in user for field in included_fields)

@pytest.mark.parametrize("seed", ["abc", "random", "test123"])
def test_seed_parameter(seed):
    """Позитивный тест: использование seed для одинакового результата"""
    response1 = requests.get(BASE_URL, params={"seed": seed})
    response2 = requests.get(BASE_URL, params={"seed": seed})
    assert response1.status_code == response2.status_code == 200
    assert response1.json() == response2.json()

@pytest.mark.parametrize("invalid_param,value", [
    ("results", -1),   # Негативный тест: отрицательное значение
    ("results", "abc"),  # Неверный тип данных
    ("gender", "unknown"),  # Неверный пол
    ("nat", "xyz"),   # Несуществующая национальность
    ("format", "invalid"),  # Неверный формат
    ("seed", ""),  # Пустой seed
])
def test_invalid_parameters(invalid_param, value):
    """Негативный тест: запрос с некорректными параметрами"""
    response = requests.get(BASE_URL, params={invalid_param: value})
    assert response.status_code in [400, 200]
    data = response.json()
    assert "error" in data or "info" in data

@pytest.mark.parametrize("missing_param", ["results", "gender", "nat"])
def test_missing_required_parameters(missing_param):
    """Негативный тест: отсутствие обязательных параметров"""
    params = {"results": 5, "gender": "male", "nat": "us"}
    del params[missing_param]
    response = requests.get(BASE_URL, params=params)
    assert response.status_code == 200  # API допускает пропущенные параметры
    data = response.json()
    assert "results" in data

@pytest.mark.parametrize("headers", [{"User-Agent": "Mozilla/5.0"}, {"Authorization": "Bearer fake_token"}])
def test_custom_headers(headers):
    """Позитивный тест: отправка запросов с разными заголовками"""
    response = requests.get(BASE_URL, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "results" in data

@pytest.mark.parametrize("timeout", [0.01, 5])
def test_request_timeout(timeout):
    """Негативный тест: проверка тайм-аута запроса"""
    try:
        response = requests.get(BASE_URL, timeout=timeout)
        assert response.status_code == 200
    except requests.exceptions.Timeout:
        assert True  # Ожидаемое поведение при малом таймауте
