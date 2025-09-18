# """SQLAlchemy async session for SQL Server using aioodbc."""

# from collections.abc import AsyncGenerator

# from loguru import logger
# from sqlalchemy.engine import URL
# from sqlalchemy.ext.asyncio import (
#     AsyncSession,
#     create_async_engine,
# )

# from config.settings import get_settings
# from database.base_session import BaseAsyncSessionManager

# settings = get_settings()


# # class MSSQLAsyncSessionManager(BaseAsyncSessionManager):
# #     def __init__(self, odbc_string: str):
# #         safe_odbc = odbc_string.replace(settings.OTODB.password or "", "***")
# #         logger.debug(f"ODBC connection string: {safe_odbc}")

# #         engine = create_async_engine(
# #             URL.create("mssql+aioodbc", query={"odbc_connect": odbc_string}),
# #             echo=settings.OTODB.echo,
# #             pool_size=settings.OTODB.pool_size,
# #             max_overflow=settings.OTODB.max_overflow,
# #             pool_timeout=settings.OTODB.timeout,
# #         )
# #         super().__init__(engine=engine)


# # singleton instance
# mssql_session_manager = MSSQLAsyncSessionManager(settings.OTODB.odbc_string)


# # getter session
# @logger.catch(message="Error getting mssql session", reraise=True)
# async def get_mssql_session() -> AsyncGenerator[AsyncSession, None]:
#     """Provides an async session for SQL Server."""
#     async with mssql_session_manager.session() as session:
#         yield session
