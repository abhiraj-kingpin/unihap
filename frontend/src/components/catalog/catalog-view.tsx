"use client";

import { usePathname, useRouter, useSearchParams } from "next/navigation";
import { useEffect, useMemo, useRef, useState } from "react";
import { BulkActionBar } from "@/components/catalog/bulk-action-bar";
import { CatalogToolbar } from "@/components/catalog/catalog-toolbar";
import { ProductTable } from "@/components/catalog/product-table";
import { ErrorState } from "@/components/common/error-state";
import { Pagination } from "@/components/common/pagination";
import { Skeleton } from "@/components/ui/skeleton";
import { useCuratorSettings } from "@/hooks/use-curator-settings";
import { useDebouncedValue } from "@/hooks/use-debounced-value";
import { useProductsQuery } from "@/hooks/use-products";
import { parseListParams } from "@/lib/catalog-params";
import { DEFAULT_PAGE_SIZE } from "@/lib/constants";
import type { CatalogFilterStatus } from "@/types";

const PARAM_DEFAULTS: Record<string, string> = { page: "1", status: "all" };

export function CatalogView() {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const { defaultPageSize } = useCuratorSettings();

  const params = useMemo(() => parseListParams((key) => searchParams.get(key)), [searchParams]);

  const [searchDraft, setSearchDraft] = useState(params.search ?? "");
  const debouncedSearch = useDebouncedValue(searchDraft, 300);
  const [selected, setSelected] = useState<Set<string>>(new Set());

  function updateParams(next: Record<string, string | number>) {
    const sp = new URLSearchParams(searchParams.toString());
    for (const [key, value] of Object.entries(next)) {
      const stringValue = String(value);
      if (stringValue === "" || stringValue === PARAM_DEFAULTS[key]) sp.delete(key);
      else sp.set(key, stringValue);
    }
    router.replace(`${pathname}?${sp.toString()}`, { scroll: false });
  }

  const updateParamsRef = useRef(updateParams);
  updateParamsRef.current = updateParams;

  useEffect(() => {
    if (!searchParams.get("limit") && defaultPageSize !== DEFAULT_PAGE_SIZE) {
      updateParamsRef.current({ limit: defaultPageSize });
    }
  }, [searchParams, defaultPageSize]);

  useEffect(() => {
    if (debouncedSearch !== (params.search ?? "")) {
      updateParamsRef.current({ search: debouncedSearch, page: 1 });
    }
  }, [debouncedSearch, params.search]);

  const query = useProductsQuery(params);

  function toggleRow(id: string) {
    setSelected((prev) => {
      const next = new Set(prev);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  }

  function toggleAll() {
    if (!query.data) return;
    const allIds = query.data.items.map((item) => item.id);
    setSelected((prev) => (allIds.every((id) => prev.has(id)) ? new Set() : new Set(allIds)));
  }

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-[32px] font-bold text-text-primary">Catalog</h1>
        <p className="mt-1 text-sm text-text-muted">
          {query.data ? `${query.data.total.toLocaleString()} records in the pipeline.` : "Loading records…"}
        </p>
      </div>

      <CatalogToolbar
        search={searchDraft}
        onSearchChange={setSearchDraft}
        status={params.status ?? "all"}
        onStatusChange={(status: CatalogFilterStatus) => updateParams({ status, page: 1 })}
        sort={params.sort ?? "confidence_desc"}
        onSortChange={(sort) => updateParams({ sort })}
      />

      <BulkActionBar selectedIds={Array.from(selected)} onClear={() => setSelected(new Set())} />

      {query.isError ? (
        <ErrorState
          title="Can't reach the UniHAP API"
          description="Start the backend so the catalog has live data to show."
          hint="uv run unihap api"
        />
      ) : query.isLoading || !query.data ? (
        <div className="space-y-2">
          {Array.from({ length: 6 }).map((_, i) => (
            <Skeleton key={i} className="h-14 w-full" />
          ))}
        </div>
      ) : (
        <>
          <ProductTable
            items={query.data.items}
            selected={selected}
            onToggleRow={toggleRow}
            onToggleAll={toggleAll}
            revealKey={`${params.page}-${params.limit}-${params.status}-${params.search}-${params.sort}`}
          />
          <Pagination
            page={query.data.page}
            limit={query.data.limit}
            total={query.data.total}
            hasNext={query.data.has_next}
            onPageChange={(page) => updateParams({ page })}
            onLimitChange={(limit) => updateParams({ limit, page: 1 })}
          />
        </>
      )}
    </div>
  );
}
