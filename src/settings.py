from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    postgres_host: str = "localhost"
    postgres_database_name: str = "auth_db"
    postgres_password: str = "postgres"
    postgres_port: int = 5433
    postgres_username: str = "postgres"

    # Explicit DSN (DATABASE_URL) wins; otherwise it's assembled from POSTGRES_*.
    database_url: str = ""

    jwt_secret: str = "change-me"
    jwt_algorithm: str = "HS256"
    jwt_expire_hours: int = 24
    jwt_refresh_expire_days: int = 30

    @model_validator(mode="after")
    def _build_database_url(self) -> "Settings":
        if not self.database_url:
            self.database_url = f"postgresql+asyncpg://{self.postgres_username}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_database_name}"
        return self
