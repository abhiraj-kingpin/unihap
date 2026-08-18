"use client";

import { CheckCircle2, XCircle } from "lucide-react";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { useCuratorSettings } from "@/hooks/use-curator-settings";
import { useApproveProduct, useRejectProduct } from "@/hooks/use-product-mutations";

export function CurationPanel({ productId }: { productId: string }) {
  const router = useRouter();
  const [notes, setNotes] = useState("");
  const { curatorName } = useCuratorSettings();

  const approve = useApproveProduct();
  const reject = useRejectProduct();
  const pending = approve.isPending || reject.isPending;

  function handleApprove() {
    approve.mutate(
      { id: productId, curator: curatorName, notes: notes || undefined },
      { onSuccess: () => router.push("/catalog") },
    );
  }

  function handleReject() {
    reject.mutate(
      { id: productId, curator: curatorName, notes: notes || undefined },
      { onSuccess: () => router.push("/catalog") },
    );
  }

  return (
    <div className="flex flex-col gap-3 p-5">
      <label htmlFor="curation-notes" className="text-xs font-semibold uppercase tracking-wide text-text-muted">
        Notes <span className="normal-case font-normal text-text-faint">(optional)</span>
      </label>
      <textarea
        id="curation-notes"
        value={notes}
        onChange={(e) => setNotes(e.target.value)}
        placeholder="Add context for this decision…"
        rows={3}
        className="w-full resize-none rounded-lg border border-border bg-bg-subtle p-3 text-sm text-text-primary placeholder:text-text-faint focus-visible:border-brand focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand/30"
      />
      <div className="flex gap-2">
        <Button variant="primary" disabled={pending} onClick={handleApprove} className="flex-1">
          <CheckCircle2 size={15} />
          Approve
        </Button>
        <Button variant="critical" disabled={pending} onClick={handleReject} className="flex-1">
          <XCircle size={15} />
          Reject
        </Button>
      </div>
    </div>
  );
}
