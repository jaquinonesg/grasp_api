from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from grasp_api.crud.example import ExampleCRUD
from tests.fixtures.database import get_session


async def override_get_example_crud(
    session: AsyncSession = Depends(get_session),
) -> ExampleCRUD:
    return ExampleCRUD(session=session)
