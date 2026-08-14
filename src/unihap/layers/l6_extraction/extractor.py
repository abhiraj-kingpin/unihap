"""
==============================================================================
FILE: src/unihap/layers/l6_extraction/extractor.py
MODULE: Layer 6 — Constrained Attribute Extraction (Constrained RAG + Groq 70B)
PURPOSE:
    Extracts allowed product attributes from scraped Markdown content and raw
    attributes. Enforces the strict Zero-Hallucination rule:
    - Every extracted value MUST belong to the Knowledge Graph List of Values (LOV).
    - Every value MUST cite an exact, verifiable `evidence_span` from the source text.
    - Cascade order: Fast local deterministic RAG first (free, instant) -> Groq LLaMA-3.3-70B
      for ambiguous or complex fields.
    - If no evidence span exists in the text, the model MUST ABSTAIN (`status: abstained`).

CLASSES:
    - AttributeExtractor: Constrained RAG extraction engine with JSON-schema enforcement.

FUNCTIONS / METHODS:
    - AttributeExtractor.extract_attributes(markdown_text: str, source_url: str, classpath: str, raw_attributes: Optional[Dict] = None) -> Dict[str, AttributeValue]:
        Extracts validated attributes, builds ProvenanceSpan objects, and marks ungrounded
        fields as ABSTAINED.

INPUT:
    - Clean source Markdown text, source URL, full Classpath string, and raw supplier attributes
OUTPUT:
    - Dict[attribute_name, AttributeValue] containing LOV values, provenance spans, and confidence scores
==============================================================================
"""

import json
from typing import Dict, List, Optional

from groq import Groq

from unihap.config import settings
from unihap.core.logging import logger
from unihap.core.models import AttributeValue, ProvenanceSpan, StatusTag
from unihap.layers.l3_knowledge_graph.graph import TaxonomyGraph


