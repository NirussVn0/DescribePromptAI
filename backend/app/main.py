"""FastAPI application bootstrap for DescribePromptAI."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.core.errors import register_exception_handlers
from app.routers import analysis, images, prompts, video
from app.utils.logger import configure_logging


def create_app() -> FastAPI:
    """Create and configure the FastAPI application instance."""
    configure_logging()

    app = FastAPI(
        title="DescribePromptAI",
        description="Multimodal prompt generation service for image-to-video workflows.",
        version="0.1.0",
    )

    register_exception_handlers(app)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(images.router, prefix="/images", tags=["Images"])
    app.include_router(analysis.router, prefix="/analysis", tags=["Analysis"])
    app.include_router(prompts.router, prefix="/prompts", tags=["Prompts"])
    app.include_router(video.router, prefix="/video", tags=["Video"])
    return app


app = create_app()
