"""
==============================================================================
FILE: src/unihap/core/exceptions.py
MODULE: Custom Domain Exceptions
PURPOSE:
    Defines specialized exception hierarchy for each stage of the 12-layer
    pipeline to ensure clean error isolation and debuggability.

CLASSES:
    - UniHAPError: Base exception for all pipeline errors.
    - IngestError: Layer 0 ingestion and spreadsheet parsing failures.
    - EntityResolutionError: Layer 1 fuzzy matching or brand resolution issues.
    - ClassificationError: Layer 2 taxonomy classification failures.
    - DiscoveryError: Layer 4 manufacturer domain resolution errors.
    - ScrapingError: Layer 5 Crawl4AI web crawling or VLM extraction errors.
    - ExtractionError: Layer 6 constrained RAG extraction issues.
    - ValidationError: Layer 9 schema, LOV, or character limit validation errors.
==============================================================================
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
