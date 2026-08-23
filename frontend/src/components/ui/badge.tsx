import { type VariantProps, cva } from "class-variance-authority";
import { cn } from "@/lib/utils";

export const badgeVariants = cva("inline-flex items-center gap-1.5 rounded-full border px-2.5 py-1 text-xs font-semibold", {
  variants: {
    tone: {
      approved: "border-status-approved/40 bg-status-approved-bg text-status-approved-text",
      pending: "border-status-pending/40 bg-status-pending-bg text-status-pending-text",
      rejected: "border-status-rejected/40 bg-status-rejected-bg text-status-rejected-text",
      neutral: "border-status-neutral/40 bg-status-neutral-bg text-status-neutral-text",
    },
  },
  defaultVariants: { tone: "neutral" },
});

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement>, VariantProps<typeof badgeVariants> {}

export function Badge({ className, tone, ...props }: BadgeProps) {
  return <span className={cn(badgeVariants({ tone }), className)} {...props} />;
}
