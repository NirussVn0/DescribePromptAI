"""Response payload definitions."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class FaceAttributes(BaseModel):
    """Extracted face-related attributes."""

    embedding_id: Optional[str] = None
    embedding_vector: Optional[List[float]] = None
    age_range: Optional[str] = None
    gender: Optional[str] = None
    emotions: List[str] = Field(default_factory=list)
    accessories: List[str] = Field(default_factory=list)


class ContextAttributes(BaseModel):
    """Environmental and stylistic attributes."""

    scene: List[str] = Field(default_factory=list)
    lighting: Optional[str] = None
    style_tags: List[str] = Field(default_factory=list)
    detected_objects: List[str] = Field(default_factory=list)


class AnalysisResult(BaseModel):
    """Combined analysis payload returned to clients."""

    image_id: str
    face: Optional[FaceAttributes] = None
    context: Optional[ContextAttributes] = None
    confidence: Dict[str, float] = Field(default_factory=dict)


class PromptPayload(BaseModel):
    """Generated prompt for a specific platform."""

    platform: str
    prompt: Dict[str, Any]
    metadata: Dict[str, Any] = Field(default_factory=dict)


class PromptGenerationResponse(BaseModel):
    """Container for multi-platform prompt generation responses."""

    image_id: str
    prompts: List[PromptPayload]


class VideoExtensionResponse(BaseModel):
    """Combined image and video prompt details."""

    image_id: str
    video_prompt: Dict[str, Any]
    duration_seconds: int
