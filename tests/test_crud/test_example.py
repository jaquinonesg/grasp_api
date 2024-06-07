import pytest
from fastapi.testclient import TestClient

from grasp_api.api.app import create_app
from grasp_api.crud.example import get_example_crud
from tests.fixtures.crud_overrides import override_get_example_crud
from tests.fixtures.database import setup_and_teardown  # noqa: F401

app = create_app()
client = TestClient(app)

app.dependency_overrides[get_example_crud] = override_get_example_crud


@pytest.mark.asyncio
async def test_create_example(setup_and_teardown):  # noqa: F811
    example = {
        "pk_example": "primary key",
        "string_example": "string1",
        "string2_example": "string2",
    }
    response = client.post("/grasp_api/v1/example", json=example)
    assert response.status_code == 201, response.text

    data = response.json()
    assert data["pk_example"] == "primary key"
    assert data["string_example"] == "string1"
    assert data["string2_example"] == "string2"


@pytest.mark.asyncio
async def test_read_example_with_inexistent_id(
    setup_and_teardown,  # noqa: F811
):
    example_id = "pdf50"
    response = client.get(f"/grasp_api/v1/{example_id}")
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == f"Example with id <{example_id}> not found!"


@pytest.mark.asyncio
async def test_read_example(setup_and_teardown):  # noqa: F811
    example = {
        "pk_example": "some_pk",
        "string_example": "string",
        "string2_example": "string1",
    }
    response = client.post("/grasp_api/v1/example", json=example)
    assert response.status_code == 201, response.text
    data = response.json()
    example_id = data["pk_example"]

    response = client.get(f"/grasp_api/v1/{example_id}")
    assert response.status_code == 200, response.text
    data = response.json()

    assert data["pk_example"] == "some_pk"
    assert data["string_example"] == "string"
    assert data["string2_example"] == "string1"
