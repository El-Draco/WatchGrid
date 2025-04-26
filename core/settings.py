from pydantic import ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict
import oracledb
import asyncpg

class Settings(BaseSettings):

    DB_DSN: str
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_WALLET_LOC: str
    DB_WALLET_DIR: str
    DB_CONFIG_DIR: str
    DB_WALLET_PASSWORD: str


    TMDB_URL: str
    TMDB_API_KEY: str


    def get_connection(self):
        conn = oracledb.connect(
            user=settings.DB_USERNAME,
            password=settings.DB_PASSWORD,
            dsn=settings.DB_DSN,
            config_dir=settings.DB_CONFIG_DIR,
            wallet_location=settings.DB_WALLET_LOC,
            wallet_password=settings.DB_WALLET_PASSWORD
        )
        return conn


    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="forbid")


settings = Settings()
