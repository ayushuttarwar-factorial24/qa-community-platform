"""
Configuration Module

Manages environment variables and application settings using Pydantic Settings.
Provides centralized configuration for MongoDB, API server, and matching algorithm.
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    
    Uses .env file for local development and environment variables in production.
    All sensitive data (like MongoDB URI) should be stored in .env file.
    """
    
    # MongoDB Configuration
    mongodb_uri: str = Field(
        ...,
        description="MongoDB Atlas connection string",
        validation_alias="MONGODB_URI"
    )
    mongodb_db_name: str = Field(
        default="qa_community",
        description="Database name for QA Community platform",
        validation_alias="MONGODB_DB_NAME"
    )
    
    # Connection Limits
    max_connections_per_user: int = Field(
        default=5,
        description="Maximum connections allowed per user",
        validation_alias="MAX_CONNECTIONS_PER_USER"
    )
    
    # API Configuration
    api_host: str = Field(
        default="0.0.0.0",
        description="API server host",
        validation_alias="API_HOST"
    )
    api_port: int = Field(
        default=8000,
        description="API server port",
        validation_alias="API_PORT"
    )
    api_reload: bool = Field(
        default=True,
        description="Auto-reload on code changes (dev only)",
        validation_alias="API_RELOAD"
    )
    
    # Application Settings
    app_name: str = "QA Community Profile Matching Platform"
    app_version: str = "1.0.0"
    
    # Matching Algorithm Configuration
    default_match_limit: int = Field(
        default=5,
        description="Default number of profile suggestions to return"
    )
    
    # Score weights for matching algorithm
    overlap_weight: float = Field(
        default=2.0,
        description="Weight for skill overlap count"
    )
    breadth_weight: float = Field(
        default=0.3,
        description="Weight for breadth of candidate's skills"
    )
    experience_weight: float = Field(
        default=1.5,
        description="Weight for years of experience"
    )
    role_exact_match_bonus: float = Field(
        default=0.5,
        description="Bonus score for exact job role match"
    )
    role_partial_match_bonus: float = Field(
        default=0.2,
        description="Bonus score for partial job role match"
    )
    
    # Caps for normalization
    max_experience_cap: int = Field(
        default=10,
        description="Maximum years of experience for scoring (capped)"
    )
    max_breadth_cap: int = Field(
        default=10,
        description="Maximum number of skills for breadth scoring (capped)"
    )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra='ignore'


# Global settings instance
settings = Settings()
