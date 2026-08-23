import { cn } from "@/lib/utils";

interface ChipProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  active?: boolean;
}

export function Chip({ className, active, ...props }: ChipProps) {
  return (
    <button
      type="button"
      className={cn(
        "flex cursor-pointer items-center gap-2 rounded-full border px-4 py-2 text-sm font-semibold transition-colors",
        active
          ? "border-brand bg-brand-bg text-brand-text"
          : "border-border text-text-muted hover:border-brand/40 hover:text-text-primary",
        className,
      )}
      {...props}
    />
  );
}
