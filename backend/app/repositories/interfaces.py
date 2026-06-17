"""Repository interfaces for DescribePromptAI."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Protocol

from app.models.prompts_models import PlatformPrompt
from app.models.response_models import AnalysisResult, PromptPayload


@dataclass(slots=True)
class StoredImage:
    """Represents an image persisted in the repository."""

    image_id: str
    filename: str
    content_type: str
    data_base64: str
    size_bytes: int


class ImageRepository(Protocol):
    """Abstract repository for images."""

    def save(self, record: StoredImage) -> None:
        ...

    def get(self, image_id: str) -> Optional[StoredImage]:
        ...


class AnalysisRepository(Protocol):
    """Abstract repository for analysis results."""

    def save(self, result: AnalysisResult) -> None:
        ...

    def get(self, image_id: str) -> Optional[AnalysisResult]:
        ...


@dataclass(slots=True)
class PromptBundle:
    """Aggregated prompt data for an image."""

    image_id: str
    normalized: PlatformPrompt
    prompts: list[PromptPayload]


class PromptRepository(Protocol):
    """Abstract repository for generated prompts."""

    def save(self, bundle: PromptBundle) -> None:
        ...

    def get(self, image_id: str) -> Optional[PromptBundle]:
        ...
