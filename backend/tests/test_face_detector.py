"""Tests for face detector service fallback behaviour."""

from __future__ import annotations

import base64

import pytest

from app.services.face_detector import FaceDetectorService


@pytest.mark.asyncio
async def test_face_detector_generates_deterministic_embedding() -> None:
    service = FaceDetectorService(model_root=None)
    image_id = "test-image"
    image_data = base64.b64encode(b"fake-image-bytes").decode()

    embedding = await service.extract_embedding(image_id=image_id, image_data=image_data)

    assert embedding.embedding_id == f"{image_id}-embedding"
    assert len(embedding.vector) == 512
    assert embedding.vector == (await service.extract_embedding(image_id=image_id, image_data=image_data)).vector
