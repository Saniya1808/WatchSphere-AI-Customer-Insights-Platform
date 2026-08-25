"""
WatchSphere AI v3.0 - Application Settings
Author: Powered by Saniya Maner (Infosys Internship Project 2026)
"""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Enterprise Application Settings powered by Pydantic v2 & pydantic-settings.
    Loads configuration from environment variables or .env file.
    """

    # Application Metadata
    APP_NAME: str = Field(default="WatchSphere AI – Customer Insights Platform")
    APP_VERSION: str = Field(default="3.0.0")
    APP_ENV: str = Field(default="development")
    DEBUG: bool = Field(default=True)

    # Server Configuration
    HOST: str = Field(default="127.0.0.1")
    PORT: int = Field(default=8000)
    API_V1_PREFIX: str = Field(default="/api/v1")

    # Database Configuration (SQLite default, PostgreSQL/MySQL compatible)
    DATABASE_URL: str = Field(default="sqlite:///./watchsphere.db")

    # Security Configuration
    SECRET_KEY: str = Field(default="watchsphere-super-secret-key-change-in-production-2026")
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60)
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(default=7)

    # Logging Configuration
    LOG_LEVEL: str = Field(default="INFO")
    LOG_DIR: str = Field(default="logs")
    SYSTEM_LOG_FILE: str = Field(default="logs/system.log")
    ERROR_LOG_FILE: str = Field(default="logs/error.log")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


# Instantiate global settings singleton
settings = Settings()
