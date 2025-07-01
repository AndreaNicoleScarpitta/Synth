class TransientError(Exception):
    """Raised for retryable failures (network issues, rate limits)."""

class FatalError(Exception):
    """Raised for non-retryable failures (invalid input, internal bugs)."""
