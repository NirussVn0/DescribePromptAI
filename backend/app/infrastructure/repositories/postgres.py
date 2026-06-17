"""Postgres-backed repository implementations."""

from __future__ import annotations

from dataclasses import asdict
from typing import Optional

from loguru import logger
from sqlalchemy import JSON, Column, DateTime, MetaData, String, Table, create_engine, select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql import func

from app.models.prompts_models import PlatformPrompt, PromptSection
from app.models.response_models import AnalysisResult, PromptPayload
from app.repositories.interfaces import AnalysisRepository, PromptBundle, PromptRepository


def _create_engine(database_url: str) -> Engine:
    return create_engine(database_url, future=True, pool_pre_ping=True)


class PostgresAnalysisRepository(AnalysisRepository):
    """Persist analysis results in Postgres."""

    def __init__(self, database_url: str) -> None:
        self._engine = _create_engine(database_url)
        self._metadata = MetaData()
        self._table = Table(
            "image_analysis",
            self._metadata,
            Column("image_id", String, primary_key=True),
            Column("payload", JSON, nullable=False),
            Column("updated_at", DateTime(timezone=True), server_default=func.now(), onupdate=func.now()),
        )
        self._metadata.create_all(self._engine)

    def save(self, result: AnalysisResult) -> None:
        payload = result.dict()
        statement = pg_insert(self._table).values(image_id=result.image_id, payload=payload)
        statement = statement.on_conflict_do_update(
            index_elements=[self._table.c.image_id],
            set_={"payload": statement.excluded.payload, "updated_at": func.now()},
        )
        try:
            with self._engine.begin() as connection:
                connection.execute(statement)
        except SQLAlchemyError as exc:  # pragma: no cover - database failure path
            logger.exception("Failed to persist analysis: %s", exc)
            raise

    def get(self, image_id: str) -> Optional[AnalysisResult]:
        statement = select(self._table.c.payload).where(self._table.c.image_id == image_id)
        try:
            with self._engine.begin() as connection:
                row = connection.execute(statement).first()
        except SQLAlchemyError as exc:  # pragma: no cover - database failure path
            logger.exception("Failed to fetch analysis: %s", exc)
            raise
        if not row:
            return None
        return AnalysisResult.parse_obj(row.payload)


class PostgresPromptRepository(PromptRepository):
    """Persist generated prompts in Postgres."""

    def __init__(self, database_url: str) -> None:
        self._engine = _create_engine(database_url)
        self._metadata = MetaData()
        self._table = Table(
            "prompt_history",
            self._metadata,
            Column("image_id", String, primary_key=True),
            Column("normalized", JSON, nullable=False),
            Column("prompts", JSON, nullable=False),
            Column("updated_at", DateTime(timezone=True), server_default=func.now(), onupdate=func.now()),
        )
        self._metadata.create_all(self._engine)

    def save(self, bundle: PromptBundle) -> None:
        normalized = asdict(bundle.normalized)
        prompts = [prompt.dict() for prompt in bundle.prompts]
        statement = pg_insert(self._table).values(
            image_id=bundle.image_id,
            normalized=normalized,
            prompts=prompts,
        )
        statement = statement.on_conflict_do_update(
            index_elements=[self._table.c.image_id],
            set_={
                "normalized": statement.excluded.normalized,
                "prompts": statement.excluded.prompts,
                "updated_at": func.now(),
            },
        )
        try:
            with self._engine.begin() as connection:
                connection.execute(statement)
        except SQLAlchemyError as exc:  # pragma: no cover - database failure path
            logger.exception("Failed to persist prompt bundle: %s", exc)
            raise

    def get(self, image_id: str) -> Optional[PromptBundle]:
        statement = select(self._table.c.normalized, self._table.c.prompts).where(self._table.c.image_id == image_id)
        try:
            with self._engine.begin() as connection:
                row = connection.execute(statement).first()
        except SQLAlchemyError as exc:  # pragma: no cover - database failure path
            logger.exception("Failed to fetch prompt bundle: %s", exc)
            raise
        if not row:
            return None

        normalized_data = row.normalized
        prompts_data = row.prompts

        visual_cues = [PromptSection(**section) for section in normalized_data.get("visual_cues", [])]
        normalized = PlatformPrompt(
            reference_id=normalized_data["reference_id"],
            narrative=normalized_data["narrative"],
            persona=normalized_data.get("persona"),
            visual_cues=visual_cues,
            technical=normalized_data.get("technical", {}),
            motion=normalized_data.get("motion", {}),
        )
        prompts = [PromptPayload.parse_obj(item) for item in prompts_data]
        return PromptBundle(image_id=image_id, normalized=normalized, prompts=prompts)
