"""
Core Pydantic data models for UniHAP pipeline.
Enforces strict schema validation, provenance tracking, and LOV constraints.
"""

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class StatusTag(str, Enum):
    """Validation and review status for an enriched field or product."""
    AUTO_APPROVED = "auto-approved"
    NEEDS_REVIEW = "needs-review"
    REJECTED = "rejected"
    ABSTAINED = "abstained"


class ProvenanceSpan(BaseModel):
    """Source evidence span backing any extracted attribute fact."""
    source_url: str = Field(description="URL of the official manufacturer domain page")
    exact_text_span: str = Field(description="Exact character span retrieved from markdown/table")
    retrieval_method: str = Field(default="crawl4ai_scrape", description="Method used to fetch page")
    confidence_score: float = Field(default=1.0, ge=0.0, le=1.0)


class AttributeValue(BaseModel):
    """Represents an extracted and normalized attribute value with provenance."""
    attribute_name: str
    raw_value: Optional[str] = None
    normalized_value: Optional[str] = None
    uom: Optional[str] = None
    in_lov: bool = Field(default=False, description="Whether normalized value belongs to List of Values")
    provenance: Optional[ProvenanceSpan] = None
    status: StatusTag = StatusTag.NEEDS_REVIEW
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)


class Classpath(BaseModel):
    """Hierarchical taxonomy classification (Dept > Class > Fine)."""
    department: str
    category_class: str
    fine_category: str
    raw_string: str = ""
    confidence: float = 1.0
    stage: str = "keyword"  # keyword, embedding, or groq_tie_break

    @property
    def full_path(self) -> str:
        return f"{self.department} > {self.category_class} > {self.fine_category}"


class ProductDescriptionSet(BaseModel):
    """5 standardized description formats generated from validated attributes."""
    invoice_caps: str = Field(default="", max_length=40, description="<=40 characters, ALL CAPS")
    mobile: str = Field(default="", description="60-80 characters for mobile viewport")
    short_title: str = Field(default="", description="Standard e-commerce title")
    long_desc: str = Field(default="", description="Detailed narrative description")
    retail_bullet_points: List[str] = Field(default_factory=list, description="Key selling bullet points")


class ProductRecord(BaseModel):
    """Raw incoming product record from messy XLSX / CSV catalog."""
    row_id: str = Field(description="Unique row or SKU identifier")
    raw_mpn: Optional[str] = Field(default=None, alias="MPN")
    raw_manufacturer: Optional[str] = Field(default=None, alias="Manufacturer")
    raw_brand: Optional[str] = Field(default=None, alias="Brand")
    raw_description: Optional[str] = Field(default=None, alias="Description")
    raw_attributes: Dict[str, Any] = Field(default_factory=dict)


class EnrichedProductRecord(BaseModel):
    """Complete 12-layer enriched product deliverable."""
    row_id: str
    mpn: str
    canonical_manufacturer: str
    canonical_brand: Optional[str] = None
    manufacturer_domain: Optional[str] = None
    spec_source_url: Optional[str] = None

    # L2 Classification
    classification: Optional[Classpath] = None

    # L6 & L7 Attributes
    attributes: Dict[str, AttributeValue] = Field(default_factory=dict)

    # L8 Descriptions
    descriptions: ProductDescriptionSet = Field(default_factory=ProductDescriptionSet)

    # L9 Overall Status & Quality Scoring
    overall_confidence: float = 0.0
    overall_status: StatusTag = StatusTag.NEEDS_REVIEW
    provenance_coverage_pct: float = 0.0
    lov_conformance_pct: float = 0.0

    # L11 Assets
    verified_image_urls: List[str] = Field(default_factory=list)
    spec_sheet_pdf_urls: List[str] = Field(default_factory=list)

    # Audit Trail
    audit_trail: List[str] = Field(default_factory=list)


class PipelineResult(BaseModel):
    """Aggregate result from executing the UniHAP enrichment pipeline."""
    total_processed: int = 0
    auto_approved_count: int = 0
    needs_review_count: int = 0
    rejected_count: int = 0
    records: List[EnrichedProductRecord] = Field(default_factory=list)
    execution_time_seconds: float = 0.0
