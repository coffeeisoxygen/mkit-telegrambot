"""utility functions for database operations."""

import asyncio

from loguru import logger
from sqlalchemy import text


async def test_connection(session_manager) -> dict:  # noqa: ANN001
    """Test DB connection and return result dict with status + version."""
    result_info = {
        "db": session_manager.engine.dialect.name.lower(),
        "status": "down",
        "version": None,
        "error": None,
    }

    try:
        dialect = session_manager.engine.dialect.name.lower()

        version_queries = {
            "mssql": text("SELECT @@VERSION"),
            "sqlite": text("SELECT sqlite_version()"),
        }

        query = version_queries.get(dialect, text("SELECT 1"))

        async with session_manager.engine.connect() as conn:
            result = await conn.execute(query)
            version = result.scalar()

        result_info["status"] = "up"
        result_info["version"] = version
        logger.info(f"{dialect.upper()} ✅ | Version: {version}")

    except Exception as e:
        result_info["error"] = str(e)
        logger.error(f"❌ Error testing {result_info['db']} connection: {e}")

    return result_info


async def test_all_connections(session_managers: list) -> list[dict]:
    """Test all DB connections and return list of dict results."""
    results = await asyncio.gather(
        *(test_connection(manager) for manager in session_managers),
        return_exceptions=False,
    )
    return results


async def close_all_engines(session_managers: list):
    """Dispose all database engines on shutdown."""
    for manager in session_managers:
        db_name = manager.__class__.__name__.replace("AsyncSessionManager", "")
        try:
            await manager.close()
            logger.info(f"{db_name} engine closed 📴")
        except Exception as e:
            logger.error(f"Error closing {db_name} engine: {e}")
