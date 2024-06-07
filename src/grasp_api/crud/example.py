from fastapi import Depends, HTTPException, status as http_status
from sqlalchemy import delete, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio.session import AsyncSession

from grasp_api.api.v1.provision.base.serializers import ExampleRM
from grasp_api.config.logger import logger
from grasp_api.db.database import get_session
from grasp_api.db.models import Example
from grasp_api.utils.errors import NotFoundError


class ExampleCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, example_id: str) -> Example:
        statement = select(Example).where(Example.pk_example == example_id)
        results = await self.session.execute(statement=statement)
        example = results.scalar_one_or_none()

        if example is None:
            raise NotFoundError()

        return example

    async def get(self, example_id: str) -> Example:
        example = await self.get_by_id(example_id)
        return example

    async def create(self, data: ExampleRM) -> Example:
        try:
            values = data.dict()
            example = Example(**values)
            self.session.add(example)

            await self.session.flush()  # Use flush() instead of commit()
            await self.session.refresh(example)

            return example
        except IntegrityError as e:
            error_message = "Error creating example due an integrity restriction on the database, maybe PK duplicated."
            logger.error(f"{error_message}: {e}")

            raise HTTPException(
                status_code=http_status.HTTP_409_CONFLICT,
                detail="Primary key already exist in the database",
            )

    async def patch(self, example_id: str, data: ExampleRM) -> Example:
        example = await self.get(example_id=example_id)
        values = data.dict(exclude_unset=True)

        for key, value in values.items():
            setattr(example, key, value)

        self.session.add(example)
        await self.session.flush()
        await self.session.refresh(example)

        return example

    async def delete(self, example_id: str) -> bool:
        await self.get(example_id)
        statement = delete(Example).where(Example.pk_example == example_id)

        await self.session.execute(statement=statement)
        await self.session.flush()

        return True


async def get_example_crud(
    session: AsyncSession = Depends(get_session),
) -> ExampleCRUD:
    return ExampleCRUD(session=session)
