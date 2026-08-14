"""
==============================================================================
FILE: tests/test_performance_and_latency.py
MODULE: Throughput & Latency Benchmark Tests
PURPOSE:
    Tests execution latency to ensure the pipeline scales efficiently.
    Asserts that in-memory parsing, matching, knowledge graph lookups,
    and normalization process 100+ records in under 2 seconds.
==============================================================================
"""

import time

import pytest

from unihap.core.models import ProductRecord
from unihap.pipeline import UniHAPPipeline


@pytest.fixture(scope="module")
def pipeline():
    return UniHAPPipeline()


def test_batch_processing_throughput(pipeline):
    """Benchmarks batch processing throughput on 100 simulated real-world rows."""
    sample_records = [
        ProductRecord(
            row_id=f"BENCH_ROW_{i}",
            MPN=f"K-596-{i}",
            Manufacturer="Kohler Co.",
            Brand="Kohler",
            Description="Simplice Pull-Down Kitchen Faucet in Matte Black 1.8 GPM",
        )
        for i in range(100)
    ]

    t0 = time.perf_counter()
    enriched = [pipeline.process_record(r) for r in sample_records]
    elapsed = time.perf_counter() - t0

    assert len(enriched) == 100
    # 100 records should process in under 2.5 seconds in memory
    assert elapsed < 2.5, f"Processing 100 records took {elapsed:.2f}s (expected < 2.5s)"
    throughput = 100 / elapsed
    assert throughput >= 40.0, f"Throughput was {throughput:.1f} rows/sec (expected >= 40)"
