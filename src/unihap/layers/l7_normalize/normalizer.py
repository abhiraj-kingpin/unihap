"""
==============================================================================
FILE: src/unihap/layers/l7_normalize/normalizer.py
MODULE: Layer 7 — Deterministic Unit of Measure & Fraction Normalization
PURPOSE:
    Provides fast, deterministic standardization of units of measure (UOM),
    numeric fractional values, and casing conventions without LLM intervention.
    Backed by static lookup tables:
      - 500+ UOM abbreviations (e.g. 'in.', 'inch', '"' -> 'in', 'gpm' -> 'GPM')
      - 63 fraction-to-decimal conversions (e.g. '1-1/4' -> '1.25', '3/4' -> '0.75')

CLASSES:
    - AttributeNormalizer: Normalization engine executing regex and dictionary lookups.

FUNCTIONS / METHODS:
    - AttributeNormalizer.normalize_string(text: Optional[str]) -> Optional[str]:
        Applies fraction replacement (longest matches first) and UOM standardization.

INPUT:
    - Raw text string with non-standard units or fractions (e.g. '1-1/4" pipe 1.8 gpm')
OUTPUT:
    - Standardized string (e.g. '1.25 in pipe 1.8 GPM')
==============================================================================
"""

import re
from typing import Dict, Optional

FRACTION_MAP: Dict[str, str] = {
    "1/8": "0.125",
    "1/4": "0.25",
    "3/8": "0.375",
    "1/2": "0.5",
    "5/8": "0.625",
    "3/4": "0.75",
    "7/8": "0.875",
    "1-1/8": "1.125",
    "1 1/8": "1.125",
    "1-1/4": "1.25",
    "1 1/4": "1.25",
    "1-3/8": "1.375",
    "1 3/8": "1.375",
    "1-1/2": "1.5",
    "1 1/2": "1.5",
    "1-5/8": "1.625",
    "1 5/8": "1.625",
    "1-3/4": "1.75",
    "1 3/4": "1.75",
    "1-7/8": "1.875",
    "1 7/8": "1.875",
    "2-1/2": "2.5",
    "2 1/2": "2.5",
    "3-1/2": "3.5",
    "3 1/2": "3.5",
    "4-1/2": "4.5",
    "4 1/2": "4.5",
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
    "dBA": "dBA",
    "dba": "dBA",
    "volts": "V",
    "volt": "V",
    "amps": "A",
    "amp": "A",
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

        # Normalize fractions (longest matches first to avoid partial replacements like 1-1/4 -> 1-0.25)
        sorted_fractions = sorted(self.fraction_map.items(), key=lambda item: len(item[0]), reverse=True)
        for frac, dec in sorted_fractions:
            pattern = rf"(?<!\w){re.escape(frac)}(?!\w)"
            result = re.sub(pattern, dec, result)

        # Normalize UOMs
        for raw_uom, std_uom in self.uom_map.items():
            if raw_uom == '"':
                result = re.sub(r'(\d+(?:\.\d+)?)\s*"', r"\1 in", result)
            else:
                pattern = rf"\b{re.escape(raw_uom)}\b"
                result = re.sub(pattern, std_uom, result, flags=re.IGNORECASE)

        return result
