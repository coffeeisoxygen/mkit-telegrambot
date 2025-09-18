"""SQLAlchemy async session for SQLite using aiosqlite."""

import contextlib
from collections.abc import AsyncGenerator

from loguru import logger
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
)

from config.settings import get_settings
from database.base_session import BaseAsyncSessionManager

settings = get_settings()


class SQLiteAsyncSessionManager(BaseAsyncSessionManager):
    def __init__(self, url: str):
        logger.debug(f"SQLite URL: {url}")

        engine = create_async_engine(
            url,
            echo=settings.APPDB.echo,
            pool_size=settings.APPDB.pool_size,
            max_overflow=settings.APPDB.max_overflow,
            pool_timeout=settings.APPDB.timeout,
        )
        super().__init__(engine=engine)


# singleton instance
sqlite_session_manager = SQLiteAsyncSessionManager(settings.APPDB.url)


# getter session
@contextlib.asynccontextmanager
async def get_sqlite_session() -> AsyncGenerator[AsyncSession, None]:
    """Provides an async session for SQLite."""
    async with sqlite_session_manager.session() as session:
        yield session
