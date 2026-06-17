"""Video extension endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.models.request_models import VideoExtensionRequest
from app.models.response_models import VideoExtensionResponse
from app.services.prompt_service import PromptOrchestrator
from app.services.video_extender import VideoExtenderService
from app.utils.dependencies import get_prompt_orchestrator, get_video_extender

router = APIRouter()


@router.post("/extend", response_model=VideoExtensionResponse)
async def extend_video_prompt(
    payload: VideoExtensionRequest,
    extender: VideoExtenderService = Depends(get_video_extender),
    orchestrator: PromptOrchestrator = Depends(get_prompt_orchestrator),
) -> VideoExtensionResponse:
    """Extend an existing image prompt into a video-friendly version."""
    normalized_prompt = orchestrator.get_normalized_prompt(payload.image_id)
    return extender.extend(
        image_id=payload.image_id,
        prompt=normalized_prompt,
        motion_description=payload.motion_description,
        duration_seconds=payload.duration_seconds,
    )
