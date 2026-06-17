"""Endpoints orchestrating multimodal analysis."""

from __future__ import annotations

from fastapi import APIRouter, Depends

from app.models.request_models import AnalysisRequest
from app.models.response_models import AnalysisResult
from app.services.pipeline import ImageProcessingPipeline
from app.utils.constants import DEFAULT_ANALYSIS_MODES
from app.utils.dependencies import get_pipeline

router = APIRouter()


@router.post("/full", response_model=AnalysisResult)
async def run_full_analysis(
    payload: AnalysisRequest,
    pipeline: ImageProcessingPipeline = Depends(get_pipeline),
) -> AnalysisResult:
    """Perform the configured analysis modes on an uploaded image."""
    modes = payload.modes or DEFAULT_ANALYSIS_MODES
    normalized_modes = list(dict.fromkeys(mode.lower() for mode in modes))
    return await pipeline.run(
        image_id=payload.image_id,
        modes=normalized_modes,
        refresh_cache=payload.refresh_cache,
    )
