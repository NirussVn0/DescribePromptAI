"""Request payload definitions."""

from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field


class ImageUploadRequest(BaseModel):
    """Represents an image upload request body."""

    filename: str = Field(..., description="Original file name")
    content_type: str = Field(..., description="MIME type of the uploaded image")
    data_base64: str = Field(..., description="Base64-encoded image payload")


class AnalysisRequest(BaseModel):
    """Request for triggering multimodal analysis."""

    image_id: str = Field(..., description="Identifier of the uploaded image")
    modes: List[str] = Field(default_factory=lambda: ["face", "context"])
    refresh_cache: bool = Field(default=False)


class PromptGenerationRequest(BaseModel):
    """Request for generating prompts from an analyzed image."""

    image_id: str = Field(..., description="Identifier of the analyzed image")
    target_platforms: List[str] = Field(default_factory=lambda: ["sora", "runway", "pika", "luma"])


class VideoExtensionRequest(BaseModel):
    """Request for extending image prompts into video prompts."""

    image_id: str = Field(..., description="Identifier of the analyzed image")
    motion_description: str = Field(..., description="User-provided motion or action details")
    duration_seconds: Optional[int] = Field(default=10, ge=1, le=120)
