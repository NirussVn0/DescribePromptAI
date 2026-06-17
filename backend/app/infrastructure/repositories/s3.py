"""S3-backed image repository implementation."""

from __future__ import annotations

import json
from dataclasses import asdict
from typing import Optional

from loguru import logger

from app.repositories.interfaces import ImageRepository, StoredImage

try:
    import boto3  # type: ignore
except ImportError:  # pragma: no cover - optional dependency
    boto3 = None  # type: ignore


class S3ImageRepository(ImageRepository):
    """Persist images to S3 for durable storage."""

    def __init__(
        self,
        *,
        bucket: str,
        region: str | None,
        access_key: str | None,
        secret_key: str | None,
    ) -> None:
        if boto3 is None:
            raise RuntimeError("boto3 is required for S3 storage.")
        session = boto3.session.Session(
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            region_name=region,
        )
        self._client = session.client("s3")
        self._bucket = bucket

    def save(self, record: StoredImage) -> None:
        payload = asdict(record)
        body = json.dumps(payload).encode("utf-8")
        try:
            self._client.put_object(
                Bucket=self._bucket,
                Key=self._object_key(record.image_id),
                Body=body,
                ContentType="application/json",
            )
        except Exception as exc:  # pragma: no cover - S3 failure path
            logger.exception("Failed to upload image %s: %s", record.image_id, exc)
            raise

    def get(self, image_id: str) -> Optional[StoredImage]:
        try:
            response = self._client.get_object(Bucket=self._bucket, Key=self._object_key(image_id))
        except self._client.exceptions.NoSuchKey:  # type: ignore[attr-defined]
            return None
        except Exception as exc:  # pragma: no cover - S3 failure path
            logger.exception("Failed to fetch image %s: %s", image_id, exc)
            raise

        body = response["Body"].read()
        data = json.loads(body)
        return StoredImage(**data)

    @staticmethod
    def _object_key(image_id: str) -> str:
        return f"images/{image_id}.json"