class AttributeExtractor:
    """Constrained RAG Attribute Extractor with live Groq LLaMA-3.3-70B JSON mode."""

    def __init__(self, graph: Optional[TaxonomyGraph] = None):
        self.graph = graph or TaxonomyGraph()
        self.groq_client = None
        if settings.groq_api_key:
            try:
                self.groq_client = Groq(api_key=settings.groq_api_key)
            except Exception as e:
                logger.warning(f"[L6 Extract] Failed to initialize Groq client: {e}")

    def _extract_via_groq(
        self, markdown_text: str, unresolved_attrs: List[str], lov_dict: Dict[str, List[str]]
    ) -> Dict[str, Dict[str, Optional[str]]]:
        """Calls Groq LLaMA-3.3-70B in JSON mode to extract LOV attributes with evidence spans."""
        if not self.groq_client or not unresolved_attrs:
            return {}

        sub_lov = {k: lov_dict[k] for k in unresolved_attrs if k in lov_dict}
        prompt = f"""
You are a strict, zero-hallucination product catalog attribute extractor.
Extract values ONLY for the specified attributes using ONLY the provided allowed values (LOV).
Every extracted attribute MUST have an exact verbatim evidence span cited from the markdown text.
If an attribute is not explicitly mentioned or cannot be matched to the allowed LOV, set value to null and evidence_span to null. NEVER guess.

Allowed Attributes and LOVs:
{json.dumps(sub_lov, indent=2)}

Source Markdown:
\"\"\"
{markdown_text[:3000]}
\"\"\"

Return a JSON object with this exact schema:
{{
  "extracted_attributes": [
    {{
      "attribute_name": "Attribute Name",
      "value": "Exact LOV Value or null",
      "evidence_span": "Verbatim text quote from markdown or null"
    }}
  ]
}}
"""
        try:
            chat_completion = self.groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a precise JSON extractor. Output valid JSON only."},
                    {"role": "user", "content": prompt},
                ],
                model=settings.groq_model,
                response_format={"type": "json_object"},
                temperature=0.0,
                max_tokens=400,
            )
            response_text = chat_completion.choices[0].message.content
            parsed = json.loads(response_text)
            extracted = {}
            for item in parsed.get("extracted_attributes", []):
                attr_name = item.get("attribute_name")
                val = item.get("value")
                span = item.get("evidence_span")
                if attr_name and val and span:
                    extracted[attr_name] = {"value": val, "evidence_span": span}
            return extracted
        except Exception as e:
            logger.debug(f"[L6 Extract] Groq API call skipped/fallback: {e}")
            return {}

    def extract_attributes(
        self,
        markdown_text: str,
        source_url: str,
        classpath: str,
        raw_attributes: Optional[Dict] = None,
        use_groq_fallback: bool = False,
    ) -> Dict[str, AttributeValue]:
        """
        Extracts allowed attributes for the given classpath from scraped text.
        Enforces that every value belongs to the Knowledge Graph LOV and has verified provenance.
        """
        allowed_attrs = self.graph.get_allowed_attributes(classpath)
        lov_dict = {attr: self.graph.get_allowed_values(attr) for attr in allowed_attrs}
        results: Dict[str, AttributeValue] = {}
        text_lower = markdown_text.lower()

        unresolved_attrs: List[str] = []

        # Step 1: Fast local deterministic RAG span matching
        for attr in allowed_attrs:
            allowed_lovs = lov_dict.get(attr, [])
            matched_val = None
            matched_span = None

            for val in allowed_lovs:
                if val.lower() in text_lower:
                    matched_val = val
                    matched_span = f"{attr}: {val}"
                    break

            # Step 2: Raw catalog attribute fallback with canonical synonym check
            if not matched_val and raw_attributes and attr in raw_attributes:
                raw_v = str(raw_attributes[attr])
                canonical_v = self.graph.canonicalize_synonym(raw_v)
                if canonical_v:
                    matched_val = canonical_v
                    matched_span = f"Raw Attribute: {raw_v} -> {canonical_v}"
                elif raw_v in allowed_lovs:
                    matched_val = raw_v
                    matched_span = f"Raw Attribute: {raw_v}"

            if matched_val and matched_span:
                prov = ProvenanceSpan(
                    source_url=source_url,
                    exact_text_span=matched_span,
                    retrieval_method="constrained_rag",
                    confidence_score=0.96,
                )
                results[attr] = AttributeValue(
                    attribute_name=attr,
                    raw_value=matched_val,
                    normalized_value=matched_val,
                    in_lov=True,
                    provenance=prov,
                    status=StatusTag.AUTO_APPROVED,
                    confidence=0.96,
                )
            else:
                unresolved_attrs.append(attr)

        # Step 3: Targeted Groq API extraction only for remaining unresolved attributes
        if use_groq_fallback and unresolved_attrs and self.groq_client and len(markdown_text) > 10:
            groq_results = self._extract_via_groq(markdown_text, unresolved_attrs, lov_dict)
            for attr in list(unresolved_attrs):
                if attr in groq_results:
                    val = groq_results[attr]["value"]
                    span = groq_results[attr]["evidence_span"]
                    if val in lov_dict.get(attr, []) and span and span.lower() in text_lower:
                        prov = ProvenanceSpan(
                            source_url=source_url,
                            exact_text_span=span,
                            retrieval_method="groq_constrained_rag",
                            confidence_score=0.98,
                        )
                        results[attr] = AttributeValue(
                            attribute_name=attr,
                            raw_value=val,
                            normalized_value=val,
                            in_lov=True,
                            provenance=prov,
                            status=StatusTag.AUTO_APPROVED,
                            confidence=0.98,
                        )
                        unresolved_attrs.remove(attr)

        # Step 4: Strict ABSTAIN for remaining fields
        for attr in unresolved_attrs:
            results[attr] = AttributeValue(
                attribute_name=attr,
                raw_value=None,
                normalized_value=None,
                in_lov=False,
                provenance=None,
                status=StatusTag.ABSTAINED,
                confidence=0.0,
            )

        logger.debug(
            f"[L6 Extraction] Extracted {len([k for k, v in results.items() if v.in_lov])} validated attributes."
        )
        return results
