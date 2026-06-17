"""Exception handler registration for FastAPI."""

from __future__ import annotations

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.core.exceptions import ConfigurationError, AnalysisError, DescribePromptAIError, NotFoundError, PromptGenerationError, ValidationError


def _error_response(message: str, error_type: str, http_status: int, details: dict | None = None) -> JSONResponse:
    payload = {"error": error_type, "detail": message}
    if details:
        payload["details"] = details
    return JSONResponse(status_code=http_status, content=payload)


def register_exception_handlers(app: FastAPI) -> None:
    """Attach exception handlers for domain-specific errors."""

    @app.exception_handler(ValidationError)
    async def handle_validation_error(_: Request, exc: ValidationError) -> JSONResponse:
        return _error_response(str(exc), "validation_error", status.HTTP_422_UNPROCESSABLE_ENTITY)

    @app.exception_handler(NotFoundError)
    async def handle_not_found(_: Request, exc: NotFoundError) -> JSONResponse:
        return _error_response(str(exc), "not_found", status.HTTP_404_NOT_FOUND)

    @app.exception_handler(AnalysisError)
    async def handle_analysis_error(_: Request, exc: AnalysisError) -> JSONResponse:
        return _error_response(str(exc), "analysis_error", status.HTTP_500_INTERNAL_SERVER_ERROR)

    @app.exception_handler(PromptGenerationError)
    async def handle_prompt_error(_: Request, exc: PromptGenerationError) -> JSONResponse:
        return _error_response(str(exc), "prompt_error", status.HTTP_500_INTERNAL_SERVER_ERROR)

    @app.exception_handler(DescribePromptAIError)
    async def handle_generic(_: Request, exc: DescribePromptAIError) -> JSONResponse:
        return _error_response(str(exc), "application_error", status.HTTP_400_BAD_REQUEST)

    @app.exception_handler(ConfigurationError)
    async def handle_configuration(_: Request, exc: ConfigurationError) -> JSONResponse:
        return _error_response(str(exc), "configuration_error", status.HTTP_503_SERVICE_UNAVAILABLE)
