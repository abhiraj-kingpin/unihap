import { DEFAULT_PAGE_SIZE } from "@/lib/constants";
import type { CatalogFilterStatus, ListProductsParams } from "@/types";

const VALID_STATUSES: CatalogFilterStatus[] = ["all", "auto-approved", "needs-review", "rejected"];
const MAX_LIMIT = 500;

function parsePositiveInt(raw: string | null, fallback: number, max?: number): number {
  const parsed = Number(raw);
  if (!Number.isInteger(parsed) || parsed < 1) return fallback;
  return max ? Math.min(parsed, max) : parsed;
}

export function parseListParams(get: (key: string) => string | null, defaultLimit = DEFAULT_PAGE_SIZE): ListProductsParams {
  const page = parsePositiveInt(get("page"), 1);
  const limit = parsePositiveInt(get("limit"), defaultLimit, MAX_LIMIT);
  const rawStatus = get("status");
  const status = VALID_STATUSES.includes(rawStatus as CatalogFilterStatus) ? (rawStatus as CatalogFilterStatus) : "all";
  const search = get("search") ?? "";
  const sort = get("sort") ?? "confidence_desc";
  return { page, limit, status, search, sort };
}
