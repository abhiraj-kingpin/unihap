import { forwardRef } from "react";
import { cn } from "@/lib/utils";

export const Select = forwardRef<HTMLSelectElement, React.SelectHTMLAttributes<HTMLSelectElement>>(
  ({ className, ...props }, ref) => {
    return (
      <select
        ref={ref}
        className={cn(
          "h-11 cursor-pointer rounded-lg border border-border bg-bg px-3 text-sm font-medium text-text-primary transition-colors focus-visible:border-brand focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand/30",
          className,
        )}
        {...props}
      />
    );
  },
);
Select.displayName = "Select";
