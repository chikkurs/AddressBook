from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite+aiosqlite:///./address_book.db"

    class Config:
        env_file = ".env"


settings = Settings()
