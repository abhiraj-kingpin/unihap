"""
Layer 10: Human-in-the-Loop Review Queue
Manages review queue for flagged rows with source diff view.
Accepts manual corrections and feeds them back into L6 few-shot PatternRAG cache.
"""

from typing import List, Dict, Optional
from unihap.core.models import EnrichedProductRecord, StatusTag
from unihap.core.logging import logger


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
        self,
        row_id: str,
        corrected_attributes: Dict[str, str],
        reviewer_id: str = "human_curator"
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
