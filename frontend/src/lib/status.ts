import { CheckCircle2, CircleSlash, Clock, XCircle, type LucideIcon } from "lucide-react";
import type { BackendStatus, CatalogFilterStatus } from "@/types";

interface StatusConfig {
  label: string;
  icon: LucideIcon;
  text: string;
  bg: string;
  border: string;
  dot: string;
}

export const STATUS_CONFIG: Record<BackendStatus, StatusConfig> = {
  "auto-approved": {
    label: "Approved",
    icon: CheckCircle2,
    text: "text-status-approved-text",
    bg: "bg-status-approved-bg",
    border: "border-status-approved/40",
    dot: "bg-status-approved",
  },
  "needs-review": {
    label: "Pending",
    icon: Clock,
    text: "text-status-pending-text",
    bg: "bg-status-pending-bg",
    border: "border-status-pending/40",
    dot: "bg-status-pending",
  },
  rejected: {
    label: "Rejected",
    icon: XCircle,
    text: "text-status-rejected-text",
    bg: "bg-status-rejected-bg",
    border: "border-status-rejected/40",
    dot: "bg-status-rejected",
  },
  abstained: {
    label: "Abstained",
    icon: CircleSlash,
    text: "text-status-neutral-text",
    bg: "bg-status-neutral-bg",
    border: "border-status-neutral/40",
    dot: "bg-status-neutral",
  },
};

export function statusConfigFor(status: string): StatusConfig {
  return STATUS_CONFIG[status as BackendStatus] ?? STATUS_CONFIG.abstained;
}

export const FILTER_TABS: { value: CatalogFilterStatus; label: string }[] = [
  { value: "all", label: "All" },
  { value: "auto-approved", label: "Approved" },
  { value: "needs-review", label: "Pending" },
  { value: "rejected", label: "Rejected" },
];
