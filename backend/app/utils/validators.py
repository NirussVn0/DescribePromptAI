"""Validation helpers for incoming requests."""

from __future__ import annotations

from fastapi import HTTPException, status

from app.config import settings


def ensure_file_extension(filename: str) -> None:
    """Ensure the provided filename uses an allowed extension."""
    allowed = {ext.lower() for ext in settings.allowed_formats}
    if "." not in filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename must include an extension.",
        )
    ext = filename.rsplit(".", 1)[-1].lower()
    if ext not in allowed:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Unsupported file type: {ext}",
        )
