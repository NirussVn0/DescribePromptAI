"""Image upload and management endpoints."""

from __future__ import annotations

import base64
import binascii
import uuid

from fastapi import APIRouter, Depends, HTTPException, status

from app.config import settings
from app.models.request_models import ImageUploadRequest
from app.repositories.interfaces import ImageRepository, StoredImage
from app.utils import validators
from app.utils.dependencies import get_image_repository

router = APIRouter()


@router.post("/upload")
async def upload_image(
    payload: ImageUploadRequest,
    repository: ImageRepository = Depends(get_image_repository),
) -> dict[str, str]:
    """Handle image upload metadata and return an identifier."""
    validators.ensure_file_extension(payload.filename)
    try:
        raw_bytes = base64.b64decode(payload.data_base64, validate=True)
    except (ValueError, binascii.Error) as exc:  # type: ignore[name-defined]
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid base64 payload.",
        ) from exc

    size_bytes = len(raw_bytes)
    if size_bytes > settings.max_file_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Uploaded image exceeds maximum allowed size.",
        )

    image_id = str(uuid.uuid4())
    repository.save(
        StoredImage(
            image_id=image_id,
            filename=payload.filename,
            content_type=payload.content_type,
            data_base64=payload.data_base64,
            size_bytes=size_bytes,
        )
    )
    return {"image_id": image_id, "size_bytes": size_bytes}
