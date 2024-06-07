from fastapi.testclient import TestClient

from grasp_api.api import settings
from grasp_api.api.app import create_app
from grasp_api.crud.example import get_example_crud
from tests.fixtures.crud_overrides import override_get_example_crud
from tests.fixtures.database import setup_and_teardown  # noqa: F401

app = create_app()
client = TestClient(app)

app.dependency_overrides[get_example_crud] = override_get_example_crud


def test_read_main():
    response = client.get("/")
    expected_response = {
        "name": settings.project_name,
        "version": settings.version,
        "description": settings.description,
    }
    assert response.json() == expected_response
