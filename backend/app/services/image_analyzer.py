"""Image analysis strategy implementations."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from loguru import logger

from app.core.exceptions import AnalysisError, ConfigurationError
from app.infrastructure.clients.anthropic_client import ClaudeVisionClient
from app.models.response_models import AnalysisResult, ContextAttributes, FaceAttributes
from app.repositories.interfaces import StoredImage


class ImageAnalysisStrategy(ABC):
    """Contract for pluggable image analysis strategies."""

    name: str

    @abstractmethod
    async def analyze(self, image: StoredImage, modes: List[str]) -> AnalysisResult:
        """Run analysis on the provided image and return structured data."""


class ClaudeVisionAnalyzer(ImageAnalysisStrategy):
    """Anthropic Claude-based multimodal analysis."""

    name = "claude"

    def __init__(self, client: ClaudeVisionClient | None = None) -> None:
        self._client = client

    async def analyze(self, image: StoredImage, modes: List[str]) -> AnalysisResult:
        """Call Claude Vision when configuration permits, otherwise fall back."""
        if not self._client:
            logger.warning("ClaudeVisionAnalyzer running in fallback mode.")
            return self._fallback(image_id=image.image_id)

        try:
            payload = await self._client.analyse(
                image_base64=image.data_base64,
                media_type=image.content_type,
                modes=modes,
            )
        except ConfigurationError:
            raise
        except Exception as exc:  # pragma: no cover - network failure
            raise AnalysisError(f"Claude vision invocation failed: {exc}") from exc

        face_block = payload.get("face") or {}
        context_block = payload.get("context") or {}

        face = None
        if "face" in modes:
            face = FaceAttributes(
                age_range=face_block.get("age_range"),
                gender=face_block.get("gender"),
                emotions=[value for value in face_block.get("emotions", []) if isinstance(value, str)],
                accessories=[value for value in face_block.get("accessories", []) if isinstance(value, str)],
            )

        context = None
        if "context" in modes:
            context = ContextAttributes(
                scene=[value for value in context_block.get("scene", []) if isinstance(value, str)],
                lighting=context_block.get("lighting"),
                style_tags=[value for value in context_block.get("style_tags", []) if isinstance(value, str)],
                detected_objects=[value for value in context_block.get("detected_objects", []) if isinstance(value, str)],
            )

        confidence_value = payload.get("confidence")
        try:
            confidence = float(confidence_value)
        except (TypeError, ValueError):
            confidence = 0.82

        return AnalysisResult(
            image_id=image.image_id,
            face=face,
            context=context,
            confidence={self.name: confidence},
        )

    @staticmethod
    def _fallback(image_id: str) -> AnalysisResult:
        """Deterministic fallback to keep pipeline operable offline."""
        return AnalysisResult(
            image_id=image_id,
            face=FaceAttributes(
                age_range="25-35",
                gender="unspecified",
                emotions=["neutral"],
                accessories=[],
            ),
            context=ContextAttributes(
                scene=["indoor studio"],
                lighting="soft key lighting",
                style_tags=["cinematic"],
                detected_objects=["primary subject"],
            ),
            confidence={ClaudeVisionAnalyzer.name: 0.4},
        )


class FlorenceAnalyzer(ImageAnalysisStrategy):
    """Microsoft Florence-2 based vision analysis (placeholder)."""

    name = "florence-2"

    async def analyze(self, image: StoredImage, modes: List[str]) -> AnalysisResult:
        """Placeholder returning lightweight cues to complement Claude Vision."""
        context = ContextAttributes(
            scene=["studio backdrop"],
            lighting="controlled",
            style_tags=["balanced"],
            detected_objects=["subject"],
        ) if "context" in modes else None
        return AnalysisResult(
            image_id=image.image_id,
            context=context,
            confidence={self.name: 0.35},
        )


class LlavaAnalyzer(ImageAnalysisStrategy):
    """LLaVA multi-modal analysis implementation (placeholder)."""

    name = "llava"

    async def analyze(self, image: StoredImage, modes: List[str]) -> AnalysisResult:
        face = FaceAttributes(
            emotions=["confident"],
            accessories=["minimal jewelry"],
        ) if "face" in modes else None
        return AnalysisResult(
            image_id=image.image_id,
            face=face,
            confidence={self.name: 0.3},
        )


class ImageAnalyzerService:
    """Coordinator responsible for selecting and executing analysis strategies."""

    def __init__(self, strategies: List[ImageAnalysisStrategy]) -> None:
        if not strategies:
            raise ValueError("at least one analysis strategy must be provided")
        self._strategies = {strategy.name: strategy for strategy in strategies}

    async def analyze(self, image: StoredImage, modes: List[str]) -> AnalysisResult:
        """Execute configured strategies and build a consolidated result."""
        aggregated_face: Optional[FaceAttributes] = None
        aggregated_context: Optional[ContextAttributes] = None
        confidences: Dict[str, float] = {}

        for name, strategy in self._strategies.items():
            try:
                result = await strategy.analyze(image, modes)
            except ConfigurationError as exc:
                logger.warning("Skipping %s due to configuration issue: %s", name, exc)
                continue
            except Exception as exc:
                raise AnalysisError(f"{name} analysis failed: {exc}") from exc

            if result.face and "face" in modes and not aggregated_face:
                aggregated_face = result.face
            if result.context and "context" in modes and not aggregated_context:
                aggregated_context = result.context
            confidences.update(result.confidence)

        if "face" not in modes:
            aggregated_face = None
        if "context" not in modes:
            aggregated_context = None

        if not confidences:
            confidences = {"fallback": 0.25}

        return AnalysisResult(
            image_id=image.image_id,
            face=aggregated_face,
            context=aggregated_context,
            confidence=confidences,
        )
