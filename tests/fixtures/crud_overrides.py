from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from grasp_api.crud.sensor_data import SensorDataCRUD
from tests.fixtures.database import get_session


async def override_get_sensor_data_crud(
    session: AsyncSession = Depends(get_session),
) -> SensorDataCRUD:
    return SensorDataCRUD(session=session)
