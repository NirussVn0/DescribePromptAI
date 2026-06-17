"""Internal domain models describing prompt structures."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass(slots=True)
class PromptSection:
    """Represents a discrete section of a prompt."""

    title: str
    content: str
    weight: float = 1.0


@dataclass(slots=True)
class PlatformPrompt:
    """Normalized platform prompt representation."""

    reference_id: str
    narrative: str
    persona: str | None = None
    visual_cues: List[PromptSection] = field(default_factory=list)
    technical: Dict[str, Any] = field(default_factory=dict)
    motion: Dict[str, Any] = field(default_factory=dict)
