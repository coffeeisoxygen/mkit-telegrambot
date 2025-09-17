"""Base class for SQLAlchemy async session managers."""

import contextlib
from collections.abc import AsyncGenerator

from loguru import logger
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
)


class BaseAsyncSessionManager:
    def __init__(self, engine: AsyncEngine):
        self.engine = engine
        self._sessionmaker = async_sessionmaker(
            bind=self.engine,
            expire_on_commit=False,
        )

    async def __aenter__(self):
        """Support async context manager for the engine manager itself."""
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: object | None,
    ):
        await self.close()

    async def close(self):
        """Dispose engine when shutting down app/lifespan."""
        await self.engine.dispose()

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        """Provide an async session with safe error handling."""
        async with self._sessionmaker() as session:
            try:
                yield session
            except Exception as e:
                await session.rollback()
                logger.error(f"Session error: {e!r}")
                raise
            finally:
                # async with udah auto close, tapi tambahan ini aman
                if session.is_active:
                    await session.close()
