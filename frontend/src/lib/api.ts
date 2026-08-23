import type {
  ApprovalRequest,
  BulkActionRequest,
  BulkActionResult,
  ListProductsParams,
  MetricsResponse,
  ProductDetail,
  ProductPage,
  ProductSummary,
} from "@/types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export class ApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

async function apiFetch<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...init?.headers,
    },
  });

  if (!response.ok) {
    const body = await response.text().catch(() => "");
    throw new ApiError(body || response.statusText, response.status);
  }

  return response.json() as Promise<T>;
}

function buildQuery(params: Record<string, string | number | undefined>): string {
  const search = new URLSearchParams();
  for (const [key, value] of Object.entries(params)) {
    if (value !== undefined && value !== "") search.set(key, String(value));
  }
  const query = search.toString();
  return query ? `?${query}` : "";
}

export const api = {
  listProducts(params: ListProductsParams): Promise<ProductPage> {
    const query = buildQuery({
      page: params.page,
      limit: params.limit,
      status: params.status && params.status !== "all" ? params.status : undefined,
      search: params.search || undefined,
      sort: params.sort,
    });
    return apiFetch<ProductPage>(`/api/v1/products${query}`);
  },

  getProduct(id: string): Promise<ProductDetail> {
    return apiFetch<ProductDetail>(`/api/v1/products/${encodeURIComponent(id)}`);
  },

  approveProduct(id: string, body: ApprovalRequest): Promise<ProductSummary> {
    return apiFetch<ProductSummary>(`/api/v1/products/${encodeURIComponent(id)}/approve`, {
      method: "POST",
      body: JSON.stringify(body),
    });
  },

  rejectProduct(id: string, body: ApprovalRequest): Promise<ProductSummary> {
    return apiFetch<ProductSummary>(`/api/v1/products/${encodeURIComponent(id)}/reject`, {
      method: "POST",
      body: JSON.stringify(body),
    });
  },

  bulkAction(body: BulkActionRequest): Promise<BulkActionResult> {
    return apiFetch<BulkActionResult>("/api/v1/products/bulk-action", {
      method: "POST",
      body: JSON.stringify(body),
    });
  },

  getMetrics(): Promise<MetricsResponse> {
    return apiFetch<MetricsResponse>("/api/v1/metrics");
  },
};

export const productKeys = {
  all: ["products"] as const,
  list: (params: ListProductsParams) => ["products", "list", params] as const,
  detail: (id: string) => ["products", "detail", id] as const,
};

export const metricsKeys = {
  all: ["metrics"] as const,
};
