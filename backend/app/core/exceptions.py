"""Domain-specific exception hierarchy."""

from __future__ import annotations


class DescribePromptAIError(Exception):
    """Base application error."""


class ValidationError(DescribePromptAIError):
    """Raised when user input fails validation."""


class AnalysisError(DescribePromptAIError):
    """Raised when image analysis fails."""


class PromptGenerationError(DescribePromptAIError):
    """Raised when prompt synthesis encounters an unrecoverable error."""


class NotFoundError(DescribePromptAIError):
    """Raised when a requested resource cannot be found."""


class ConfigurationError(DescribePromptAIError):
    """Raised when required configuration is missing."""
