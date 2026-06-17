"""Unit tests for prompt generation factory."""

from __future__ import annotations

from app.models.prompts_models import PlatformPrompt, PromptSection
from app.services.prompt_generator import PromptGeneratorFactory


def _sample_prompt() -> PlatformPrompt:
    return PlatformPrompt(
        reference_id="img-123",
        narrative="Scene: indoor studio. Lighting: soft key lighting.",
        persona="Expresses calm confidence",
        visual_cues=[
            PromptSection(title="Emotions", content="confident"),
            PromptSection(title="Key Objects", content="camera, tripod"),
        ],
        technical={
            "camera": "35mm prime lens",
            "lighting": "soft key lighting",
            "aspect_ratio": "16:9",
            "face_embedding_id": "img-123-embedding",
            "face_embedding_vector": [0.1] * 512,
            "style_tags": "cinematic",
        },
        motion={
            "duration": 10,
            "camera_type": "medium close-up",
            "camera_angle": "eye-level",
            "camera_movement": "static hold",
            "action": "Subject maintains gentle smile",
            "environment": "indoor studio",
            "aesthetic": "cinematic",
        },
    )


def test_prompt_factory_builds_all_platforms() -> None:
    prompt = _sample_prompt()
    platforms = ["sora", "runway", "pika", "luma"]
    payloads = PromptGeneratorFactory.build_prompts(prompt, platforms)
    assert {payload.platform for payload in payloads} == set(platforms)

    runway_payload = next(item for item in payloads if item.platform == "runway")
    assert runway_payload.prompt["identity_control"]["preserve_likeness"] is True
    assert len(runway_payload.prompt["identity_control"]["face_embedding"]) == 512

    sora_payload = next(item for item in payloads if item.platform == "sora")
    assert "world_state" in sora_payload.prompt

    metadata = runway_payload.metadata
    assert metadata["face_embedding_id"] == "img-123-embedding"
