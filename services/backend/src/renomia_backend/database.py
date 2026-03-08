"""
Async SQLite database setup using SQLAlchemy 2.x.

Usage in routers:
    async with get_session() as session:
        result = await session.execute(select(MyModel))
"""

from collections.abc import AsyncGenerator
from pathlib import Path

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from renomia_backend.config import settings

# Ensure data directory exists
Path("data").mkdir(exist_ok=True)

engine = create_async_engine(settings.database_url, echo=settings.debug)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


async def create_tables() -> None:
    """Create all tables declared on Base. Called at startup."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
