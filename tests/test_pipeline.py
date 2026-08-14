"""
==============================================================================
FILE: tests/test_pipeline.py
MODULE: Pipeline Smoke & Integration Test
PURPOSE:
    Tests basic pipeline execution on the sample catalog fixture.
==============================================================================
"""

from pathlib import Path

from unihap.pipeline import UniHAPPipeline


def test_pipeline_end_to_end():
    pipeline = UniHAPPipeline()
    sample_csv = Path(__file__).parent.parent / "data" / "raw" / "sample_catalog.csv"

    result = pipeline.run(sample_csv)
    assert result.total_processed == 4
    assert result.auto_approved_count > 0

    first = result.records[0]
    assert first.canonical_manufacturer == "Kohler"
    assert first.classification is not None
    assert first.classification.fine_category == "Kitchen Faucets"
    assert len(first.descriptions.invoice_caps) <= 40
    assert first.provenance_coverage_pct > 0.0
