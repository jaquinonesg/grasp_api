import binascii
from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, Query, status as http_status
from sqlalchemy.exc import IntegrityError

from grasp_api.api.v1.provision.base.serializers import (
    PubSubMessage,
    SensorDataOut,
)
from grasp_api.config.logger import logger
from grasp_api.crud.sensor_data import SensorDataCRUD, get_sensor_data_crud
from grasp_api.utils.errors import (
    InvalidDateRangeError,
    InvalidPageParameterError,
)
from grasp_api.utils.exceptions import (
    raise_bad_request_get,
    raise_bad_request_post,
    raise_conflict,
    raise_exception_with_ack,
    raise_not_found,
    raise_unprocessable_content,
)

router = APIRouter()


@router.get("/", response_model=List[SensorDataOut])
async def get_sensor_data(
    start_time: datetime = Query(
        "2024-01-01T00:00:00", description="Start time for the data range"
    ),
    end_time: datetime = Query(
        "2025-01-01T00:00:00", description="End time for the data range"
    ),
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(
        10, ge=1, le=100, description="Number of items per page"
    ),
    sensor_data: SensorDataCRUD = Depends(get_sensor_data_crud),
):
    try:
        return await sensor_data.get(start_time, end_time, page, page_size)
    except (InvalidDateRangeError, InvalidPageParameterError) as e:
        raise_unprocessable_content(e)


@router.post(
    "/", response_model=SensorDataOut, status_code=http_status.HTTP_201_CREATED
)
async def receive_pubsub_push(
    data: PubSubMessage,
    sensor_data: SensorDataCRUD = Depends(get_sensor_data_crud),
):
    try:
        return await sensor_data.create(data)
    except IntegrityError:
        raise_conflict(data)
    except binascii.Error:
        raise_bad_request_post(data)
    except Exception as e:
        # Return a generic 200 response to acknowledge the message but indicate processing error
        logger.error(
            f"Message received but processing failed. Unhandled error: {e}"
        )
        raise_exception_with_ack()
