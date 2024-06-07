from typing import Any, AsyncGenerator

import sqlalchemy.pool
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.ext.asyncio.engine import AsyncEngine

Session: async_sessionmaker[AsyncSession] = async_sessionmaker(
    class_=AsyncSession
)


ReadOnlySession: async_sessionmaker[AsyncSession] = async_sessionmaker(
    class_=AsyncSession
)


def get_db_url(db_config: dict[Any, Any], driver: str = "asyncpg") -> str:
    return (
        f"postgresql+{driver}://{db_config['user']}:{db_config['password']}"
        f"@{db_config['host']}:{db_config['port']}/{db_config['name']}"
    )


def configure_db_session(
    session_maker: async_sessionmaker[AsyncSession], db_config: dict[Any, Any]
) -> AsyncEngine:
    config = {"url": get_db_url(db_config)}
    if getattr(db_config, "POOL_CLASS", None):
        config["poolclass"] = getattr(sqlalchemy.pool, db_config["pool_class"])
    if getattr(db_config, "POOL_SIZE", None):
        config["pool_size"] = db_config["pool_session"]

    engine: AsyncEngine = create_async_engine(
        **config,
        # connect_args={"ssl": getattr(db_config, "SSLMODE", None) or "require"},
        connect_args={"ssl": getattr(db_config, "SSLMODE", None) or "disable"},
    )
    session_maker.configure(bind=engine)
    return engine


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with Session.begin() as session:
        yield session


async def get_read_only_session() -> AsyncGenerator[AsyncSession, None]:
    async with ReadOnlySession() as session:
        yield session
