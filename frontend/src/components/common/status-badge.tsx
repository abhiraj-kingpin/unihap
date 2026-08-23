import { Badge } from "@/components/ui/badge";
import { statusConfigFor } from "@/lib/status";
import type { BackendStatus } from "@/types";

const TONE_MAP: Record<BackendStatus, "approved" | "pending" | "rejected" | "neutral"> = {
  "auto-approved": "approved",
  "needs-review": "pending",
  rejected: "rejected",
  abstained: "neutral",
};

export function StatusBadge({ status }: { status: string }) {
  const config = statusConfigFor(status);
  const Icon = config.icon;
  const tone = TONE_MAP[status as BackendStatus] ?? "neutral";

  return (
    <Badge tone={tone}>
      <Icon size={12} strokeWidth={2.5} />
      {config.label}
    </Badge>
  );
}
