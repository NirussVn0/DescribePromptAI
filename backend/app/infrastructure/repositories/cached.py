"""Cached repository decorators combining primary storage with Redis caches."""

from __future__ import annotations

from typing import Optional

from app.models.response_models import AnalysisResult
from app.repositories.interfaces import AnalysisRepository, PromptBundle, PromptRepository


class CachedAnalysisRepository(AnalysisRepository):
    """Write-through cache combining persistent storage with Redis."""

    def __init__(self, primary: AnalysisRepository, cache: Optional[AnalysisRepository] = None) -> None:
        self._primary = primary
        self._cache = cache

    def save(self, result: AnalysisResult) -> None:
        self._primary.save(result)
        if self._cache:
            self._cache.save(result)

    def get(self, image_id: str) -> AnalysisResult | None:
        if self._cache:
            cached = self._cache.get(image_id)
            if cached:
                return cached

        result = self._primary.get(image_id)
        if result and self._cache:
            self._cache.save(result)
        return result


class CachedPromptRepository(PromptRepository):
    """Write-through cache for prompts."""

    def __init__(self, primary: PromptRepository, cache: Optional[PromptRepository] = None) -> None:
        self._primary = primary
        self._cache = cache

    def save(self, bundle: PromptBundle) -> None:
        self._primary.save(bundle)
        if self._cache:
            self._cache.save(bundle)

    def get(self, image_id: str) -> PromptBundle | None:
        if self._cache:
            cached = self._cache.get(image_id)
            if cached:
                return cached

        bundle = self._primary.get(image_id)
        if bundle and self._cache:
            self._cache.save(bundle)
        return bundle
