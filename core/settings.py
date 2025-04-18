from pydantic_settings import BaseSettings
import asyncpg

class Settings(BaseSettings):
    DB_URL: str

    TMDB_URL: str
    TMDB_API_KEY: str

    class Config:
        env_file = ".env"

    async def get_connection(self):
        return await asyncpg.connect(self.DB_URL)

settings = Settings()
