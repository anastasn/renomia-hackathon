from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Renomia Backend"
    app_version: str = "0.1.0"
    debug: bool = False

    # SQLite database path (relative to the service root)
    database_url: str = "sqlite+aiosqlite:///./data/db.sqlite3"

    # URL of the AI engine service
    ai_engine_url: str = "http://ai-engine:8001"

    # CORS: comma-separated list of allowed origins
    cors_origins: str = "http://localhost:3000"

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",")]


settings = Settings()
