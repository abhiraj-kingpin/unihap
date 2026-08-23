import { ExternalLink, Quote } from "lucide-react";
import { ConfidenceMeter } from "@/components/common/confidence-meter";
import { Disclosure, DisclosureButton, DisclosurePanel } from "@/components/ui/disclosure";
import type { AttributeOut } from "@/types";

export function AttributeRow({ attribute }: { attribute: AttributeOut }) {
  const evidence = attribute.evidence;

  if (!evidence) {
    return (
      <div className="flex items-center gap-4 border-b border-border px-4 py-3 last:border-0">
        <div className="min-w-0 flex-1">
          <p className="text-xs font-semibold uppercase tracking-wide text-text-muted">{attribute.name}</p>
          <p className="text-sm italic text-text-faint">abstained — no evidence</p>
        </div>
        <ConfidenceMeter confidence={attribute.confidence} />
      </div>
    );
  }

  return (
    <Disclosure>
      <div className="border-b border-border px-4 py-3 last:border-0">
        <DisclosureButton>
          <div className="flex flex-1 items-center gap-4">
            <div className="min-w-0 flex-1 text-left">
              <p className="text-xs font-semibold uppercase tracking-wide text-text-muted">{attribute.name}</p>
              <p className="truncate text-sm text-text-primary">
                {attribute.normalized_value}
                {attribute.uom && <span className="ml-1 text-text-muted">{attribute.uom}</span>}
              </p>
            </div>
            <Quote size={13} className="shrink-0 text-text-faint" />
            <ConfidenceMeter confidence={attribute.confidence} />
          </div>
        </DisclosureButton>
        <DisclosurePanel className="pt-3">
          <div className="rounded-lg border border-border bg-bg-subtle p-3">
            <p className="border-l-2 border-brand/40 pl-3 text-sm italic text-text-muted">
              &ldquo;{evidence.exact_text_span}&rdquo;
            </p>
            <div className="mt-2 flex items-center justify-between gap-3 text-xs text-text-faint">
              <a
                href={evidence.source_url}
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center gap-1 truncate text-brand-text hover:underline"
              >
                {evidence.source_url}
                <ExternalLink size={11} />
              </a>
              <span className="shrink-0 font-mono uppercase">{evidence.retrieval_method}</span>
            </div>
          </div>
        </DisclosurePanel>
      </div>
    </Disclosure>
  );
}
