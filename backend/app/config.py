"""Centralized environment configuration."""

from __future__ import annotations

from functools import lru_cache
from typing import List

from pydantic import BaseSettings, Field, validator


class Settings(BaseSettings):
    """Application settings sourced from environment variables."""

    environment: str = Field(default="development")
    cors_allow_origins: List[str] = Field(default_factory=lambda: ["*"])

    # AI integrations
    anthropic_api_key: str | None = None
    claude_model: str = Field(default="claude-3-5-sonnet-20241022")
    claude_max_tokens: int = Field(default=4096, ge=512, le=8192)
    insightface_model_name: str = Field(default="antelopev2")
    insightface_model_dir: str | None = None

    # Persistence and caching
    database_url: str | None = None
    storage_backend: str = Field(default="memory")
    redis_url: str | None = None
    redis_analysis_ttl_seconds: int = Field(default=3600, ge=60)
    redis_prompt_ttl_seconds: int = Field(default=86_400, ge=300)
    redis_face_ttl_seconds: int = Field(default=604_800, ge=300)

    # Object storage
    aws_access_key_id: str | None = None
    aws_secret_access_key: str | None = None
    aws_s3_bucket: str | None = None
    aws_s3_region: str | None = None

    # File handling
    max_file_size: int = Field(default=50_000_000)
    allowed_formats: List[str] = Field(default_factory=lambda: ["jpg", "jpeg", "png", "webp"])

    class Config:
        env_file = ".env"
        case_sensitive = False

    @validator("environment")
    def _validate_environment(cls, value: str) -> str:
        allowed = {"development", "staging", "production", "test"}
        if value not in allowed:
            raise ValueError(f"environment must be one of {allowed}")
        return value

    @validator("storage_backend")
    def _validate_storage_backend(cls, value: str) -> str:
        allowed = {"memory", "hybrid"}
        if value not in allowed:
            raise ValueError(f"storage_backend must be one of {allowed}")
        return value


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance."""
    return Settings()


settings = get_settings()
