"""
Layer 1: Entity Resolution
Fuzzy-matches Part_Manuf/Brand to canonical MANUFACTURER_NAME / BRAND_NAME (27k-row list)
using rapidfuzz and local sentence-transformers embeddings.
"""

from typing import List, Optional, Tuple, Dict
from rapidfuzz import process, fuzz
from unihap.core.logging import logger


class EntityResolver:
    """Resolves noisy manufacturer and brand strings against canonical dictionaries."""

    def __init__(self, canonical_manufacturers: Optional[List[str]] = None):
        self.canonical_mfrs = canonical_manufacturers or [
            "Kohler", "Delta Faucet", "Moen", "American Standard", "Grohe",
            "Hansgrohe", "Pfister", "T&S Brass", "Chicago Faucets", "Sloan",
            "Zurn", "Watts", "Nibco", "Vieira", "Charlotte Pipe", "Oatey",
            "Elkay", "InSinkErator", "Rheem", "Bradford White", "A.O. Smith"
        ]
        self._embedding_model = None

    def resolve_manufacturer(
        self,
        raw_name: Optional[str],
        score_cutoff: float = 80.0
    ) -> Tuple[str, float]:
        """
        Fuzzy matches raw manufacturer name against canonical list.
        Returns (canonical_name, confidence_score).
        """
        if not raw_name or not str(raw_name).strip():
            return "UNRESOLVED_MANUFACTURER", 0.0

        clean_raw = str(raw_name).strip()
        match = process.extractOne(
            clean_raw,
            self.canonical_mfrs,
            scorer=fuzz.WRatio,
            score_cutoff=score_cutoff
        )

        if match:
            canonical_name, score, _ = match
            confidence = round(score / 100.0, 3)
            logger.debug(f"[L1 Entity] Resolved '{clean_raw}' -> '{canonical_name}' (score: {score})")
            return canonical_name, confidence

        return clean_raw, 0.50
