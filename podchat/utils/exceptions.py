"""Custom exceptions for PodChat."""


class PodChatError(Exception):
    """Base exception for all PodChat errors."""
    pass


# Input/Validation Errors
class ValidationError(PodChatError):
    """Base class for validation errors."""
    pass


class InvalidURLError(ValidationError):
    """Invalid YouTube URL provided."""
    pass


class InvalidArgumentError(ValidationError):
    """Invalid command-line argument."""
    pass


# Transcript Errors
class TranscriptError(PodChatError):
    """Base class for transcript-related errors."""
    pass


class TranscriptNotAvailableError(TranscriptError):
    """Transcript not available for video."""
    pass


class TranscriptExtractionError(TranscriptError):
    """Failed to extract transcript."""
    pass


# LLM Errors
class LLMError(PodChatError):
    """Base class for LLM-related errors."""
    pass


class LLMAPIError(LLMError):
    """LLM API call failed."""
    pass


class TokenLimitError(LLMError):
    """Content exceeds token limit."""
    pass


class RateLimitError(LLMError):
    """API rate limit exceeded."""
    pass


# Output Errors
class OutputError(PodChatError):
    """Base class for output-related errors."""
    pass


class FormattingError(OutputError):
    """Failed to format output."""
    pass


class FileWriteError(OutputError):
    """Failed to write output file."""
    pass


# Network Errors
class NetworkError(PodChatError):
    """Network-related errors."""
    pass


# Configuration Errors
class ConfigurationError(PodChatError):
    """Configuration-related errors."""
    pass
