from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from typing import Literal
from pathlib import Path

import os

# Root of your project
BASE_DIR = Path(__file__).resolve().parents[3]  # adjust if needed


class Settings(BaseSettings):

    @staticmethod
    def get_env_file():
        env = os.getenv('ENV', 'development') ## default as development
        if env == "development":
            print(BASE_DIR)
            return BASE_DIR / ".env"
        return BASE_DIR / f".env.{env}" ## construct dynamically

    model_config = SettingsConfigDict(
        env_file=get_env_file(),
        env_file_encoding= "utf-8"
    )

    openai_api_key: str
    olostep_api_key: str
    email_pwd: str
    to_email: str
    smtp_server: str
    smtp_port: int
    from_email: str
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"

    ### ------------ Property validations ---------------
    @field_validator("openai_api_key")
    @classmethod
    def validate_openai_api_key(cls, value: str) -> str :
        if not value or not value.strip():
            raise ValueError("openai_api_key must not be empty!")
        return value
    
    @field_validator("olostep_api_key")
    @classmethod
    def validate_olostep_api_key(cls, value: str) -> str :
        if not value or not value.strip():
            raise ValueError("olostep_api_key must not be empty!")
        return value

