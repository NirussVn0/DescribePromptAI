"""Prompt generation endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.models.request_models import PromptGenerationRequest
from app.models.response_models import PromptGenerationResponse
from app.services.prompt_service import PromptOrchestrator
from app.utils.constants import SUPPORTED_PLATFORMS
from app.utils.dependencies import get_prompt_orchestrator

router = APIRouter()


@router.post("/generate", response_model=PromptGenerationResponse)
async def generate_prompts(
    payload: PromptGenerationRequest,
    orchestrator: PromptOrchestrator = Depends(get_prompt_orchestrator),
) -> PromptGenerationResponse:
    """Generate platform-specific prompts from prior analysis."""
    platforms = payload.target_platforms or SUPPORTED_PLATFORMS
    normalized_platforms = list(dict.fromkeys(platform.lower() for platform in platforms))
    return orchestrator.generate_prompts(payload.image_id, normalized_platforms)
