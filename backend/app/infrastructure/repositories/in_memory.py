"""In-memory repository implementations for development and testing."""

from __future__ import annotations

from typing import Dict, Optional

from app.models.response_models import AnalysisResult
from app.repositories.interfaces import (
    AnalysisRepository,
    ImageRepository,
    PromptBundle,
    PromptRepository,
    StoredImage,
)


class InMemoryImageRepository(ImageRepository):
    """Simple in-memory image storage."""

    def __init__(self) -> None:
        self._store: Dict[str, StoredImage] = {}

    def save(self, record: StoredImage) -> None:
        self._store[record.image_id] = record

    def get(self, image_id: str) -> Optional[StoredImage]:
        return self._store.get(image_id)


class InMemoryAnalysisRepository(AnalysisRepository):
    """In-memory cache for analysis results."""

    def __init__(self) -> None:
        self._store: Dict[str, AnalysisResult] = {}

    def save(self, result: AnalysisResult) -> None:
        self._store[result.image_id] = result

    def get(self, image_id: str) -> Optional[AnalysisResult]:
        return self._store.get(image_id)


class InMemoryPromptRepository(PromptRepository):
    """In-memory prompt persistence."""

    def __init__(self) -> None:
        self._store: Dict[str, PromptBundle] = {}

    def save(self, bundle: PromptBundle) -> None:
        self._store[bundle.image_id] = bundle

    def get(self, image_id: str) -> Optional[PromptBundle]:
        return self._store.get(image_id)
