"use client";

import { motion } from "framer-motion";
import { CheckCircle2, Clock, Package, XCircle, type LucideIcon } from "lucide-react";
import { AnimatedCounter } from "@/components/common/animated-counter";
import { Skeleton } from "@/components/ui/skeleton";
import { useMetricsQuery } from "@/hooks/use-metrics";
import { buildStagger, EASE_OUT, staggerItem, viewportDefault } from "@/lib/animations";
import { cn } from "@/lib/utils";

interface MetricTile {
  label: string;
  value: number;
  icon: LucideIcon;
  tone: string;
  iconBg: string;
}

export function MetricsSection() {
  const { data, isLoading, isError } = useMetricsQuery();

  const tiles: MetricTile[] = [
    { label: "Total Products", value: data?.total_products ?? 0, icon: Package, tone: "text-text-primary", iconBg: "bg-bg-subtle" },
    {
      label: "Approved",
      value: data?.auto_approved_count ?? 0,
      icon: CheckCircle2,
      tone: "text-status-approved-text",
      iconBg: "bg-status-approved-bg",
    },
    {
      label: "Pending",
      value: data?.needs_review_count ?? 0,
      icon: Clock,
      tone: "text-status-pending-text",
      iconBg: "bg-status-pending-bg",
    },
    {
      label: "Rejected",
      value: data?.rejected_count ?? 0,
      icon: XCircle,
      tone: "text-status-rejected-text",
      iconBg: "bg-status-rejected-bg",
    },
  ];

  return (
    <section
      className="px-6 py-24"
      style={{ background: "linear-gradient(180deg, var(--color-bg) 0%, var(--color-brand-bg) 50%, var(--color-bg) 100%)" }}
    >
      <div className="mx-auto max-w-6xl">
        <div className="mb-12 max-w-xl">
          <h2 className="text-[32px] font-bold leading-tight text-text-primary sm:text-[42px]">
            The catalog, live right now
          </h2>
          <p className="mt-3 text-base text-text-muted">Pulled straight from the pipeline — no sampling, no delay.</p>
        </div>

        {isError ? (
          <p className="rounded-2xl border border-status-rejected/25 bg-status-rejected-bg px-6 py-10 text-center text-sm text-status-rejected-text">
            Metrics unavailable — start the backend to see live numbers.
          </p>
        ) : isLoading || !data ? (
          <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
            {Array.from({ length: 4 }).map((_, i) => (
              <Skeleton key={i} className="h-32" />
            ))}
          </div>
        ) : (
          <motion.div
            variants={buildStagger(tiles.length)}
            initial="hidden"
            whileInView="visible"
            viewport={viewportDefault}
            className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4"
          >
            {tiles.map(({ label, value, icon: Icon, tone, iconBg }) => (
              <motion.div
                key={label}
                variants={staggerItem}
                whileHover={{ scale: 1.05 }}
                transition={{ duration: 0.3, ease: EASE_OUT }}
                className="rounded-2xl border border-border bg-bg p-6 shadow-card"
              >
                <div className="flex items-center justify-between">
                  <p className="text-xs font-semibold uppercase tracking-[0.14em] text-text-muted">{label}</p>
                  <span className={cn("flex h-9 w-9 items-center justify-center rounded-lg", iconBg)}>
                    <Icon size={16} className={tone} strokeWidth={2.25} />
                  </span>
                </div>
                <div className={cn("mt-3 font-mono text-3xl font-semibold tabular", tone)}>
                  <AnimatedCounter value={value} />
                </div>
              </motion.div>
            ))}
          </motion.div>
        )}
      </div>
    </section>
  );
}
