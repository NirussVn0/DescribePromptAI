"""End-to-end smoke tests for FastAPI application."""

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_end_to_end_pipeline() -> None:
    upload_response = client.post(
        "/images/upload",
        json={
            "filename": "portrait.png",
            "content_type": "image/png",
            "data_base64": "dGVzdA==",
        },
    )
    assert upload_response.status_code == 200
    payload = upload_response.json()
    image_id = payload["image_id"]

    analysis_response = client.post(
        "/analysis/full",
        json={"image_id": image_id, "modes": ["face", "context"]},
    )
    assert analysis_response.status_code == 200
    analysis_payload = analysis_response.json()
    assert analysis_payload["image_id"] == image_id
    assert analysis_payload["face"]["embedding_id"].endswith("-embedding")
    assert len(analysis_payload["face"]["embedding_vector"]) == 512
    assert analysis_payload["context"]["scene"]

    prompt_response = client.post(
        "/prompts/generate",
        json={"image_id": image_id, "target_platforms": ["sora", "runway"]},
    )
    assert prompt_response.status_code == 200
    prompt_payload = prompt_response.json()
    assert len(prompt_payload["prompts"]) == 2
    for platform_payload in prompt_payload["prompts"]:
        assert platform_payload["metadata"]["reference_id"] == image_id
        if platform_payload["platform"] == "runway":
            assert platform_payload["prompt"]["identity_control"]["preserve_likeness"] is True
            assert len(platform_payload["prompt"]["identity_control"]["face_embedding"]) == 512

    video_response = client.post(
        "/video/extend",
        json={
            "image_id": image_id,
            "motion_description": "Camera pans slowly around the subject.",
            "duration_seconds": 8,
        },
    )
    assert video_response.status_code == 200
    video_payload = video_response.json()
    assert video_payload["duration_seconds"] == 8
    assert video_payload["video_prompt"]["reference_id"] == image_id
