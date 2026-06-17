"""Security utilities and helpers."""

from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict

import jwt

from app.config import settings


class TokenService:
    """Simple JWT service placeholder to support future auth integration."""

    def __init__(self, secret_key: str | None = None, algorithm: str = "HS256") -> None:
        self._secret_key = secret_key or settings.aws_secret_access_key or "changeme"
        self._algorithm = algorithm

    def create_access_token(self, subject: str, expires_delta: timedelta | None = None) -> str:
        """Generate a signed JWT for the provided subject."""
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=30))
        payload: Dict[str, Any] = {"sub": subject, "exp": expire}
        return jwt.encode(payload, self._secret_key, algorithm=self._algorithm)

    def decode_token(self, token: str) -> Dict[str, Any]:
        """Decode an incoming JWT and return its payload."""
        return jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
