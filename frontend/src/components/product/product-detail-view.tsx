"use client";

import { ArrowLeft } from "lucide-react";
import Link from "next/link";
import { AttributesTable } from "@/components/product/attributes-table";
import { AuditTrail } from "@/components/product/audit-trail";
import { CurationPanel } from "@/components/product/curation-panel";
import { DescriptionTabs } from "@/components/product/description-tabs";
import { SourcePanel } from "@/components/product/source-panel";
import { StatStrip } from "@/components/product/stat-strip";
import { ScrollReveal } from "@/components/common/scroll-reveal";
import { ConfidenceMeter } from "@/components/common/confidence-meter";
import { StatusBadge } from "@/components/common/status-badge";
import { ErrorState } from "@/components/common/error-state";
import { Card, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { useProductQuery } from "@/hooks/use-products";

export function ProductDetailView({ productId }: { productId: string }) {
  const { data: product, isLoading, isError } = useProductQuery(productId);

  return (
    <div>
      <Link
        href="/catalog"
        className="mb-6 inline-flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wide text-text-muted transition-colors hover:text-brand-text"
      >
        <ArrowLeft size={13} />
        Back to Catalog
      </Link>

      {isError ? (
        <ErrorState title="Couldn't load this record" description={`Record "${productId}" may not exist, or the API is unreachable.`} />
      ) : isLoading || !product ? (
        <div className="space-y-4">
          <Skeleton className="h-10 w-64" />
          <Skeleton className="h-64 w-full" />
        </div>
      ) : (
        <>
          <ScrollReveal className="mb-6 flex flex-wrap items-start justify-between gap-4">
            <div>
              <h1 className="text-[28px] font-bold text-text-primary">{product.name}</h1>
              <p className="font-mono text-xs text-text-faint">
                {product.sku} · {product.classpath}
              </p>
            </div>
            <div className="flex items-center gap-2">
              <StatusBadge status={product.status} />
              <ConfidenceMeter confidence={product.confidence} />
            </div>
          </ScrollReveal>

          <div className="mb-6">
            <StatStrip product={product} />
          </div>

          <div className="grid grid-cols-1 gap-6 xl:grid-cols-[1.6fr_1fr]">
            <div className="flex flex-col gap-6">
              <ScrollReveal>
                <Card>
                  <CardHeader>
                    <CardTitle>Enriched Attributes</CardTitle>
                  </CardHeader>
                  <AttributesTable attributes={product.attributes} />
                </Card>
              </ScrollReveal>

              <ScrollReveal delay={0.05}>
                <Card>
                  <CardHeader>
                    <CardTitle>Description Formats</CardTitle>
                  </CardHeader>
                  <DescriptionTabs descriptions={product.descriptions} />
                </Card>
              </ScrollReveal>
            </div>

            <div className="flex flex-col gap-6">
              <ScrollReveal delay={0.05}>
                <Card>
                  <CardHeader>
                    <CardTitle>Source &amp; Discovery</CardTitle>
                  </CardHeader>
                  <SourcePanel product={product} />
                </Card>
              </ScrollReveal>

              <ScrollReveal delay={0.1}>
                <Card>
                  <CardHeader>
                    <CardTitle>Curator Action</CardTitle>
                  </CardHeader>
                  <CurationPanel productId={product.id} />
                </Card>
              </ScrollReveal>

              <ScrollReveal delay={0.15}>
                <Card>
                  <AuditTrail entries={product.audit_trail} />
                </Card>
              </ScrollReveal>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
