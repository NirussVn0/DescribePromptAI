"""Dependency management helpers."""

from __future__ import annotations

from functools import lru_cache
from typing import Optional

from loguru import logger

from app.config import settings
from app.core.exceptions import ConfigurationError
from app.infrastructure.clients.anthropic_client import ClaudeVisionClient
from app.infrastructure.repositories.in_memory import (
    InMemoryAnalysisRepository,
    InMemoryImageRepository,
    InMemoryPromptRepository,
)
from app.infrastructure.repositories.postgres import PostgresAnalysisRepository, PostgresPromptRepository
from app.infrastructure.repositories.redis_cache import RedisAnalysisRepository, RedisPromptRepository
from app.infrastructure.repositories.cached import CachedAnalysisRepository, CachedPromptRepository
from app.infrastructure.repositories.s3 import S3ImageRepository
from app.repositories.interfaces import AnalysisRepository, ImageRepository, PromptRepository
from app.services.context_analyzer import ContextAnalyzerService
from app.services.face_detector import FaceDetectorService
from app.services.image_analyzer import (
    ClaudeVisionAnalyzer,
    FlorenceAnalyzer,
    ImageAnalyzerService,
    LlavaAnalyzer,
)
from app.services.pipeline import ImageProcessingPipeline
from app.services.prompt_generator import PromptGeneratorFactory
from app.services.prompt_service import PromptOrchestrator
from app.services.video_extender import VideoExtenderService

try:
    import redis  # type: ignore
except ImportError:  # pragma: no cover - optional dependency
    redis = None  # type: ignore


@lru_cache
def get_redis_client() -> "redis.Redis" | None:
    """Return a Redis client when configuration and dependency are available."""
    if not settings.redis_url:
        return None
    if redis is None:
        logger.warning("Redis dependency not installed; skipping cache wiring.")
        return None
    try:
        return redis.from_url(settings.redis_url, decode_responses=False)
    except Exception as exc:  # pragma: no cover - connection failure path
        logger.warning("Failed to connect to Redis: %s", exc)
        return None


@lru_cache
def get_image_repository() -> ImageRepository:
    """Provide an image repository implementation."""
    if settings.storage_backend == "hybrid" and settings.aws_s3_bucket:
        try:
            return S3ImageRepository(
                bucket=settings.aws_s3_bucket,
                region=settings.aws_s3_region,
                access_key=settings.aws_access_key_id,
                secret_key=settings.aws_secret_access_key,
            )
        except Exception as exc:  # pragma: no cover - configuration failure path
            logger.warning("Falling back to in-memory image repository: %s", exc)
    return InMemoryImageRepository()


@lru_cache
def get_analysis_repository() -> AnalysisRepository:
    """Provide an analysis repository implementation."""
    primary: AnalysisRepository
    if settings.storage_backend == "hybrid" and settings.database_url:
        try:
            primary = PostgresAnalysisRepository(settings.database_url)
        except Exception as exc:  # pragma: no cover - db failure path
            logger.warning("Falling back to in-memory analysis repository: %s", exc)
            primary = InMemoryAnalysisRepository()
    else:
        primary = InMemoryAnalysisRepository()

    cache_repo: Optional[AnalysisRepository] = None
    redis_client = get_redis_client()
    if redis_client:
        cache_repo = RedisAnalysisRepository(redis_client, prefix="analysis", ttl=settings.redis_analysis_ttl_seconds)

    if cache_repo:
        return CachedAnalysisRepository(primary=primary, cache=cache_repo)
    return primary


@lru_cache
def get_prompt_repository() -> PromptRepository:
    """Provide a prompt repository implementation."""
    primary: PromptRepository
    if settings.storage_backend == "hybrid" and settings.database_url:
        try:
            primary = PostgresPromptRepository(settings.database_url)
        except Exception as exc:  # pragma: no cover - db failure path
            logger.warning("Falling back to in-memory prompt repository: %s", exc)
            primary = InMemoryPromptRepository()
    else:
        primary = InMemoryPromptRepository()

    cache_repo: Optional[PromptRepository] = None
    redis_client = get_redis_client()
    if redis_client:
        cache_repo = RedisPromptRepository(redis_client, prefix="prompts", ttl=settings.redis_prompt_ttl_seconds)

    if cache_repo:
        return CachedPromptRepository(primary=primary, cache=cache_repo)
    return primary


@lru_cache
def get_face_detector() -> FaceDetectorService:
    """Provide a singleton face detector service."""
    redis_client = get_redis_client()
    return FaceDetectorService(
        model_name=settings.insightface_model_name,
        model_root=settings.insightface_model_dir,
        redis_client=redis_client,
        cache_ttl=settings.redis_face_ttl_seconds,
    )


@lru_cache
def get_context_analyzer() -> ContextAnalyzerService:
    """Provide a singleton context analyzer service."""
    return ContextAnalyzerService()


@lru_cache
def get_image_analyzer() -> ImageAnalyzerService:
    """Provide an image analyzer configured with available strategies."""
    claude_client = None
    if settings.anthropic_api_key:
        try:
            claude_client = ClaudeVisionClient(
                api_key=settings.anthropic_api_key,
                model=settings.claude_model,
                max_tokens=settings.claude_max_tokens,
            )
        except ConfigurationError as exc:  # pragma: no cover - config path
            logger.warning("Claude client configuration failed: %s", exc)
    strategies = [ClaudeVisionAnalyzer(client=claude_client), FlorenceAnalyzer(), LlavaAnalyzer()]
    return ImageAnalyzerService(strategies=strategies)


@lru_cache
def get_prompt_factory() -> PromptGeneratorFactory:
    """Expose the prompt generator factory."""
    return PromptGeneratorFactory()


@lru_cache
def get_pipeline() -> ImageProcessingPipeline:
    """Provide the image processing pipeline."""
    return ImageProcessingPipeline(
        image_repository=get_image_repository(),
        analysis_repository=get_analysis_repository(),
        analyzer=get_image_analyzer(),
        face_detector=get_face_detector(),
        context_analyzer=get_context_analyzer(),
    )


@lru_cache
def get_prompt_orchestrator() -> PromptOrchestrator:
    """Provide the prompt orchestration service."""
    return PromptOrchestrator(
        analysis_repository=get_analysis_repository(),
        prompt_repository=get_prompt_repository(),
        factory=get_prompt_factory(),
    )


@lru_cache
def get_video_extender() -> VideoExtenderService:
    """Provide the video extender service."""
    return VideoExtenderService()
