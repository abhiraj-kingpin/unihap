import type { LucideIcon } from "lucide-react";
import { cn } from "@/lib/utils";

interface StatCardProps {
  label: string;
  value: React.ReactNode;
  icon?: LucideIcon;
  className?: string;
}

export function StatCard({ label, value, icon: Icon, className }: StatCardProps) {
  return (
    <div className={cn("rounded-xl border border-border bg-bg-subtle px-4 py-3.5", className)}>
      <div className="flex items-center justify-between gap-2">
        <p className="text-xs font-semibold uppercase tracking-[0.14em] text-text-muted">{label}</p>
        {Icon && <Icon size={15} className="text-brand-text" strokeWidth={2.25} />}
      </div>
      <p className="mt-1.5 font-mono text-lg font-semibold tabular text-text-primary">{value}</p>
    </div>
  );
}
