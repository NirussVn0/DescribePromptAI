"""Processing pipeline orchestrating image analysis steps."""

from __future__ import annotations

from typing import List, Optional

from app.core.exceptions import AnalysisError, NotFoundError
from app.models.response_models import AnalysisResult, ContextAttributes, FaceAttributes
from app.repositories.interfaces import AnalysisRepository, ImageRepository, StoredImage
from app.services.context_analyzer import ContextAnalyzerService
from app.services.face_detector import FaceDetectorService
from app.services.image_analyzer import ImageAnalyzerService


class ImageProcessingPipeline:
    """Pipeline orchestrating validation, analysis, and persistence."""

    def __init__(
        self,
        image_repository: ImageRepository,
        analysis_repository: AnalysisRepository,
        analyzer: ImageAnalyzerService,
        face_detector: FaceDetectorService,
        context_analyzer: ContextAnalyzerService,
    ) -> None:
        self._image_repository = image_repository
        self._analysis_repository = analysis_repository
        self._analyzer = analyzer
        self._face_detector = face_detector
        self._context_analyzer = context_analyzer

    def _load_image(self, image_id: str) -> StoredImage:
        record = self._image_repository.get(image_id)
        if record is None:
            raise NotFoundError(f"Image '{image_id}' was not found.")
        return record

    def get_cached(self, image_id: str) -> Optional[AnalysisResult]:
        """Return a cached analysis result when available."""
        return self._analysis_repository.get(image_id)

    async def run(self, image_id: str, modes: List[str], refresh_cache: bool = False) -> AnalysisResult:
        """Execute the analysis pipeline for the provided image."""
        if not refresh_cache:
            cached = self.get_cached(image_id)
            if cached:
                return cached

        image_record = self._load_image(image_id)
        try:
            base_result = await self._analyzer.analyze(image_record, modes)
        except Exception as exc:
            raise AnalysisError(f"Analysis failed: {exc}") from exc

        face_attrs: FaceAttributes | None = base_result.face
        if "face" in modes:
            embedding = await self._face_detector.extract_embedding(
                image_id=image_id,
                image_data=image_record.data_base64,
            )
            face_attrs = FaceAttributes(
                embedding_id=embedding.embedding_id,
                embedding_vector=embedding.vector,
                age_range=face_attrs.age_range if face_attrs else None,
                gender=face_attrs.gender if face_attrs else None,
                emotions=face_attrs.emotions if face_attrs else [],
                accessories=face_attrs.accessories if face_attrs else [],
            )
        else:
            face_attrs = None

        context_attrs: ContextAttributes | None = base_result.context
        if "context" in modes:
            descriptor = await self._context_analyzer.analyze(
                image_id=image_id,
                image_data=image_record.data_base64,
            )
            context_attrs = ContextAttributes(
                scene=descriptor.scene,
                lighting=descriptor.lighting,
                style_tags=descriptor.style_tags or [],
                detected_objects=descriptor.detected_objects or [],
            )
        else:
            context_attrs = None

        result = AnalysisResult(
            image_id=image_id,
            face=face_attrs,
            context=context_attrs,
            confidence=base_result.confidence,
        )
        self._analysis_repository.save(result)
        return result
