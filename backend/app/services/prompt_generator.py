"""Prompt generation factory for multi-platform support."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Type

from app.core.exceptions import PromptGenerationError
from app.models.prompts_models import PlatformPrompt
from app.models.response_models import PromptPayload


def _cue(prompt: PlatformPrompt, title: str, default: str = "") -> str:
    for section in prompt.visual_cues:
        if section.title.lower() == title.lower() and section.content:
            return section.content
    return default


class PromptGenerator(ABC):
    """Abstract base for platform-specific prompt generators."""

    platform: str

    @abstractmethod
    def build_prompt(self, prompt: PlatformPrompt) -> PromptPayload:
        """Transform a normalized prompt into platform-specific output."""

    def _base_metadata(self, prompt: PlatformPrompt) -> Dict[str, Any]:
        metadata: Dict[str, Any] = {
            "reference_id": prompt.reference_id,
            "aspect_ratio": prompt.technical.get("aspect_ratio"),
            "lighting": prompt.technical.get("lighting"),
        }
        face_id = prompt.technical.get("face_embedding_id")
        if face_id:
            metadata["face_embedding_id"] = face_id
        face_vector = prompt.technical.get("face_embedding_vector")
        if face_vector:
            metadata["face_embedding_vector"] = face_vector
        style_tags = prompt.technical.get("style_tags")
        if style_tags:
            metadata["style_tags"] = style_tags
        return {key: value for key, value in metadata.items() if value}


class SoraPromptGenerator(PromptGenerator):
    platform = "sora"

    def build_prompt(self, prompt: PlatformPrompt) -> PromptPayload:
        visual_summary = ", ".join(section.content for section in prompt.visual_cues if section.content)
        data = {
            "subject": prompt.persona or "Primary character from reference image",
            "action": prompt.motion.get("action", "Maintains subtle breathing and micro movements"),
            "environment": prompt.motion.get("environment", visual_summary or "Controlled studio environment"),
            "cinematic": {
                "camera": prompt.technical.get("camera", "35mm prime lens"),
                "composition": prompt.motion.get("composition", "Centered portrait"),
            },
            "aesthetic": prompt.motion.get("aesthetic", prompt.technical.get("style_tags", "cinematic realism")),
            "world_state": {
                "physics": "Real-world gravity and lighting continuity",
                "initial_conditions": prompt.motion.get("initial_conditions", "Start from captured pose"),
            },
        }
        return PromptPayload(platform=self.platform, prompt=data, metadata=self._base_metadata(prompt) | {"temperature": 0.15})


class RunwayPromptGenerator(PromptGenerator):
    platform = "runway"

    def build_prompt(self, prompt: PlatformPrompt) -> PromptPayload:
        data = {
            "prompt": prompt.narrative,
            "camera": {
                "type": prompt.motion.get("camera_type", "medium shot"),
                "angle": prompt.motion.get("camera_angle", "eye-level"),
                "movement": prompt.motion.get("camera_movement", "static hold"),
            },
            "identity_control": {
                "mode": "embedding_conditioning",
                "face_embedding": prompt.technical.get("face_embedding_vector")
                or prompt.technical.get("face_embedding_id"),
                "preserve_likeness": True,
            },
            "duration": int(prompt.motion.get("duration", 10)),
        }
        return PromptPayload(platform=self.platform, prompt=data, metadata=self._base_metadata(prompt))


class PikaPromptGenerator(PromptGenerator):
    platform = "pika"

    def build_prompt(self, prompt: PlatformPrompt) -> PromptPayload:
        data = {
            "prompt": prompt.narrative,
            "style": prompt.motion.get("style", "stylized"),
            "aesthetic": prompt.motion.get("aesthetic", "cinematic"),
            "platform_optimized": "social_media",
            "duration": int(prompt.motion.get("duration", 8)),
        }
        metadata = self._base_metadata(prompt)
        metadata.update({"fps": prompt.technical.get("fps", 24)})
        return PromptPayload(platform=self.platform, prompt=data, metadata=metadata)


class LumaPromptGenerator(PromptGenerator):
    platform = "luma"

    def build_prompt(self, prompt: PlatformPrompt) -> PromptPayload:
        data = {
            "prompt": prompt.narrative,
            "motion_type": prompt.motion.get("motion_type", "natural"),
            "physics_aware": True,
            "duration": int(prompt.motion.get("duration", 10)),
        }
        metadata = self._base_metadata(prompt)
        metadata.setdefault("lighting", prompt.technical.get("lighting", "soft key lighting"))
        metadata.setdefault("environment", _cue(prompt, "Key Objects", "studio backdrop"))
        return PromptPayload(platform=self.platform, prompt=data, metadata=metadata)


class PromptGeneratorFactory:
    """Factory responsible for resolving prompt generator implementations."""

    _registry: Dict[str, Type[PromptGenerator]] = {
        SoraPromptGenerator.platform: SoraPromptGenerator,
        RunwayPromptGenerator.platform: RunwayPromptGenerator,
        PikaPromptGenerator.platform: PikaPromptGenerator,
        LumaPromptGenerator.platform: LumaPromptGenerator,
    }

    @classmethod
    def create(cls, platform: str) -> PromptGenerator:
        """Return a prompt generator for the requested platform."""
        try:
            generator_cls = cls._registry[platform.lower()]
        except KeyError as exc:
            raise PromptGenerationError(f"Unsupported platform '{platform}'") from exc
        return generator_cls()

    @classmethod
    def build_prompts(cls, normalized_prompt: PlatformPrompt, platforms: List[str]) -> List[PromptPayload]:
        """Generate prompts for the provided platform list."""
        results: List[PromptPayload] = []
        for platform in platforms:
            generator = cls.create(platform)
            results.append(generator.build_prompt(normalized_prompt))
        return results
