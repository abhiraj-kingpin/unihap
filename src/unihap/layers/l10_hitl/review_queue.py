"""
==============================================================================
FILE: src/unihap/layers/l10_hitl/review_queue.py
MODULE: Layer 10 — Human-in-the-Loop (HITL) Triage & Review Queue
PURPOSE:
    Manages the triage queue for catalog items flagged as NEEDS_REVIEW or REJECTED.
    Provides a source diff review interface, records human curator corrections,
    and updates the few-shot PatternRAG feedback cache to improve future predictions.

CLASSES:
    - ReviewQueueManager: In-memory queue manager for human verification and corrections.

FUNCTIONS / METHODS:
    - ReviewQueueManager.add_to_queue(record: EnrichedProductRecord): Adds flagged record to triage queue.
    - ReviewQueueManager.apply_human_correction(row_id, corrected_attributes, reviewer_id) -> Optional[EnrichedProductRecord]:
        Applies curator corrections and promotes record status to AUTO_APPROVED.

INPUT:
    - Flagged EnrichedProductRecord instances and human correction dictionaries
OUTPUT:
    - Promoted EnrichedProductRecord with audit trail entry
==============================================================================
"""

from typing import Dict, List, Optional

from unihap.core.logging import logger
from unihap.core.models import EnrichedProductRecord, StatusTag


class ReviewQueueManager:
    """Manages triage queue for human verification of ambiguous catalog items."""

    def __init__(self):
        self.queue: List[EnrichedProductRecord] = []
        self.approved_corrections: Dict[str, Dict] = {}

    def add_to_queue(self, record: EnrichedProductRecord):
        """Adds a record flagged as NEEDS_REVIEW or REJECTED into queue."""
        if record.overall_status in [StatusTag.NEEDS_REVIEW, StatusTag.REJECTED]:
            self.queue.append(record)

    def apply_human_correction(
        self, row_id: str, corrected_attributes: Dict[str, str], reviewer_id: str = "human_curator"
    ) -> Optional[EnrichedProductRecord]:
        """Applies human correction, updating the record status to AUTO_APPROVED."""
        for rec in self.queue:
            if rec.row_id == row_id:
                for attr_name, val in corrected_attributes.items():
                    if attr_name in rec.attributes:
                        rec.attributes[attr_name].normalized_value = val
                        rec.attributes[attr_name].status = StatusTag.AUTO_APPROVED
                rec.overall_status = StatusTag.AUTO_APPROVED
                rec.audit_trail.append(f"Human correction by {reviewer_id}")
                self.approved_corrections[row_id] = corrected_attributes
                logger.info(f"[L10 HITL] Applied human correction for Row {row_id}")
                return rec
        return None
