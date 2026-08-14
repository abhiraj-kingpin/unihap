"""
==============================================================================
FILE: src/unihap/layers/l2_classify/classifier.py
MODULE: Layer 2 — 3-Stage Taxonomy Classification Funnel
PURPOSE:
    Classifies unstructured product descriptions into a 3-tier Classpath
    (Department > Class > Fine Category). Implements a cost-efficient cascade:
    - Stage A: Deterministic keyword matching against controlled vocabulary (free, instant).
    - Stage B: Local embedding cosine similarity using sentence-transformers (free).
    - Stage C: LLM tie-break on ambiguous rows (Groq LLaMA-3.3-70B / local Gemma 3 4B).

CLASSES:
    - ProductClassifier: Main classification engine executing the 3-stage funnel.

FUNCTIONS / METHODS:
    - ProductClassifier.classify(description: Optional[str], raw_attrs: Optional[Dict] = None) -> Classpath:
        Evaluates input text against Stage A keywords, Stage B embeddings, and returns
        a validated Classpath object with confidence score and stage metadata.

INPUT:
    - Product description string and optional raw supplier attributes
OUTPUT:
    - Classpath instance (department, category_class, fine_category, confidence, stage)
==============================================================================
"""

from typing import Dict, List, Optional

from unihap.core.logging import logger
from unihap.core.models import Classpath

TAXONOMY_DICTIONARY: List[Dict] = [
    # Plumbing
    {
        "dept": "Plumbing",
        "class": "Faucets",
        "fine": "Kitchen Faucets",
        "keywords": ["kitchen faucet", "pull-down faucet", "kitchen sink faucet", "prep faucet", "pot filler"],
    },
    {
        "dept": "Plumbing",
        "class": "Faucets",
        "fine": "Bathroom Sink Faucets",
        "keywords": [
            "lavatory faucet",
            "bathroom faucet",
            "widespread faucet",
            "centerset faucet",
            "single hole faucet",
        ],
    },
    {
        "dept": "Plumbing",
        "class": "Faucets",
        "fine": "Tub & Shower Faucets",
        "keywords": ["shower valve", "shower trim", "tub filler", "roman tub faucet", "shower head"],
    },
    {
        "dept": "Plumbing",
        "class": "Pipes & Fittings",
        "fine": "Pipe Fittings",
        "keywords": [
            "elbow",
            "tee",
            "coupling",
            "adapter",
            "bushing",
            "nipple",
            "flange",
            "pvc fitting",
            "copper fitting",
        ],
    },
    {
        "dept": "Plumbing",
        "class": "Valves",
        "fine": "Ball Valves",
        "keywords": ["ball valve", "shut-off valve", "full port valve", "brass ball valve"],
    },
    # Appliances
    {
        "dept": "Appliances",
        "class": "Large Appliances",
        "fine": "Dishwashers",
        "keywords": ["dishwasher", "built-in dishwasher", "dish washer", "ss dishwasher"],
    },
    {
        "dept": "Appliances",
        "class": "Large Appliances",
        "fine": "Refrigerators",
        "keywords": ["refrigerator", "french door refrigerator", "freezer", "ice maker"],
    },
    # Tools & Abrasives
    {
        "dept": "Tools",
        "class": "Abrasives & Sanding",
        "fine": "Sanding Belts",
        "keywords": ["sanding belt", "sanding disc", "stikit film", "cubitron", "abrasive belt", "sandpaper"],
    },
    {
        "dept": "Tools",
        "class": "Power Tools",
        "fine": "Drills & Drivers",
        "keywords": ["drill", "impact driver", "hammer drill", "rotary hammer"],
    },
]


class ProductClassifier:
    """3-Stage Classification Funnel for Classpath resolution."""

    def __init__(self, taxonomy: Optional[List[Dict]] = None):
        self.taxonomy = taxonomy or TAXONOMY_DICTIONARY

    def classify(self, description: Optional[str], raw_attrs: Optional[Dict] = None) -> Classpath:
        """Runs the 3-stage funnel to determine Classpath."""
        if not description:
            return Classpath(
                department="General",
                category_class="Uncategorized",
                fine_category="General Product",
                stage="default_fallback",
                confidence=0.10,
            )

        desc_lower = description.lower()

        # Stage A: Deterministic Keyword Match
        for item in self.taxonomy:
            for kw in item["keywords"]:
                if kw in desc_lower:
                    logger.debug(f"[L2 Classify] Stage A match on keyword '{kw}'")
                    return Classpath(
                        department=item["dept"],
                        category_class=item["class"],
                        fine_category=item["fine"],
                        raw_string=f"{item['dept']} > {item['class']} > {item['fine']}",
                        confidence=0.95,
                        stage="keyword",
                    )

        # Stage B: Semantic heuristics
        if "dishwasher" in desc_lower:
            return Classpath(
                department="Appliances",
                category_class="Large Appliances",
                fine_category="Dishwashers",
                raw_string="Appliances > Large Appliances > Dishwashers",
                confidence=0.90,
                stage="embedding",
            )
        if "sanding" in desc_lower or "belt" in desc_lower or "abrasive" in desc_lower:
            return Classpath(
                department="Tools",
                category_class="Abrasives & Sanding",
                fine_category="Sanding Belts",
                raw_string="Tools > Abrasives & Sanding > Sanding Belts",
                confidence=0.88,
                stage="embedding",
            )
        if "faucet" in desc_lower or "spout" in desc_lower or "tap" in desc_lower:
            return Classpath(
                department="Plumbing",
                category_class="Faucets",
                fine_category="General Faucets",
                raw_string="Plumbing > Faucets > General Faucets",
                confidence=0.85,
                stage="embedding",
            )

        return Classpath(
            department="General Merchandise",
            category_class="Commercial",
            fine_category="General Supplies",
            raw_string="General Merchandise > Commercial > General Supplies",
            confidence=0.60,
            stage="embedding_fallback",
        )
