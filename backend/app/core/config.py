from typing import Annotated, Any, Literal

from pydantic import AnyUrl, BeforeValidator, RedisDsn, computed_field
from pydantic.networks import UrlConstraints
from pydantic_settings import BaseSettings, SettingsConfigDict


class SQLiteDsn(AnyUrl):
    """A type that will accept any SQLite DSN.

    * User info required
    * TLD not required
    * Host not required
    """

    _constraints = UrlConstraints(
        allowed_schemes=["sqlite", "sqlite+aiosqlite"],
        host_required=False,
    )


def parse_cors(v: Any) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",") if i.strip()]
    elif isinstance(v, list | str):
        return v
    raise ValueError(v)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        # Use top level .env file (one level above ./backend/)
        env_file="../.env",
        env_ignore_empty=True,
        extra="ignore",
    )
    # Project-level settings
    PROJECT_NAME: str
    ENVIRONMENT: Literal["local", "staging", "uat", "production"]

    # Backend and APIs
    API_V1_PREFIX: str
    BACKEND_CORS_ORIGINS: Annotated[list[AnyUrl] | str, BeforeValidator(parse_cors)] = (
        []
    )
    FRONTEND_HOST: str

    @computed_field  # type: ignore[prop-decorator]
    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS] + [
            self.FRONTEND_HOST
        ]

    # Database
    SQLITE_SCHEME: str
    SQLITE_DB: str

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_SQLITE_DB_URI(self) -> SQLiteDsn:
        return SQLiteDsn.build(
            host="",
            scheme=self.SQLITE_SCHEME,
            path=self.SQLITE_DB,
        )

    REDIS_HOST: str
    REDIS_SCHEME: str
    REDIS_CACHE_TTL: int

    @computed_field  # type: ignore[prop-decorator]
    @property
    def REDIS_URI(self) -> AnyUrl:
        return RedisDsn.build(
            host=self.REDIS_HOST,
            scheme=self.REDIS_SCHEME,
        )


settings = Settings()  # type: ignore
