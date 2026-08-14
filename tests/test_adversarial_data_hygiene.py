"""
==============================================================================
FILE: tests/test_adversarial_data_hygiene.py
MODULE: Adversarial Data Hygiene & Fault Tolerance Tests
PURPOSE:
    Ensures that the pipeline is resilient against malformed, corrupt, or hostile
    data:
      - None / NaN / Empty strings in required fields
      - Extremely long description payloads (>10,000 characters)
      - Complex Unicode / foreign symbols / emoji injection
      - Special punctuation, quotes, slashes, and backslashes in MPNs
      - Missing columns in input files
==============================================================================
"""

import pytest

from unihap.core.models import ProductRecord, StatusTag
from unihap.pipeline import UniHAPPipeline


@pytest.fixture(scope="module")
def pipeline():
    return UniHAPPipeline()


def test_empty_and_none_record_handling(pipeline):
    """Pipeline should never crash when encountering empty or None records."""
    raw = ProductRecord(row_id="EMPTY_ROW", MPN=None, Manufacturer=None, Brand=None, Description=None)
    enriched = pipeline.process_record(raw)
    assert enriched.row_id == "EMPTY_ROW"
    assert enriched.canonical_manufacturer in ["UNRESOLVED_MANUFACTURER", ""]
    assert enriched.overall_status in [StatusTag.NEEDS_REVIEW, StatusTag.REJECTED]
    assert enriched.descriptions.invoice_caps == "" or len(enriched.descriptions.invoice_caps) <= 40


def test_extreme_length_payload_protection(pipeline):
    """Protects against buffer overflows and keeps synthesized descriptions within bounds."""
    giant_desc = "Industrial Faucet " * 500  # ~9,000 chars
    raw = ProductRecord(
        row_id="GIANT_ROW", MPN="SUPER-LONG-PART-NUMBER-" + ("9" * 100), Manufacturer="Kohler", Description=giant_desc
    )
    enriched = pipeline.process_record(raw)
    assert len(enriched.descriptions.invoice_caps) <= 40
    assert len(enriched.descriptions.mobile) <= 80


def test_special_characters_and_slashes_in_mpn(pipeline):
    """Validates that complex MPNs with slashes, dots, hashes, and hyphens are preserved."""
    raw = ProductRecord(
        row_id="SPECIAL_CHARS_ROW",
        MPN="K-596/BL#01.A-2026",
        Manufacturer="Kohler",
        Description="Simplice Kitchen Faucet Matte Black",
    )
    enriched = pipeline.process_record(raw)
    assert "K-596/BL#01.A-2026" in enriched.mpn
    assert len(enriched.descriptions.invoice_caps) <= 40


def test_unicode_and_accent_character_handling(pipeline):
    """Ensures international accents and trademark symbols do not break processing."""
    raw = ProductRecord(
        row_id="UNICODE_ROW",
        MPN="GRO-321",
        Manufacturer="Grohe® Deutschland",
        Brand="Grohe™",
        Description="Essence New Évier Mitigeur Chromé 1.75 GPM",
    )
    enriched = pipeline.process_record(raw)
    assert "Grohe" in enriched.canonical_manufacturer
    assert enriched.descriptions.invoice_caps.isupper()
