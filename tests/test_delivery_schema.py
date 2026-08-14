"""
==============================================================================
FILE: tests/test_delivery_schema.py
MODULE: Delivery Format Schema Parity Test
PURPOSE:
    Validates that UniHAP's DELIVERY_HEADERS array matches the exact 252 columns
    and ordering of the Unihack Expected Output Delivery Format ground-truth CSV.
==============================================================================
"""

import csv
from pathlib import Path

from unihap.core.delivery_format import DELIVERY_HEADERS


def test_delivery_headers_count_and_parity():
    """Asserts that DeliveryFormatExporter has exactly 252 columns and matches ground truth."""
    assert len(DELIVERY_HEADERS) == 252, f"Expected 252 columns, found {len(DELIVERY_HEADERS)}"

    ground_truth_path = (
        Path(__file__).parent.parent / "data" / "ground_truth" / "unihack_expected_output_delivery_format.csv"
    )
    if ground_truth_path.exists():
        with open(ground_truth_path, mode="r", encoding="utf-8-sig", errors="replace") as f:
            reader = csv.reader(f)
            gt_headers = next(reader, [])
            assert len(gt_headers) == 252, f"Ground truth has {len(gt_headers)} columns, expected 252"
            assert DELIVERY_HEADERS == gt_headers, "DELIVERY_HEADERS does not match ground truth ordering"
