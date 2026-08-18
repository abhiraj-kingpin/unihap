import { dehydrate, HydrationBoundary } from "@tanstack/react-query";
import type { Metadata } from "next";
import { Suspense } from "react";
import { CatalogView } from "@/components/catalog/catalog-view";
import { Skeleton } from "@/components/ui/skeleton";
import { PageShell } from "@/components/layout/page-shell";
import { api, productKeys } from "@/lib/api";
import { parseListParams } from "@/lib/catalog-params";
import { getQueryClient } from "@/lib/query-client";

export const metadata: Metadata = {
  title: "Catalog",
  description: "Browse, filter, and curate every product moving through the UniHAP pipeline.",
};

interface CatalogPageProps {
  searchParams: Promise<Record<string, string | string[] | undefined>>;
}

function CatalogSkeleton() {
  return (
    <div className="flex flex-col gap-6">
      <Skeleton className="h-9 w-48" />
      <Skeleton className="h-11 w-full" />
      {Array.from({ length: 6 }).map((_, i) => (
        <Skeleton key={i} className="h-14 w-full" />
      ))}
    </div>
  );
}

export default async function CatalogPage({ searchParams }: CatalogPageProps) {
  const resolved = await searchParams;
  const get = (key: string) => {
    const value = resolved[key];
    return Array.isArray(value) ? (value[0] ?? null) : (value ?? null);
  };
  const params = parseListParams(get);

  const queryClient = getQueryClient();
  await queryClient.prefetchQuery({ queryKey: productKeys.list(params), queryFn: () => api.listProducts(params) });

  return (
    <PageShell>
      <HydrationBoundary state={dehydrate(queryClient)}>
        <Suspense fallback={<CatalogSkeleton />}>
          <CatalogView />
        </Suspense>
      </HydrationBoundary>
    </PageShell>
  );
}
