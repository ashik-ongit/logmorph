from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "Endpoint Security Intelligence"
    database_url: str = "sqlite:///../data/security.db"
    ollama_base_url: str | None = None
    ollama_model: str = "llama3.2:3b"
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
