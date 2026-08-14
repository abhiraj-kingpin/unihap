"""
==============================================================================
FILE: src/unihap/layers/l9_validation/validator.py
MODULE: Layer 9 — Validation & Quality Scoring Engine
PURPOSE:
    Evaluates schema validity, LOV conformance %, character limit adherence, and
    provenance completeness for all extracted fields. Computes an overall confidence
    score and assigns status tags:
      - AUTO_APPROVED (Score >= 90%): High confidence, straight-through processing.
      - NEEDS_REVIEW (Score 70-89%): Flagged for human curation triage queue.
      - REJECTED (Score < 70%): Low confidence or missing critical evidence.

CLASSES:
    - QualityValidator: Validation rules engine and confidence calculator.

FUNCTIONS / METHODS:
    - QualityValidator.validate_and_score(record: EnrichedProductRecord) -> EnrichedProductRecord:
        Calculates provenance coverage, LOV compliance %, checks length limits, and assigns StatusTag.

INPUT:
    - EnrichedProductRecord instance
OUTPUT:
    - EnrichedProductRecord with overall_confidence, lov_conformance_pct, and overall_status
==============================================================================
"""

from unihap.config import settings
from unihap.core.logging import logger
from unihap.core.models import EnrichedProductRecord, StatusTag


class QualityValidator:
    """Computes quality metrics, provenance scores, and status tags."""

    def __init__(
        self,
        auto_approve_threshold: float = settings.confidence_auto_approve,
        needs_review_threshold: float = settings.confidence_needs_review,
    ):
        self.auto_thresh = auto_approve_threshold
        self.review_thresh = needs_review_threshold

    def validate_and_score(self, record: EnrichedProductRecord) -> EnrichedProductRecord:
        """Calculates provenance coverage, LOV conformance, and assigns overall status."""
        total_attrs = len(record.attributes)
        if total_attrs == 0:
            record.overall_status = StatusTag.NEEDS_REVIEW
            record.overall_confidence = 0.0
            return record

        filled_attrs = [a for a in record.attributes.values() if a.normalized_value is not None]
        lov_attrs = [a for a in filled_attrs if a.in_lov]
        prov_attrs = [a for a in filled_attrs if a.provenance is not None]

        # Metric percentages
        lov_pct = (len(lov_attrs) / len(filled_attrs)) if filled_attrs else 0.0
        prov_pct = (len(prov_attrs) / len(filled_attrs)) if filled_attrs else 0.0

        # Description compliance checks
        desc_valid = True
        if len(record.descriptions.invoice_caps) > 40:
            desc_valid = False
            record.audit_trail.append("Invoice description exceeded 40 chars.")

        # Compute composite confidence
        base_score = (lov_pct * 0.45) + (prov_pct * 0.45) + (0.10 if desc_valid else 0.0)
        overall_conf = round(base_score, 3)

        record.overall_confidence = overall_conf
        record.lov_conformance_pct = round(lov_pct * 100.0, 1)
        record.provenance_coverage_pct = round(prov_pct * 100.0, 1)

        # Status Tag Assignment
        if overall_conf >= self.auto_thresh and desc_valid:
            record.overall_status = StatusTag.AUTO_APPROVED
        elif overall_conf >= self.review_thresh:
            record.overall_status = StatusTag.NEEDS_REVIEW
        else:
            record.overall_status = StatusTag.REJECTED

        logger.debug(f"[L9 Validate] Row {record.row_id} Status: {record.overall_status} (Conf: {overall_conf})")
        return record
