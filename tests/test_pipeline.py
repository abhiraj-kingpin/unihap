from pathlib import Path
from unihap.pipeline import UniHAPPipeline
from unihap.core.models import StatusTag


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
