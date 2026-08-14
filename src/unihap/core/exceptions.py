"""
Custom exceptions for UniHAP pipeline.
"""

class UniHAPError(Exception):
    """Base exception for UniHAP pipeline errors."""
    pass


class IngestError(UniHAPError):
    """Raised when XLSX or CSV ingestion fails."""
    pass


class EntityResolutionError(UniHAPError):
    """Raised when fuzzy or embedding matching fails."""
    pass


class ClassificationError(UniHAPError):
    """Raised when classpath classification fails."""
    pass


class DiscoveryError(UniHAPError):
    """Raised when manufacturer domain discovery fails."""
    pass


class ScrapingError(UniHAPError):
    """Raised when Crawl4AI document scraping fails."""
    pass


class ExtractionError(UniHAPError):
    """Raised when LLM attribute extraction fails or hallucinates without evidence."""
    pass


class ValidationError(UniHAPError):
    """Raised when validation schema or LOV bounds are violated."""
    pass
