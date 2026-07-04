import uuid


class TestProjects:
    """Тесты для методов работы с проектами YouGile"""

    def test_create_project_positive(self, api_session, project_data):
        """Позитивный тест: создание проекта с валидными данными"""
        response = api_session.post(
            f"{api_session.base_url}/projects",
            json=project_data
        )
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        project_id = data["id"]

        get_response = api_session.get(
            f"{api_session.base_url}/projects/{project_id}"
        )
        assert get_response.status_code == 200
        project = get_response.json()

        assert project.get("title") == project_data["title"]
        assert "users" in project
        assert len(project["users"]) > 0

        api_session.delete(f"{api_session.base_url}/projects/{project_id}")

    def test_create_project_negative_missing_title(self, api_session):
        """Негативный тест: создание проекта без обязательного поля title"""
        invalid_data = {
            "users": {
                "2a4b0539-c61c-40c1-a411-769a061b5803": "admin"
            }
        }
        response = api_session.post(
            f"{api_session.base_url}/projects",
            json=invalid_data
        )
        assert response.status_code == 400
        assert "error" in response.json() or "message" in response.json()

    def test_create_project_negative_invalid_users(self, api_session):
        """Негативный тест: создание проекта с некорректным полем users"""
        invalid_data = {
            "title": "Проект с ошибкой",
            "users": "invalid_format"
        }
        response = api_session.post(
            f"{api_session.base_url}/projects",
            json=invalid_data
        )
        assert response.status_code == 400

    def test_update_project_positive(self, api_session, existing_project):
        """Позитивный тест: обновление проекта"""
        new_title = f"Обновленное название {uuid.uuid4().hex[:8]}"
        update_data = {
            "title": new_title,
            "users": {
                "2a4b0539-c61c-40c1-a411-769a061b5803": "admin"
            }
        }

        response = api_session.put(
            f"{api_session.base_url}/projects/{existing_project}",
            json=update_data
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("id") == existing_project

        get_response = api_session.get(
            f"{api_session.base_url}/projects/{existing_project}"
        )
        assert get_response.status_code == 200
        project = get_response.json()
        assert project.get("title") == new_title

    def test_update_project_negative_not_found(self, api_session):
        """Негативный тест: обновление несуществующего проекта"""
        fake_id = "00000000-0000-0000-0000-000000000000"
        update_data = {
            "title": "Новое имя",
            "users": {}
        }
        response = api_session.put(
            f"{api_session.base_url}/projects/{fake_id}",
            json=update_data
        )
        assert response.status_code == 404

    def test_update_project_negative_empty_title(
            self, api_session, existing_project
    ):
        """Негативный тест: обновление с пустым названием"""
        update_data = {
            "title": "",
            "users": {}
        }
        response = api_session.put(
            f"{api_session.base_url}/projects/{existing_project}",
            json=update_data
        )
        assert response.status_code == 400

    def test_get_project_positive(self, api_session, existing_project):
        """Позитивный тест: получение проекта по ID"""
        response = api_session.get(
            f"{api_session.base_url}/projects/{existing_project}"
        )
        assert response.status_code == 200
        data = response.json()
        assert data.get("id") == existing_project
        assert "title" in data
        assert "users" in data

    def test_get_project_negative_not_found(self, api_session):
        """Негативный тест: получение несуществующего проекта"""
        fake_id = "00000000-0000-0000-0000-000000000000"
        response = api_session.get(
            f"{api_session.base_url}/projects/{fake_id}"
        )
        assert response.status_code == 404

    def test_get_project_negative_invalid_id(self, api_session):
        """Негативный тест: некорректный формат ID"""
        invalid_id = "not-a-valid-uuid"
        response = api_session.get(
            f"{api_session.base_url}/projects/{invalid_id}"
        )
        assert response.status_code == 404
