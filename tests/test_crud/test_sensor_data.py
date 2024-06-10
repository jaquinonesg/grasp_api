import pytest
from fastapi.testclient import TestClient

from grasp_api.api.app import create_app
from grasp_api.crud.sensor_data import get_sensor_data_crud
from tests.fixtures.crud_overrides import override_get_sensor_data_crud
from tests.fixtures.database import setup_and_teardown  # noqa: F401
from tests.fixtures.payloads import (
    sensor_data_payload_incomplete,
    sensor_data_payload_success,
)

app = create_app()
client = TestClient(app)

app.dependency_overrides[get_sensor_data_crud] = override_get_sensor_data_crud


@pytest.mark.asyncio
async def test_post_sensor_data_sucess(setup_and_teardown):  # noqa: F811
    response = client.post(
        "/grasp_api/v1/sensor_data/", json=sensor_data_payload_success
    )
    assert response.status_code == 201, response.text

    data = response.json()

    assert data["sensor_id"] == "244138"
    assert data["dwell_time"] == "1.77"
    assert data["time"] == "2024-06-07T16:18:20.954212"


@pytest.mark.asyncio
async def test_post_sensor_data_with_incomplete_payload(
    setup_and_teardown,  # noqa: F811
):
    response = client.post(
        "/grasp_api/v1/sensor_data/", json=sensor_data_payload_incomplete
    )
    assert response.status_code == 422, response.text


@pytest.mark.asyncio
async def test_get_sensor_data_with_valid_date_range(
    setup_and_teardown, # noqa: F811
):
    response = client.post(
        "/grasp_api/v1/sensor_data/", json=sensor_data_payload_success
    )
    response = client.get(
        "/grasp_api/v1/sensor_data/?start_time=2024-01-01T00:00:00&end_time=2024-12-31T23:59:59&page=1&page_size=10"
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 10


@pytest.mark.asyncio
async def test_get_sensor_data_with_invalid_date_range(
    setup_and_teardown, # noqa: F811
):
    response = client.post(
        "/grasp_api/v1/sensor_data/", json=sensor_data_payload_success
    )
    response = client.get(
        "/grasp_api/v1/sensor_data/?start_time=2024-12-31T23:59:59&end_time=2024-01-01T00:00:00&page=1&page_size=10"
    )
    assert response.status_code == 422, response.text



@pytest.mark.asyncio
async def test_get_sensor_data_with_page_size_out_of_range(
    setup_and_teardown, # noqa: F811
):
    response = client.post(
        "/grasp_api/v1/sensor_data/", json=sensor_data_payload_success
    )
    response = client.get(
        "/grasp_api/v1/sensor_data/?start_time=2024-01-01T00:00:00&end_time=2024-12-31T23:59:59&page=1&page_size=101"
    )
    assert response.status_code == 422, response.text


@pytest.mark.asyncio
async def test_get_sensor_data_with_default_params(
    setup_and_teardown, # noqa: F811
):
    response = client.post(
        "/grasp_api/v1/sensor_data/", json=sensor_data_payload_success
    )
    response = client.get("/grasp_api/v1/sensor_data/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 10
