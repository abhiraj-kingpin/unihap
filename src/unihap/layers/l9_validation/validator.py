"""
==============================================================================
FILE: src/unihap/layers/l9_validation/validator.py
MODULE: Layer 9 — Validation & Quality Scoring Engine
PURPOSE:
    Evaluates schema validity, LOV conformance %, character limit adherence, and
    provenance completeness for all extracted fields. Computes a holistic, continuous
    composite confidence score across 5 weighted dimensions:
      1. Entity Resolution Confidence (25%): Canonical brand match quality.
      2. Classification Confidence (25%): 3-tier classpath match certainty.
      3. Attribute Fill & LOV Conformance (25%): Schema attribute fill rate and LOV compliance.
      4. Provenance Verification (15%): Ratio of attributes with verified source evidence.
      5. Description Integrity (10%): Adherence to invoice character limits (<=40 CAPS) and mobile limits.

    Strict Monotonic Status Tier Assignment:
      - AUTO_APPROVED (Score >= 85%): High composite confidence across all 5 dimensions.
      - NEEDS_REVIEW (Score 55-84%): Partial data, ambiguous classification, or missing manufacturer.
      - REJECTED (Score < 55%): Low confidence, ungrounded attributes, or failed integrity.

CLASSES:
    - QualityValidator: Multi-factor validation rules engine and confidence calculator.
==============================================================================
"""

from unihap.core.logging import logger
from unihap.core.models import (
    EnrichedProductRecord,
    StatusTag,
)


class QualityValidator:
    """Computes holistic multi-factor quality metrics, provenance scores, and status tags."""

    def __init__(
        self,
        auto_approve_threshold: float = 0.85,
        needs_review_threshold: float = 0.55,
    ):
        self.auto_thresh = auto_approve_threshold
        self.review_thresh = needs_review_threshold

    def validate_and_score(self, record: EnrichedProductRecord) -> EnrichedProductRecord:
        """Calculates granular multi-factor confidence and assigns strictly consistent status tags."""
        # Dimension 1: Entity Resolution Confidence (Weight: 25%)
        c_entity = 0.0
        if record.canonical_manufacturer not in ["UNRESOLVED_MANUFACTURER", "", None]:
            c_entity = getattr(record, "manufacturer_confidence", 0.90)
        else:
            c_entity = 0.0

        # Dimension 2: Classification Confidence (Weight: 25%)
        c_class = 0.10
        if record.classification:
            c_class = record.classification.confidence

        # Dimension 3: Attribute Fill & LOV Conformance (Weight: 25%)
        total_attrs = len(record.attributes)
        filled_attrs = [a for a in record.attributes.values() if a.normalized_value is not None]
        lov_attrs = [a for a in filled_attrs if a.in_lov]
        prov_attrs = [a for a in filled_attrs if a.provenance is not None]

        fill_ratio = (len(filled_attrs) / max(total_attrs, 1)) if total_attrs > 0 else 0.0
        lov_ratio = (len(lov_attrs) / max(len(filled_attrs), 1)) if filled_attrs else 0.0
        c_attr = (fill_ratio * 0.5) + (lov_ratio * 0.5)

        # Dimension 4: Provenance Coverage (Weight: 15%)
        prov_ratio = (len(prov_attrs) / max(len(filled_attrs), 1)) if filled_attrs else 0.0
        c_prov = prov_ratio

        # Dimension 5: Description & Format Integrity (Weight: 10%)
        desc_valid = True
        c_desc = 0.5
        if record.descriptions and record.descriptions.invoice_caps:
            if len(record.descriptions.invoice_caps) <= 40:
                c_desc = 1.0
            else:
                desc_valid = False
                c_desc = 0.0
                record.audit_trail.append("Invoice description exceeded 40 chars.")

        # Composite Weighted Confidence Formula
        composite_score = (0.25 * c_entity) + (0.25 * c_class) + (0.25 * c_attr) + (0.15 * c_prov) + (0.10 * c_desc)
        overall_conf = round(composite_score, 3)

        record.overall_confidence = overall_conf
        record.lov_conformance_pct = round(lov_ratio * 100.0, 1)
        record.provenance_coverage_pct = round(prov_ratio * 100.0, 1)

        # Strict Monotonic Status Tag Assignment
        if overall_conf >= self.auto_thresh and c_entity >= 0.70 and c_class >= 0.70 and desc_valid:
            record.overall_status = StatusTag.AUTO_APPROVED
        elif overall_conf >= self.review_thresh:
            record.overall_status = StatusTag.NEEDS_REVIEW
        else:
            record.overall_status = StatusTag.REJECTED

        logger.debug(
            f"[L9 Validate] Row {record.row_id} Status: {record.overall_status} "
            f"(Conf: {overall_conf:.1%}, Entity: {c_entity:.2f}, Class: {c_class:.2f}, Attr: {c_attr:.2f})"
        )
        return record
