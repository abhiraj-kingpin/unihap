"""
Layer 8: Description Synthesis
Generates 5 standardized e-commerce description formats strictly from validated attributes:
1. Invoice (<= 40 characters, ALL CAPS)
2. Mobile (60-80 characters)
3. Short Title
4. Long Narrative Description
5. Retail Feature Bullet Points
"""

from typing import Dict, Optional, List
from unihap.core.models import AttributeValue, ProductDescriptionSet, Classpath
from unihap.core.logging import logger


class DescriptionSynthesizer:
    """Deterministic template synthesizer for 5 catalog description formats."""

    def synthesize(
        self,
        manufacturer: str,
        mpn: str,
        classification: Optional[Classpath],
        attributes: Dict[str, AttributeValue]
    ) -> ProductDescriptionSet:
        """Constructs 5 description formats strictly using validated attributes."""
        fine_cat = classification.fine_category if classification else "Product"
        finish = attributes.get("Finish")
        finish_str = f" in {finish.normalized_value}" if (finish and finish.normalized_value) else ""
        flow = attributes.get("Flow Rate")
        flow_str = f", {flow.normalized_value}" if (flow and flow.normalized_value) else ""
        handle = attributes.get("Handle Count")
        handle_str = f", {handle.normalized_value}-Handle" if (handle and handle.normalized_value) else ""

        # 1. Invoice (<= 40 CAPS)
        raw_invoice = f"{manufacturer[:8]} {mpn} {fine_cat[:12]} {finish.normalized_value[:4] if finish and finish.normalized_value else ''}"
        invoice_caps = raw_invoice.upper()[:40].strip()

        # 2. Mobile (60-80 chars)
        mobile_raw = f"{manufacturer} {mpn} {fine_cat}{finish_str}{handle_str}"
        if len(mobile_raw) > 80:
            mobile_desc = mobile_raw[:77] + "..."
        else:
            mobile_desc = mobile_raw

        # 3. Short Title
        short_title = f"{manufacturer} {mpn} {fine_cat}{finish_str}{flow_str}"

        # 4. Long Description
        long_desc = (
            f"The {manufacturer} {mpn} is a high-performance {fine_cat.lower()}{finish_str}. "
            f"Engineered for reliability, it features precision craftsmanship{flow_str}{handle_str}."
        )

        # 5. Retail Bullet Points
        bullets = [
            f"Manufacturer: {manufacturer}",
            f"Model / MPN: {mpn}",
            f"Category: {fine_cat}",
        ]
        if finish and finish.normalized_value:
            bullets.append(f"Finish: {finish.normalized_value}")
        if flow and flow.normalized_value:
            bullets.append(f"Flow Rate: {flow.normalized_value}")
        if handle and handle.normalized_value:
            bullets.append(f"Handle Configuration: {handle.normalized_value}-Handle")

        return ProductDescriptionSet(
            invoice_caps=invoice_caps,
            mobile=mobile_desc,
            short_title=short_title,
            long_desc=long_desc,
            retail_bullet_points=bullets
        )
