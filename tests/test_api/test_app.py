from fastapi.testclient import TestClient

from grasp_api.api import settings
from grasp_api.api.app import create_app

app = create_app()
client = TestClient(app)


def test_read_main():
    response = client.get("/")
    expected_response = {
        "name": settings.project_name,
        "version": settings.version,
        "description": settings.description,
    }
    assert response.json() == expected_response
