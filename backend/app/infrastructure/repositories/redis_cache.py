"""Redis-backed repository/cache implementations."""

from __future__ import annotations

import json
from dataclasses import asdict
from typing import Optional

from loguru import logger

from app.models.prompts_models import PlatformPrompt, PromptSection
from app.models.response_models import AnalysisResult, PromptPayload
from app.repositories.interfaces import AnalysisRepository, PromptBundle, PromptRepository

try:
    import redis  # type: ignore
except ImportError:  # pragma: no cover - optional dependency
    redis = None  # type: ignore


class RedisRepositoryBase:
    """Common functionality for Redis-backed repositories."""

    def __init__(self, client: "redis.Redis", prefix: str, ttl: int) -> None:
        self._redis = client
        self._prefix = prefix
        self._ttl = ttl

    def _key(self, identifier: str) -> str:
        return f"{self._prefix}:{identifier}"


class RedisAnalysisRepository(RedisRepositoryBase, AnalysisRepository):
    """Redis cache for analysis results."""

    def save(self, result: AnalysisResult) -> None:
        try:
            self._redis.set(self._key(result.image_id), result.json(), ex=self._ttl)
        except Exception as exc:  # pragma: no cover - redis failure path
            logger.warning("Failed to cache analysis: %s", exc)

    def get(self, image_id: str) -> Optional[AnalysisResult]:
        try:
            payload = self._redis.get(self._key(image_id))
        except Exception as exc:  # pragma: no cover - redis failure path
            logger.warning("Failed to read cached analysis: %s", exc)
            return None
        if not payload:
            return None
        data = json.loads(payload)
        return AnalysisResult.parse_obj(data)


class RedisPromptRepository(RedisRepositoryBase, PromptRepository):
    """Redis cache for prompt bundles."""

    def save(self, bundle: PromptBundle) -> None:
        payload = {
            "image_id": bundle.image_id,
            "normalized": asdict(bundle.normalized),
            "prompts": [prompt.dict() for prompt in bundle.prompts],
        }
        try:
            self._redis.set(self._key(bundle.image_id), json.dumps(payload), ex=self._ttl)
        except Exception as exc:  # pragma: no cover - redis failure path
            logger.warning("Failed to cache prompt bundle: %s", exc)

    def get(self, image_id: str) -> Optional[PromptBundle]:
        try:
            payload = self._redis.get(self._key(image_id))
        except Exception as exc:  # pragma: no cover - redis failure path
            logger.warning("Failed to read cached prompt bundle: %s", exc)
            return None
        if not payload:
            return None

        data = json.loads(payload)
        normalized_data = data["normalized"]
        visual_cues = [PromptSection(**section) for section in normalized_data.get("visual_cues", [])]
        normalized = PlatformPrompt(
            reference_id=normalized_data["reference_id"],
            narrative=normalized_data["narrative"],
            persona=normalized_data.get("persona"),
            visual_cues=visual_cues,
            technical=normalized_data.get("technical", {}),
            motion=normalized_data.get("motion", {}),
        )
        prompts = [PromptPayload.parse_obj(item) for item in data.get("prompts", [])]
        return PromptBundle(image_id=image_id, normalized=normalized, prompts=prompts)
