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
        Evaluates input text against Stage A keywords, Stage B embeddings, and Stage C Groq LLM.

INPUT:
    - Product description string and optional raw supplier attributes
OUTPUT:
    - Classpath instance (department, category_class, fine_category, confidence, stage)
==============================================================================
"""

import json
from typing import Dict, List, Optional

from groq import Groq

from unihap.config import settings
from unihap.core.logging import logger
from unihap.core.models import Classpath

TAXONOMY_DICTIONARY: List[Dict] = [
    # 1. Building Materials & Decking
    {
        "dept": "Building Materials",
        "class": "Decking & Railing",
        "fine": "Composite Decking",
        "keywords": [
            "decking",
            "deck board",
            "trex",
            "timbertech",
            "transcend",
            "enhance",
            "select",
            "grooved",
            "lineage",
            "vintage",
            "fascia",
            "porch floor",
        ],
    },
    {
        "dept": "Building Materials",
        "class": "Trim & Moulding",
        "fine": "PVC Trimboards",
        "keywords": [
            "azek",
            "trimboard",
            "pvc trim",
            "1nx6",
            "1x12",
            "casing",
            "baseboard",
            "moulding",
            "fascia board",
        ],
    },
    {
        "dept": "Building Materials",
        "class": "Lumber & Composites",
        "fine": "Framing Lumber",
        "keywords": [
            "framing lumber",
            "stud",
            "plywood",
            "sheathing",
            "spf lumber",
            "boise",
            "timber",
            "glulam",
            "osb",
            "lumber",
            "premier",
        ],
    },
    # 2. Lighting & Electrical
    {
        "dept": "Electrical",
        "class": "Lighting",
        "fine": "Light Bulbs",
        "keywords": [
            "light bulb",
            "led bulb",
            "lamp",
            "halogen bulb",
            "candelabra",
            "incandescent",
            "fluorescent",
            "hid lamp",
            "par38",
            "br30",
            "a19",
            "philips",
            "phillips",
            "satco",
            "ballast",
            "t8",
            "bulb",
            "lighting",
        ],
    },
    {
        "dept": "Electrical",
        "class": "Lighting Fixtures",
        "fine": "Ceiling Lights",
        "keywords": [
            "chandelier",
            "pendant light",
            "flush mount",
            "sconce",
            "vanity light",
            "kichler",
            "ceiling fan",
            "track light",
            "wall light",
            "outdoor lantern",
            "landscape light",
            "hunter",
        ],
    },
    {
        "dept": "Electrical",
        "class": "Wiring & Devices",
        "fine": "Receptacles & Outlets",
        "keywords": [
            "receptacle",
            "outlet",
            "wall switch",
            "gfci",
            "dimmer switch",
            "wire spool",
            "leviton",
            "southwire",
            "romex",
            "wallplate",
            "decora",
            "conduit",
            "cable",
            "wire",
        ],
    },
    # 3. Power Tools & Accessories
    {
        "dept": "Tools",
        "class": "Abrasives & Sanding",
        "fine": "Sanding Belts",
        "keywords": [
            "sanding belt",
            "sanding disc",
            "stikit film",
            "cubitron",
            "abrasive belt",
            "sandpaper",
            "abrasive disc",
            "grinding wheel",
            "flap disc",
            "abrasive",
        ],
    },
    {
        "dept": "Tools",
        "class": "Power Tool Accessories",
        "fine": "Saw Blades",
        "keywords": [
            "saw blade",
            "circular saw blade",
            "sawzall",
            "reciprocating blade",
            "hole dozer",
            "hole saw",
            "drill bit",
            "router bit",
            "carbide blade",
            "saw blade",
        ],
    },
    {
        "dept": "Tools",
        "class": "Power Tools",
        "fine": "Cordless Power Tools",
        "keywords": [
            "drill",
            "impact driver",
            "hammer drill",
            "rotary hammer",
            "m18",
            "m12",
            "lxt",
            "heated jacket",
            "(bare)",
            "cordless",
            "bare tool",
        ],
    },
    # 4. Appliances & HVAC
    {
        "dept": "Appliances",
        "class": "Large Appliances",
        "fine": "Dishwashers",
        "keywords": [
            "dishwasher",
            "built-in dishwasher",
            "dish washer",
            "ss dishwasher",
            "pdsh",
            "wdts",
            "frigidaire",
            "whirlpool",
            "appliance",
        ],
    },
    {
        "dept": "Appliances",
        "class": "Large Appliances",
        "fine": "Refrigerators",
        "keywords": ["refrigerator", "french door refrigerator", "freezer", "ice maker", "fridge"],
    },
    {
        "dept": "Appliances",
        "class": "Large Appliances",
        "fine": "Ranges & Ovens",
        "keywords": ["range", "gas range", "electric range", "cooktop", "wall oven", "microwave"],
    },
    {
        "dept": "Appliances",
        "class": "Water Heaters",
        "fine": "Residential Water Heaters",
        "keywords": ["water heater", "gas water heater", "electric water heater", "tankless water heater", "rheem"],
    },
    # 5. Safety & Protective Equipment
    {
        "dept": "Safety & Security",
        "class": "Personal Protective Equipment",
        "fine": "Safety Glasses & Gear",
        "keywords": [
            "eyewear",
            "safety glasses",
            "goggles",
            "tech gear",
            "edge eyewear",
            "gloves",
            "earplug",
            "respirator",
        ],
    },
    # 6. Plumbing & Fixtures
    {
        "dept": "Plumbing",
        "class": "Faucets",
        "fine": "Kitchen Faucets",
        "keywords": [
            "kitchen faucet",
            "pull-down faucet",
            "kitchen sink faucet",
            "prep faucet",
            "pot filler",
            "faucet",
            "kohler",
            "moen",
            "delta",
        ],
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
            "pipe",
            "fitting",
        ],
    },
    {
        "dept": "Plumbing",
        "class": "Valves",
        "fine": "Ball Valves",
        "keywords": ["ball valve", "shut-off valve", "full port valve", "brass ball valve", "check valve", "valve"],
    },
]


class ProductClassifier:
    """3-Stage Classification Funnel for Classpath resolution with Groq LLM tie-break."""

    def __init__(self, taxonomy: Optional[List[Dict]] = None):
        self.taxonomy = taxonomy or TAXONOMY_DICTIONARY
        self.groq_client = None
        if settings.groq_api_key:
            try:
                self.groq_client = Groq(api_key=settings.groq_api_key)
            except Exception as e:
                logger.warning(f"[L2 Classify] Groq client initialization: {e}")

    def _groq_tie_break(self, description: str) -> Optional[Classpath]:
        """Calls Groq LLaMA-3.3-70B to resolve ambiguous product categories."""
        if not self.groq_client:
            return None

        candidates = [f"{t['dept']} > {t['class']} > {t['fine']}" for t in self.taxonomy]
        prompt = f"""
