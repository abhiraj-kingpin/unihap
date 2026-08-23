import { dehydrate, HydrationBoundary } from "@tanstack/react-query";
import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { PageShell } from "@/components/layout/page-shell";
import { ProductDetailView } from "@/components/product/product-detail-view";
import { ApiError, api, productKeys } from "@/lib/api";
import { getQueryClient } from "@/lib/query-client";

interface ProductPageProps {
  params: Promise<{ id: string }>;
}

export async function generateMetadata({ params }: ProductPageProps): Promise<Metadata> {
  const { id } = await params;
  try {
    const product = await api.getProduct(id);
    return { title: product.name, description: `${product.sku} — ${product.classpath}` };
  } catch {
    return { title: "Record not found" };
  }
}

export default async function ProductPage({ params }: ProductPageProps) {
  const { id } = await params;
  const queryClient = getQueryClient();

  try {
    await queryClient.fetchQuery({ queryKey: productKeys.detail(id), queryFn: () => api.getProduct(id) });
  } catch (error) {
    if (error instanceof ApiError && error.status === 404) notFound();
  }

  return (
    <PageShell>
      <HydrationBoundary state={dehydrate(queryClient)}>
        <ProductDetailView productId={id} />
      </HydrationBoundary>
    </PageShell>
  );
}
