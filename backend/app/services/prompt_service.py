"""Prompt orchestration services."""

from __future__ import annotations

from typing import List

from fastapi import HTTPException, status

from app.models.prompts_models import PlatformPrompt, PromptSection
from app.models.response_models import PromptGenerationResponse, PromptPayload
from app.repositories.interfaces import AnalysisRepository, PromptBundle, PromptRepository
from app.services.prompt_generator import PromptGeneratorFactory


class PromptOrchestrator:
    """Compose normalized prompts and generate platform-specific variants."""

    def __init__(
        self,
        analysis_repository: AnalysisRepository,
        prompt_repository: PromptRepository,
        factory: PromptGeneratorFactory,
    ) -> None:
        self._analysis_repository = analysis_repository
        self._prompt_repository = prompt_repository
        self._factory = factory

    def _build_normalized_prompt(self, image_id: str) -> PlatformPrompt:
        analysis = self._analysis_repository.get(image_id)
        if analysis is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No analysis found for image '{image_id}'.",
            )

        face = analysis.face
        context = analysis.context

        narrative_parts: List[str] = []
        if context and context.scene:
            narrative_parts.append(f"Scene: {', '.join(context.scene)}.")
        if context and context.lighting:
            narrative_parts.append(f"Lighting: {context.lighting}.")
        if face:
            narrative_parts.append("Primary subject faces camera with confident posture.")
        if not narrative_parts:
            narrative_parts.append("Well-lit portrait of the primary subject.")

        visual_cues: List[PromptSection] = []
        if face:
            if face.emotions:
                visual_cues.append(
                    PromptSection(
                        title="Emotions",
                        content=", ".join(face.emotions),
                        weight=0.9,
                    )
                )
            if face.accessories:
                visual_cues.append(
                    PromptSection(
                        title="Accessories",
                        content=", ".join(face.accessories),
                        weight=0.6,
                    )
                )

        if context and context.detected_objects:
            visual_cues.append(
                PromptSection(
                    title="Key Objects",
                    content=", ".join(context.detected_objects),
                    weight=0.7,
                )
            )

        lighting = context.lighting if context and context.lighting else "balanced soft light"
        style_tags = context.style_tags if context and context.style_tags else []
        environment = ", ".join(context.scene) if context and context.scene else "controlled studio"
        technical = {
            "camera": "35mm prime lens",
            "lighting": lighting,
            "aspect_ratio": "16:9",
        }
        if style_tags:
            technical["style_tags"] = ", ".join(style_tags)
        if face and face.embedding_id:
            technical["face_embedding_id"] = face.embedding_id
        if face and face.embedding_vector:
            technical["face_embedding_vector"] = face.embedding_vector

        persona = None
        if face and face.emotions:
            persona = f"Expresses {', '.join(face.emotions)}"

        motion = {
            "action": "Subject maintains gentle breathing and eye contact",
            "environment": environment,
            "duration": 10,
            "camera_type": "medium close-up",
            "camera_angle": "eye-level",
            "camera_movement": "slow dolly-in" if context and context.scene else "static hold",
            "composition": "Subject centered with balanced headroom",
            "style": "stylized" if style_tags else "realistic",
            "aesthetic": style_tags[0] if style_tags else "cinematic",
            "motion_type": "natural",
        }

        return PlatformPrompt(
            reference_id=image_id,
            narrative=" ".join(narrative_parts),
            persona=persona,
            visual_cues=visual_cues,
            technical=technical,
            motion=motion,
        )

    def generate_prompts(self, image_id: str, platforms: List[str]) -> PromptGenerationResponse:
        """Generate prompts for the requested platforms."""
        normalized = self._build_normalized_prompt(image_id)
        prompt_payloads: List[PromptPayload] = self._factory.build_prompts(normalized, platforms)
        bundle = PromptBundle(image_id=image_id, normalized=normalized, prompts=prompt_payloads)
        self._prompt_repository.save(bundle)
        return PromptGenerationResponse(image_id=image_id, prompts=prompt_payloads)

    def get_normalized_prompt(self, image_id: str) -> PlatformPrompt:
        """Return an existing normalized prompt or construct a new one on-demand."""
        bundle = self._prompt_repository.get(image_id)
        if bundle:
            return bundle.normalized
        return self._build_normalized_prompt(image_id)
