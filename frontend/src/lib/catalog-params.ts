import { DEFAULT_PAGE_SIZE } from "@/lib/constants";
import type { CatalogFilterStatus, ListProductsParams } from "@/types";

export function parseListParams(get: (key: string) => string | null, defaultLimit = DEFAULT_PAGE_SIZE): ListProductsParams {
  const page = Number(get("page")) || 1;
  const limit = Number(get("limit")) || defaultLimit;
  const status = (get("status") as CatalogFilterStatus | null) ?? "all";
  const search = get("search") ?? "";
  const sort = get("sort") ?? "confidence_desc";
  return { page, limit, status, search, sort };
}
