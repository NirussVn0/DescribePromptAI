"""Face detection and embedding extraction services."""

from __future__ import annotations

import asyncio
import base64
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List

from loguru import logger


try:  # Optional heavy dependencies
    import numpy as np  # type: ignore
except ImportError:  # pragma: no cover - optional dependency
    np = None  # type: ignore

try:
    import cv2  # type: ignore
except ImportError:  # pragma: no cover - optional dependency
    cv2 = None  # type: ignore

try:
    from insightface.app import FaceAnalysis  # type: ignore
except ImportError:  # pragma: no cover - optional dependency
    FaceAnalysis = None  # type: ignore

try:
    import redis  # type: ignore
except ImportError:  # pragma: no cover - optional dependency
    redis = None  # type: ignore


@dataclass(slots=True)
class FaceEmbedding:
    """Represents a stored face embedding result."""

    embedding_id: str
    vector: List[float]


class FaceDetectorService:
    """Interface to a face detection and embedding backend."""

    def __init__(
        self,
        *,
        model_name: str = "antelopev2",
        model_root: str | None = None,
        cache_ttl: int = 86_400,
        redis_client: "redis.Redis" | None = None,
    ) -> None:
        self._cache_ttl = cache_ttl
        self._redis = redis_client
        self._store: Dict[str, FaceEmbedding] = {}
        self._analyzer = self._prepare_analyzer(model_name=model_name, model_root=model_root)

    async def extract_embedding(self, image_id: str, image_data: str) -> FaceEmbedding:
        """Extract and cache a face embedding for the provided image."""
        cache_key = self._cache_key(image_id)
        cached = self._try_load_from_cache(cache_key)
        if cached:
            return cached

        if embedding := self._store.get(cache_key):
            return embedding

        raw_bytes = self._decode_image(image_data)
        vector = await self._compute_embedding(raw_bytes)

        embedding = FaceEmbedding(embedding_id=f"{image_id}-embedding", vector=vector)
        self._store[cache_key] = embedding
        self._persist(cache_key, embedding)
        return embedding

    async def get_embedding(self, embedding_id: str) -> FaceEmbedding | None:
        """Retrieve a cached embedding if available."""
        cache_key = self._cache_key(embedding_id.replace("-embedding", ""))
        if cached := self._try_load_from_cache(cache_key):
            return cached
        return self._store.get(cache_key)

    def _prepare_analyzer(self, *, model_name: str, model_root: str | None) -> FaceAnalysis | None:
        if FaceAnalysis is None or np is None or cv2 is None:
            logger.warning("InsightFace dependency not available; using deterministic embedding fallback.")
            return None
        if not model_root:
            logger.warning("INSIGHTFACE_MODEL_DIR not configured; skipping InsightFace initialization.")
            return None
        root_path = Path(model_root)
        if not root_path.exists():
            logger.warning("InsightFace model directory '%s' does not exist.", model_root)
            return None
        try:
            analyzer = FaceAnalysis(name=model_name, root=model_root)
            analyzer.prepare(ctx_id=-1, det_size=(640, 640))
            return analyzer
        except Exception as exc:  # pragma: no cover - runtime setup failure
            logger.exception("Failed to prepare InsightFace: %s", exc)
            return None

    async def _compute_embedding(self, raw_bytes: bytes) -> List[float]:
        if self._analyzer is None:
            return self._fallback_embedding(raw_bytes)

        def _run() -> List[float]:
            array = np.frombuffer(raw_bytes, dtype=np.uint8)
            image = cv2.imdecode(array, cv2.IMREAD_COLOR)
            if image is None:
                return self._fallback_embedding(raw_bytes)
            faces = self._analyzer.get(image)  # type: ignore[operator]
            if not faces:
                return self._fallback_embedding(raw_bytes)
            embedding = faces[0].normed_embedding.astype(float).tolist()
            if len(embedding) != 512:
                return self._fallback_embedding(raw_bytes)
            return embedding

        return await asyncio.to_thread(_run)

    @staticmethod
    def _fallback_embedding(raw_bytes: bytes) -> List[float]:
        digest = hashlib.sha256(raw_bytes).digest()
        values: List[float] = []
        seed = digest
        while len(values) < 512:
            for chunk_start in range(0, len(seed), 4):
                chunk = seed[chunk_start : chunk_start + 4]
                if len(chunk) < 4:
                    continue
                integer = int.from_bytes(chunk, "little")
                values.append((integer % 10_000) / 10_000.0)
                if len(values) == 512:
                    break
            seed = hashlib.sha256(seed).digest()
        return values

    @staticmethod
    def _decode_image(image_data: str) -> bytes:
        return base64.b64decode(image_data, validate=True)

    def _persist(self, cache_key: str, embedding: FaceEmbedding) -> None:
        if not self._redis:
            return
        try:
            self._redis.set(cache_key, json.dumps(embedding.__dict__), ex=self._cache_ttl)
        except Exception as exc:  # pragma: no cover - Redis failure path
            logger.warning("Failed to persist embedding to Redis: %s", exc)

    def _try_load_from_cache(self, cache_key: str) -> FaceEmbedding | None:
        if not self._redis:
            return None
        try:
            payload = self._redis.get(cache_key)
        except Exception as exc:  # pragma: no cover - Redis failure path
            logger.warning("Failed to read embedding cache: %s", exc)
            return None
        if not payload:
            return None
        try:
            data = json.loads(payload)
            return FaceEmbedding(embedding_id=data["embedding_id"], vector=list(map(float, data["vector"])))
        except Exception as exc:  # pragma: no cover - corrupt cache
            logger.warning("Invalid embedding cache payload: %s", exc)
            return None

    @staticmethod
    def _cache_key(image_id: str) -> str:
        return f"face-embedding:{image_id}"
