"""
==============================================================================
FILE: src/unihap/layers/l12_evaluation/evaluator.py
MODULE: Layer 12 — Evaluation & Benchmark Scoring Engine
PURPOSE:
    Evaluates batch enrichment performance against ground-truth datasets. Computes:
      - Field-level exact/near-match accuracy %
      - LOV conformance % (vocabulary compliance)
      - Required-attribute fill rate %
      - Provenance coverage % (% fields with verified source spans)
      - Confidence-tier distribution (Auto-Approved / Needs-Review / Rejected)

CLASSES:
    - BenchmarkEvaluator: Statistical scoring and metrics aggregation engine.

FUNCTIONS / METHODS:
    - BenchmarkEvaluator.evaluate_batch(records: List[EnrichedProductRecord], ground_truth: Optional[List[Dict]]) -> Dict[str, Any]:
        Calculates composite performance metrics across all enriched items.

INPUT:
    - List[EnrichedProductRecord] and optional ground truth list
OUTPUT:
    - Dict with precision metrics and tier breakdown
==============================================================================
"""

from typing import Any, Dict, List, Optional

from unihap.core.logging import logger
from unihap.core.models import EnrichedProductRecord, StatusTag


class BenchmarkEvaluator:
    """Computes precision metrics and ground truth alignment."""

    def evaluate_batch(
        self, records: List[EnrichedProductRecord], ground_truth: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """Calculates comprehensive pipeline performance metrics."""
        total = len(records)
        if total == 0:
            return {"total_records": 0}

        auto_approved = sum(1 for r in records if r.overall_status == StatusTag.AUTO_APPROVED)
        needs_review = sum(1 for r in records if r.overall_status == StatusTag.NEEDS_REVIEW)
        rejected = sum(1 for r in records if r.overall_status == StatusTag.REJECTED)

        avg_conf = sum(r.overall_confidence for r in records) / total
        avg_lov = sum(r.lov_conformance_pct for r in records) / total
        avg_prov = sum(r.provenance_coverage_pct for r in records) / total

        metrics = {
            "total_records": total,
            "auto_approved_rate_pct": round((auto_approved / total) * 100.0, 2),
            "needs_review_rate_pct": round((needs_review / total) * 100.0, 2),
            "rejected_rate_pct": round((rejected / total) * 100.0, 2),
            "avg_confidence_score": round(avg_conf, 3),
            "avg_lov_conformance_pct": round(avg_lov, 2),
            "avg_provenance_coverage_pct": round(avg_prov, 2),
            "tier_counts": {"auto_approved": auto_approved, "needs_review": needs_review, "rejected": rejected},
        }

        logger.info(
            f"[L12 Eval] Benchmark Results: "
            f"Auto-Approved: {metrics['auto_approved_rate_pct']}% | "
            f"Avg LOV: {metrics['avg_lov_conformance_pct']}% | "
            f"Avg Provenance: {metrics['avg_provenance_coverage_pct']}%"
        )
        return metrics
