# 🛠 API Testing with Pytest

Этот репозиторий содержит автоматизированные тесты для API `jsonplaceholder.typicode.com`, написанные с использованием **pytest** и **requests**.

## 🚀 Установка зависимостей

Перед началом работы убедись, что у тебя установлен **Python 3.8+**.

### 1️⃣ Создай и активируй виртуальное окружение (рекомендуется)
```bash
python -m venv venv  # Создание виртуального окружения
source venv/bin/activate  # Для macOS/Linux
venv\Scripts\activate  # Для Windows
```

### 2️⃣ Установи зависимости
```bash
pip install --upgrade pip  # Обновление pip
pip install -r requirements.txt  # Установка зависимостей
```

## 📌 Запуск тестов
```bash
pytest -v
```

## 🔄 Обновление зависимостей
Если нужно обновить пакеты:
```bash
pip install --upgrade -r requirements.txt
```

## 📜 Генерация нового `requirements.txt`
Если ты установил новые зависимости и хочешь обновить `requirements.txt`:
```bash
pip freeze > requirements.txt
```

## 🚀 Интеграция с CI/CD
Если используешь GitHub Actions или другие CI/CD инструменты, добавь в `.github/workflows`:
```yaml
- name: Install dependencies
  run: |
    python -m pip install --upgrade pip
    pip install -r requirements.txt
```

---
