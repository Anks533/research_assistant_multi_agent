from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from typing import Literal

import os

class Settings(BaseSettings):

    @staticmethod
    def get_env_file():
        env = os.getenv('RA_ENV', 'development') ## default as development
        if env == "development":
            return ".env"
        return f".env.{env}" ## construct dynamically

    model_config = SettingsConfigDict(
        env_file=get_env_file(),
        env_prefix= "RA_",
        env_file_encoding= "utf-8"
    )

    openai_api_key: str
    olostep_api_key: str
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"

    ### ------------ Property validations ---------------
    @field_validator("openai_api_key")
    @classmethod
    def validate_openai_api_key(cls, value: str) -> str :
        if not value or value.strip():
            raise ValueError("openai_api_key must not be empty!")
        return value
    
    @field_validator("olostep_api_key")
    @classmethod
    def validate_olostep_api_key(cls, value: str) -> str :
        if not value or value.strip():
            raise ValueError("olostep_api_key must not be empty!")
        return value

