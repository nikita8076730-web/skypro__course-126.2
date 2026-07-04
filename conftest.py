import pytest
<<<<<<< HEAD
import requests
import uuid

BASE_URL = "https://ru.yougile.com/api-v2"

AUTH_DATA = {
    "login": "",
    "password": "",
    "companyId": ""
}


@pytest.fixture(scope="session")
def api_token():
    """Получение API-ключа через авторизацию"""
    response = requests.post(
        f"{BASE_URL}/auth/keys",
        json=AUTH_DATA
    )
    assert response.status_code == 201, (
        f"Авторизация не удалась: {response.text}"
    )
    token = response.json().get("key")
    assert token is not None, "Токен не получен"
    print(f"\n✅ Токен получен: {token[:20]}...")
    return token


@pytest.fixture(scope="session")
def api_session(api_token):
    """Сессия requests с авторизацией через Bearer токен"""
    session = requests.Session()
    session.base_url = BASE_URL
    session.headers.update({
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    })
    yield session
    session.close()


@pytest.fixture
def project_data():
    """Данные для создания проекта"""
    return {
        "title": f"Тестовый проект {uuid.uuid4().hex[:8]}",
        "users": {
            "2a4b0539-c61c-40c1-a411-769a061b5803": "admin"
        }
    }


@pytest.fixture
def existing_project(api_session, project_data):
    """Создает проект и возвращает его ID"""
    response = api_session.post(f"{BASE_URL}/projects", json=project_data)
    assert response.status_code == 201
    project_id = response.json().get("id")
    assert project_id is not None
    yield project_id
    try:
        api_session.delete(f"{BASE_URL}/projects/{project_id}")
    except Exception:
        pass
