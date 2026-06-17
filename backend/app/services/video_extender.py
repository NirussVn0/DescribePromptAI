"""Video prompt extension services."""

from __future__ import annotations

from dataclasses import dataclass

from app.models.prompts_models import PlatformPrompt
from app.models.response_models import VideoExtensionResponse


@dataclass(slots=True)
class VideoExtensionConfig:
    """Configuration for video prompt synthesis."""

    default_duration: int = 12


class VideoExtenderService:
    """Service composing video prompts from image prompts and motion cues."""

    def __init__(self, config: VideoExtensionConfig | None = None) -> None:
        self._config = config or VideoExtensionConfig()

    def extend(
        self,
        image_id: str,
        prompt: PlatformPrompt,
        motion_description: str,
        duration_seconds: int | None = None,
    ) -> VideoExtensionResponse:
        """Create a video-oriented prompt representation."""
        duration = duration_seconds or self._config.default_duration
        video_prompt = {
            "reference_id": prompt.reference_id,
            "narrative": prompt.narrative,
            "motion": motion_description,
            "persona": prompt.persona,
            "visual_cues": [
                {"title": section.title, "content": section.content, "weight": section.weight}
                for section in prompt.visual_cues
            ],
            "technical": {
                **prompt.technical,
                "duration_seconds": str(duration),
            },
        }
        return VideoExtensionResponse(
            image_id=image_id,
            video_prompt=video_prompt,
            duration_seconds=duration,
        )
