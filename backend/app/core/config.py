from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://gagelang:toor@localhost:5432/portfolio_db"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()