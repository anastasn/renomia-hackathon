from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "Renomia AI Engine"
    app_version: str = "0.1.0"
    debug: bool = False

    # LLM provider — set via environment variable
    openai_api_key: str = ""
    # anthropic_api_key: str = ""

    # ChromaDB — local persistent storage
    chroma_persist_dir: str = "./data/chroma"

    # Embedding model
    embedding_model: str = "text-embedding-3-small"


settings = Settings()