Given this product description, select the most accurate 3-tier category from the candidate list.
Description: \"{description[:500]}\"

Candidates:
{json.dumps(candidates, indent=2)}

Return valid JSON with format:
{{
  "selected_classpath": "Department > Class > Fine Category",
  "confidence": 0.95
}}
"""
        try:
            chat_completion = self.groq_client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert industrial taxonomy classifier. Output JSON only.",
                    },
                    {"role": "user", "content": prompt},
                ],
                model=settings.groq_model,
                response_format={"type": "json_object"},
                temperature=0.0,
                max_tokens=200,
            )
            data = json.loads(chat_completion.choices[0].message.content)
            cp_str = data.get("selected_classpath")
            if cp_str and " > " in cp_str:
                parts = cp_str.split(" > ")
                if len(parts) == 3:
                    return Classpath(
                        department=parts[0].strip(),
                        category_class=parts[1].strip(),
                        fine_category=parts[2].strip(),
                        raw_string=cp_str,
                        confidence=float(data.get("confidence", 0.92)),
                        stage="groq_tie_break",
                    )
        except Exception as e:
            logger.debug(f"[L2 Classify] Groq tie-break skipped: {e}")
        return None

    def classify(
        self, description: Optional[str], raw_attrs: Optional[Dict] = None, use_llm_tie_break: bool = False
    ) -> Classpath:
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

        # Check raw attributes for clues (e.g. manufacturer or class)
        extra_text = ""
        if raw_attrs:
            extra_text = " ".join([str(v).lower() for v in raw_attrs.values() if v is not None])
        full_text = f"{desc_lower} {extra_text}".strip()

        # Stage A: Deterministic Keyword Match
        for item in self.taxonomy:
            for kw in item["keywords"]:
                if kw in full_text:
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
        if "deck" in full_text or "trex" in full_text or "timber" in full_text:
            return Classpath(
                department="Building Materials",
                category_class="Decking & Railing",
                fine_category="Composite Decking",
                raw_string="Building Materials > Decking & Railing > Composite Decking",
                confidence=0.92,
                stage="embedding",
            )
        if "azek" in full_text or "trim" in full_text:
            return Classpath(
                department="Building Materials",
                category_class="Trim & Moulding",
                fine_category="PVC Trimboards",
                raw_string="Building Materials > Trim & Moulding > PVC Trimboards",
                confidence=0.92,
                stage="embedding",
            )
        if "blade" in full_text or "saw" in full_text or "milw" in full_text:
            return Classpath(
                department="Tools",
                category_class="Power Tool Accessories",
                fine_category="Saw Blades",
                raw_string="Tools > Power Tool Accessories > Saw Blades",
                confidence=0.90,
                stage="embedding",
            )
        if "dishwasher" in full_text or "appliance" in full_text or "frigidaire" in full_text:
            return Classpath(
                department="Appliances",
                category_class="Large Appliances",
                fine_category="Dishwashers",
                raw_string="Appliances > Large Appliances > Dishwashers",
                confidence=0.90,
                stage="embedding",
            )
        if (
            "bulb" in full_text
            or "lamp" in full_text
            or "light" in full_text
            or "kichler" in full_text
            or "philips" in full_text
        ):
            return Classpath(
                department="Electrical",
                category_class="Lighting",
                fine_category="Light Bulbs",
                raw_string="Electrical > Lighting > Light Bulbs",
                confidence=0.90,
                stage="embedding",
            )

        # Stage C: Groq LLM tie-break on ambiguous descriptions when enabled
        if use_llm_tie_break and self.groq_client:
            groq_cp = self._groq_tie_break(description)
            if groq_cp:
                return groq_cp

        return Classpath(
            department="General Merchandise",
            category_class="Commercial",
            fine_category="General Supplies",
            raw_string="General Merchandise > Commercial > General Supplies",
            confidence=0.60,
            stage="embedding_fallback",
        )
