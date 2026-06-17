"""Scene and environment analysis services."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(slots=True)
class ContextDescriptor:
    """Normalized context descriptor returned by analyzers."""

    scene: List[str]
    lighting: str | None = None
    style_tags: List[str] | None = None
    detected_objects: List[str] | None = None


class ContextAnalyzerService:
    """Analyze environment and style details from an image."""

    async def analyze(self, image_id: str, _image_data: str) -> ContextDescriptor:
        """Return a placeholder descriptor until real model integration arrives."""
        return ContextDescriptor(
            scene=["indoor studio"],
            lighting="soft key lighting",
            style_tags=["cinematic", "high-detail"],
            detected_objects=["subject"],
        )
