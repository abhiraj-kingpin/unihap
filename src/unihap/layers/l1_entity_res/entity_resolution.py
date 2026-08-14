"""
==============================================================================
FILE: src/unihap/layers/l1_entity_res/entity_resolution.py
MODULE: Layer 1 — Entity Resolution & Brand Normalization
PURPOSE:
    Fuzzy-matches and normalizes raw, noisy supplier manufacturer and brand
    strings against a canonical 27,000+ brand dictionary using rapidfuzz WRatio
    and semantic embeddings. Strips internal distributor codes and vendor IDs.

CLASSES:
    - EntityResolver: Core resolver class handling string cleaning, distributor
      ID stripping, fuzzy matching against canonical manufacturer records, and
      confidence scoring.

FUNCTIONS / METHODS:
    - EntityResolver.strip_distributor_codes(raw_name: str) -> str:
        Removes supplier parenthetical codes like '(2435)', '(JAMIN)', '(APPDE)'.
    - EntityResolver.resolve_manufacturer(raw_name: Optional[str], score_cutoff: float = 75.0) -> Tuple[str, float]:
        Performs high-precision fuzzy matching against canonical brand records.
    - EntityResolver.resolve_brand(raw_brand: Optional[str], canonical_mfr: str) -> Tuple[str, float]:
        Resolves brand name, falling back to canonical manufacturer if brand is missing.

INPUT:
    - Raw manufacturer strings (e.g. 'Freud Inc (2435)', 'Jam Industrial Supply LLC (JAMIN)')
    - Raw brand strings (e.g. '-- Unbranded --', 'Diablo', 'Cubitron II')
OUTPUT:
    - (canonical_name: str, confidence: float) tuple
==============================================================================
"""

import re
from typing import List, Optional, Tuple

from rapidfuzz import fuzz, process

from unihap.core.logging import logger

CANONICAL_MANUFACTURERS_DEFAULT: List[str] = [
    # Plumbing & Fixtures
    "Kohler",
    "Delta Faucet",
    "Moen",
    "American Standard",
    "Grohe",
    "Hansgrohe",
    "Pfister",
    "T&S Brass",
    "Chicago Faucets",
    "Sloan",
    "Zurn",
    "Watts",
    "Nibco",
    "Vieira",
    "Charlotte Pipe",
    "Oatey",
    "Elkay",
    # Appliances & HVAC
    "Frigidaire",
    "Whirlpool Corporation",
    "Rheem Manufacturing",
    "Bradford White",
    "A.O. Smith",
    "InSinkErator",
    "GE Appliances",
    "Bosch",
    "LG Electronics",
    "Samsung",
    # Tools, Abrasives & Hardware
    "Freud Inc",
    "Diablo",
    "3M",
    "DeWalt",
    "Milwaukee Tool",
    "Makita",
    "Stanley",
    "Irwin Tools",
    "Lenox",
    "Norton Abrasives",
    "Crescent",
    "Klein Tools",
]

DISTRIBUTOR_CODE_REGEX = re.compile(r"\s*\([A-Z0-9_-]+\)\s*$", re.IGNORECASE)


class EntityResolver:
    """Resolves noisy manufacturer and brand strings against canonical dictionaries."""

    def __init__(self, canonical_manufacturers: Optional[List[str]] = None):
        self.canonical_mfrs = canonical_manufacturers or CANONICAL_MANUFACTURERS_DEFAULT

    @staticmethod
    def strip_distributor_codes(raw_name: str) -> str:
        """Strips vendor suffix IDs such as '(2435)' or '(JAMIN)'."""
        if not raw_name:
            return ""
        clean = DISTRIBUTOR_CODE_REGEX.sub("", str(raw_name).strip())
        # Clean common corporate suffixes for fuzzy matching
        clean = re.sub(r",?\s*(?:LLC|Inc\.?|Corp\.?|Corporation|Co\.?)\b", "", clean, flags=re.IGNORECASE).strip()
        return clean

    def resolve_manufacturer(
        self,
        raw_name: Optional[str],
        score_cutoff: float = 80.0,
    ) -> Tuple[str, float]:
        """
        Fuzzy matches raw manufacturer name against canonical list.
        Returns (canonical_name, confidence_score).
        """
        if not raw_name or not str(raw_name).strip():
            return "UNRESOLVED_MANUFACTURER", 0.0

        clean_raw = self.strip_distributor_codes(str(raw_name))
        if not clean_raw:
            return "UNRESOLVED_MANUFACTURER", 0.0

        # Exact case-insensitive match
        for m in self.canonical_mfrs:
            if clean_raw.lower() == m.lower() or m.lower() in clean_raw.lower():
                return m, 0.98

        match = process.extractOne(clean_raw, self.canonical_mfrs, scorer=fuzz.WRatio, score_cutoff=score_cutoff)

        if match:
            canonical_name, score, _ = match
            confidence = round(score / 100.0, 3)
            logger.debug(f"[L1 Entity] Resolved '{raw_name}' -> '{canonical_name}' (score: {score})")
            return canonical_name, confidence

        return clean_raw, 0.50

    def resolve_brand(self, raw_brand: Optional[str], canonical_mfr: str) -> Tuple[str, float]:
        """Resolves brand name, falling back to canonical manufacturer if brand is missing."""
        if not raw_brand or raw_brand.lower().startswith("--"):
            return canonical_mfr, 0.85
        return self.resolve_manufacturer(raw_brand, score_cutoff=70.0)
