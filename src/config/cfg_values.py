"""nested model for settings."""

from enum import StrEnum

from pydantic import BaseModel, field_validator


class EnvironmentEnums(StrEnum):
    """enum for environment."""

    PRODUCTION = "PRODUCTION"
    DEVELOPMENT = "DEVELOPMENT"
    TESTING = "TESTING"


class ConfigEnvironment(BaseModel):
    """core config for environment."""

    environment: EnvironmentEnums = EnvironmentEnums.PRODUCTION
    name: str = "MKIT-TELEGRAMBOT"
    debug: bool = False

    @field_validator("environment", mode="before")
    @classmethod
    def normalize_env(cls, v: str) -> str:
        if isinstance(v, str):
            v = v.upper()
        return v


class DatabaseConfig(BaseModel):
    echo: bool = False
    pool_size: int = 5
    max_overflow: int = 10


class SQLiteConfig(DatabaseConfig):
    url: str = "sqlite+aiosqlite:///./mkittelebot.db"
    timeout: int = 30  # lock wait timeout


class SQLServerConfig(DatabaseConfig):
    driver: str
    server: str
    database: str
    username: str | None = None
    password: str | None = None
    timeout: int = 15  # connection timeout

    @property
    def odbc_string(self) -> str:
        auth = (
            f"UID={self.username};PWD={self.password};"
            if self.username
            else "Trusted_Connection=yes;Encrypt=No"
        )
        return f"DRIVER={{{self.driver}}};SERVER={self.server};DATABASE={self.database};{auth}"


class SchedulerConfig(BaseModel):
    timezone: str = "Asia/Jakarta"  # timezone for scheduler
    sqlite_url: str = "sqlite:///jobs.sqlite"  # SQLite URL for job storage
    max_instances: int = (
        3  # Jumlah maksimum instance job yang boleh berjalan secara bersamaan.
    )
    coalesce: bool = False  # Jika True, job yang tertunda akan digabungkan menjadi satu eksekusi saat scheduler berjalan.
    thread_pool_size: int = 20  # Jumlah maksimum thread dalam ThreadPoolExecutor.
    process_pool_size: int = 5  # Jumlah maksimum proses dalam ProcessPoolExecutor


class TelegramConfig(BaseModel):
    API_ID: int
    API_HASH: str
    BOT_TOKEN: str
    ADMIN_ID: int
    ADMIN_PHONE: str
    ADMIN_NAME: str
