"""Anthropic Claude client wrapper with JSON extraction helpers."""

from __future__ import annotations

import asyncio
import json
from typing import Any, Dict, Iterable, List

from loguru import logger

from app.core.exceptions import ConfigurationError

try:
    from anthropic import Anthropic  # type: ignore
except ImportError:  # pragma: no cover - dependency is optional during tests
    Anthropic = None  # type: ignore[assignment]


CLAUDE_ANALYSIS_PROMPT = """You are a senior vision-language analyst helping a film prompt generation system.
Analyse the provided image and return STRICT JSON (no prose) matching this schema:
{
  "face": {
    "age_range": "string | null",
    "gender": "string | null",
    "emotions": ["string"],
    "accessories": ["string"]
  },
  "context": {
    "scene": ["string"],
    "lighting": "string | null",
    "style_tags": ["string"],
    "detected_objects": ["string"]
  },
  "confidence": 0.0-1.0 number indicating your certainty
}
Respect the requested analysis modes when deciding which sections to populate."""


class ClaudeVisionClient:
    """Thin wrapper around the Anthropic SDK for vision analysis."""

    def __init__(self, api_key: str | None, model: str, max_tokens: int) -> None:
        if not api_key:
            raise ConfigurationError("Claude Vision requires ANTHROPIC_API_KEY to be set.")
        if Anthropic is None:
            raise ConfigurationError("anthropic python package is required for Claude integration.")
        self._client = Anthropic(api_key=api_key)
        self._model = model
        self._max_tokens = max_tokens

    async def analyse(self, *, image_base64: str, media_type: str, modes: Iterable[str]) -> Dict[str, Any]:
        """Call Claude Vision to analyse the provided image."""
        payload = {
            "model": self._model,
            "max_tokens": self._max_tokens,
            "temperature": 0,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"{CLAUDE_ANALYSIS_PROMPT}\nRequested modes: {', '.join(modes)}.",
                        },
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": media_type or "image/png",
                                "data": image_base64,
                            },
                        },
                    ],
                }
            ],
        }

        try:
            response = await asyncio.to_thread(self._client.messages.create, **payload)
        except Exception as exc:  # pragma: no cover - network error path
            logger.exception("Claude analysis failed: %s", exc)
            raise

        text_blocks = [
            block.text
            for block in getattr(response, "content", [])
            if getattr(block, "type", "") == "text"
        ]
        raw = "".join(text_blocks).strip()

        if not raw:
            raise ValueError("Claude returned empty content.")
        try:
            data = json.loads(raw)
        except json.JSONDecodeError as exc:
            logger.exception("Claude response was not valid JSON: %s", raw)
            raise ValueError("Claude response parsing failed.") from exc
        return data
