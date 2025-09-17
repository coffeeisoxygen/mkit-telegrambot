from functools import lru_cache
from pathlib import Path

from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict

from config.cfg_values import (
    ConfigEnvironment,
    DatabaseConfig,
    SchedulerConfig,
    SQLiteConfig,
    SQLServerConfig,
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=DEFAULT_ENV_FILE,
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="ignore",
        case_sensitive=False,
    )
    ENV: ConfigEnvironment = ConfigEnvironment()
    SETDB: DatabaseConfig = DatabaseConfig()
    APPDB: SQLiteConfig = SQLiteConfig()
    OTODB: SQLServerConfig  # ini wajib overide , no default values.
    SCHEDULER: SchedulerConfig = SchedulerConfig()


@lru_cache
def get_settings(_env_file: str | Path | None = None) -> Settings:
    """Get application settings.

    This function retrieves the application settings from the environment or a specified .env file.

    Args:
        _env_file (str | Path | None, optional): Path to the .env file. Defaults to None.

    Returns:
        1- Jika tidak passing env file fallback ke DEFAULT_ENV_FILE
        2- jika Default env tidak ada ada , fallback ke default pydantic settings
        3- jika all values missing , pydantic akan raise validation error
    """
    if _env_file is None:
        env_file = DEFAULT_ENV_FILE
        logger.debug(f" settings using env file: {env_file}")
    else:
        logger.debug(f" settings using env file: {_env_file}")
    return Settings(_env_file=env_file, _env_file_encoding="utf-8")  # type: ignore
