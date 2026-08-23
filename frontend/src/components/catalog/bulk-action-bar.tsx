"use client";

import { AnimatePresence, motion } from "framer-motion";
import { CheckCircle2, X, XCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useCuratorSettings } from "@/hooks/use-curator-settings";
import { useBulkAction } from "@/hooks/use-product-mutations";
import { DURATION, EASE_OUT } from "@/lib/animations";

interface BulkActionBarProps {
  selectedIds: string[];
  onClear: () => void;
}

export function BulkActionBar({ selectedIds, onClear }: BulkActionBarProps) {
  const { curatorName } = useCuratorSettings();
  const bulkAction = useBulkAction();

  function handleAction(action: "approve" | "reject") {
    bulkAction.mutate(
      { product_ids: selectedIds, action, curator: curatorName },
      { onSuccess: onClear },
    );
  }

  return (
    <AnimatePresence>
      {selectedIds.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: -12 }}
          animate={{ opacity: 1, y: 0, transition: { duration: DURATION.base, ease: EASE_OUT } }}
          exit={{ opacity: 0, y: -12, transition: { duration: DURATION.fast } }}
          className="flex items-center justify-between gap-4 rounded-xl border border-brand/30 bg-brand-bg px-4 py-3"
        >
          <span className="text-sm font-semibold text-brand-text">{selectedIds.length} selected</span>
          <div className="flex items-center gap-2">
            <Button variant="primary" size="sm" disabled={bulkAction.isPending} onClick={() => handleAction("approve")}>
              <CheckCircle2 size={14} />
              Approve All
            </Button>
            <Button variant="critical" size="sm" disabled={bulkAction.isPending} onClick={() => handleAction("reject")}>
              <XCircle size={14} />
              Reject All
            </Button>
            <Button variant="ghost" size="sm" disabled={bulkAction.isPending} onClick={onClear}>
              <X size={14} />
              Clear
            </Button>
          </div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
