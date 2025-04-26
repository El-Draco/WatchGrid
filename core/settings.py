from pydantic import ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict
import oracledb
import asyncpg

import os
import base64
import zipfile
import streamlit as st


def prepare_wallet(wallet_base64):

    wallet_zip_path = "./wallet.zip"
    wallet_folder_path = "./wallet"

    # Save base64 text back into a zip file
    with open(wallet_zip_path, "wb") as f:
        f.write(base64.b64decode(wallet_base64))

    # Unzip into /tmp/wallet
    with zipfile.ZipFile(wallet_zip_path, "r") as zip_ref:
        zip_ref.extractall(wallet_folder_path)




class Settings(BaseSettings):

    DB_DSN: str
    DB_USERNAME: str
    DB_PASSWORD: str
    DB_WALLET_LOC: str
    DB_WALLET_DIR: str
    DB_CONFIG_DIR: str
    DB_WALLET_PASSWORD: str
    DB_WALLET_BASE64: str

    TMDB_URL: str
    TMDB_API_KEY: str

    def __init__(self):
        super(Settings, self).__init__()
        prepare_wallet(self.DB_WALLET_BASE64)

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
