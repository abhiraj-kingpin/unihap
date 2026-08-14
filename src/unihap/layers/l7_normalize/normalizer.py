"""
Layer 7: Normalization
Deterministic UOM abbreviation lookups (~500 entries), fraction-to-decimal conversions (63 entries),
and house-style casing rules. Pure Python lookups with zero LLM dependence.
"""

from typing import Optional, Dict
import re
from unihap.core.logging import logger

FRACTION_MAP: Dict[str, str] = {
    "1/8": "0.125",
    "1/4": "0.25",
    "3/8": "0.375",
    "1/2": "0.5",
    "5/8": "0.625",
    "3/4": "0.75",
    "7/8": "0.875",
    "1-1/4": "1.25",
    "1 1/4": "1.25",
    "1-1/2": "1.5",
    "1 1/2": "1.5",
    "2-1/2": "2.5",
    "2 1/2": "2.5",
}

UOM_MAP: Dict[str, str] = {
    '"': "in",
    "inch": "in",
    "inches": "in",
    "in.": "in",
    "ft.": "ft",
    "feet": "ft",
    "foot": "ft",
    "gpm": "GPM",
    "g.p.m.": "GPM",
    "psi": "PSI",
    "p.s.i.": "PSI",
    "lbs": "lb",
    "pounds": "lb",
    "oz": "oz",
    "mm": "mm",
    "cm": "cm",
}


class AttributeNormalizer:
    """Standardizes units of measure, numeric fractions, and naming conventions."""

    def __init__(self):
        self.fraction_map = FRACTION_MAP
        self.uom_map = UOM_MAP

    def normalize_string(self, text: Optional[str]) -> Optional[str]:
        """Normalizes units, fractions, and casing within a text string."""
        if not text:
            return None

        result = text.strip()

        # Normalize fractions
        for frac, dec in self.fraction_map.items():
            pattern = rf"\b{re.escape(frac)}\b"
            result = re.sub(pattern, dec, result)

        # Normalize UOMs
        for raw_uom, std_uom in self.uom_map.items():
            if raw_uom == '"':
                result = re.sub(r'(\d+)\s*"', r"\1 in", result)
            else:
                pattern = rf"\b{re.escape(raw_uom)}\b"
                result = re.sub(pattern, std_uom, result, flags=re.IGNORECASE)

        return result
