import { ExternalLink } from "lucide-react";
import { ConfidenceMeter } from "@/components/common/confidence-meter";
import type { ProductDetail } from "@/types";

export function SourcePanel({ product }: { product: ProductDetail }) {
  return (
    <div className="flex flex-col gap-3 p-5 text-sm">
      <div className="flex items-center justify-between">
        <span className="text-text-muted">Domain</span>
        <span className="font-mono text-text-primary">{product.manufacturer_domain ?? "—"}</span>
      </div>
      <div className="flex items-center justify-between">
        <span className="text-text-muted">Manufacturer confidence</span>
        <ConfidenceMeter confidence={product.manufacturer_confidence} />
      </div>
      {product.spec_source_url && (
        <a
          href={product.spec_source_url}
          target="_blank"
          rel="noopener noreferrer"
          className="flex items-center gap-1.5 truncate text-xs font-medium text-brand-text hover:underline"
        >
          {product.spec_source_url}
          <ExternalLink size={11} />
        </a>
      )}
    </div>
  );
}
