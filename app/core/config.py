from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    AI_API_KEY: str = ""
    AI_MODEL_NAME: str = "gemini-2.5-flash"
    APP_ENV: str = "development"
    APP_HOST: str = "127.0.0.1"
    APP_PORT: int = 8000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()