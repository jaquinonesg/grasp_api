import base64
import binascii
import json
from datetime import datetime
from typing import List

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio.session import AsyncSession

from grasp_api.api.v1.provision.base.serializers import (
    PubSubMessage,
    SensorDataIn,
    SensorDataOut,
)
from grasp_api.config.logger import logger
from grasp_api.db.database import get_session
from grasp_api.db.models import SensorData
from grasp_api.utils.errors import (
    InvalidDateRangeError,
    InvalidPageParameterError,
    NotFoundError,
)


class SensorDataCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(
        self,
        start_time: datetime,
        end_time: datetime,
        page: int,
        page_size: int,
    ) -> List[SensorDataOut]:
        if start_time >= end_time:
            raise InvalidDateRangeError(
                "start_time must be earlier than end_time"
            )
        if page <= 0:
            raise InvalidPageParameterError(
                "Page number must be greater than 0"
            )
        if page_size <= 0:
            raise InvalidPageParameterError("Page size must be greater than 0")

        offset = (page - 1) * page_size
        statement = (
            select(SensorData)
            .where(SensorData.time >= start_time, SensorData.time <= end_time)
            .order_by(SensorData.time)
            .offset(offset)
            .limit(page_size)
        )

        result = await self.session.execute(statement=statement)
        data = result.scalars().all()

        return data if data is not None else []

    async def create(self, data: PubSubMessage) -> SensorDataIn:
        data = await self.get_json(data)
        values = data.dict()
        new_sensor_data = SensorData(**values)
        try:
            self.session.add(new_sensor_data)
            await self.session.flush()
            await self.session.refresh(new_sensor_data)
            return new_sensor_data
        except IntegrityError as e:
            error_message = "Error creating sensor_data due an integrity restriction on the database, maybe PK duplicated."
            logger.error(f"{error_message}: {e}")
            raise IntegrityError

    async def fill_if_padding_is_missing(self, encoded_data: str) -> str:
        # Add filling if required to guarantee being able to decode the message
        missing_padding = len(encoded_data) % 4
        if missing_padding:
            warning_message = "Encoded data is incomplete. Might be due to a codification error or data loss."
            logger.warning(warning_message)
            encoded_data += "=" * (4 - missing_padding)
        return encoded_data

    async def get_json(self, data: PubSubMessage) -> SensorDataIn:
        # Decode and parse data to json
        encoded_data = data.message.data
        encoded_data = await self.fill_if_padding_is_missing(encoded_data)

        try:
            decoded_data = base64.b64decode(data.message.data).decode("utf-8")
            message_json = json.loads(decoded_data)

            sensor_data = SensorDataIn(
                sensor_id=str(message_json["v0"]),
                dwell_time=str(message_json["v18"]),
                time=message_json["Time"],
            )
        except binascii.Error as e:
            error_message = "Error decoding message"
            logger.error(f"{error_message}: {e}")
            raise binascii.Error
        return sensor_data


async def get_sensor_data_crud(
    session: AsyncSession = Depends(get_session),
) -> SensorDataCRUD:
    return SensorDataCRUD(session=session)
