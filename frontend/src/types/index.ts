export type BackendStatus = "auto-approved" | "needs-review" | "rejected" | "abstained";

export type CatalogFilterStatus = "all" | "auto-approved" | "needs-review" | "rejected";

export interface EvidenceSpanOut {
  source_url: string;
  exact_text_span: string;
  retrieval_method: string;
  confidence_score: number;
}

export interface AttributeOut {
  name: string;
  raw_value: string | null;
  normalized_value: string | null;
  uom: string | null;
  in_lov: boolean;
  status: BackendStatus;
  confidence: number;
  evidence: EvidenceSpanOut | null;
}

export interface DescriptionSetOut {
  invoice_caps: string;
  mobile: string;
  short_title: string;
  long_desc: string;
  retail_bullet_points: string[];
}

export interface ProductSummary {
  id: string;
  sku: string;
  mpn: string;
  name: string;
  brand: string;
  manufacturer: string;
  classpath: string;
  department: string;
  confidence: number;
  status: BackendStatus;
  evidence_count: number;
  attribute_count: number;
  created_at: string;
  updated_at: string;
}

export interface ProductDetail extends ProductSummary {
  manufacturer_domain: string | null;
  spec_source_url: string | null;
  manufacturer_confidence: number;
  lov_conformance_pct: number;
  provenance_coverage_pct: number;
  attributes: AttributeOut[];
  descriptions: DescriptionSetOut;
  audit_trail: string[];
  approved_by: string | null;
  approval_notes: string | null;
}

export interface ProductPage {
  items: ProductSummary[];
  total: number;
  page: number;
  limit: number;
  has_next: boolean;
}

export interface TrendPoint {
  date: string;
  auto_approved_pct: number;
  total: number;
}

export interface MetricsResponse {
  total_products: number;
  auto_approved_count: number;
  auto_approved_pct: number;
  needs_review_count: number;
  needs_review_pct: number;
  rejected_count: number;
  rejected_pct: number;
  avg_confidence: number;
  avg_lov_conformance_pct: number;
  avg_provenance_coverage_pct: number;
  last_updated: string;
  trend: TrendPoint[];
}

export interface ApprovalRequest {
  curator: string;
  notes?: string;
}

export interface BulkActionRequest {
  product_ids: string[];
  action: "approve" | "reject";
  curator?: string;
  notes?: string;
}

export interface BulkActionResult {
  success_count: number;
  failed_count: number;
  results: ProductSummary[];
}

export interface ListProductsParams {
  page: number;
  limit: number;
  status?: CatalogFilterStatus;
  search?: string;
  sort?: string;
}
