from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    GROQ_API_KEY: str
    TAVILY_API_KEY: str
    OPENAI_API_KEY: str = ""
    GOOGLE_API_KEY: str = ""
    BASE_URL: str = "http://localhost:8000"
    LOG_LEVEL: str = "INFO"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
