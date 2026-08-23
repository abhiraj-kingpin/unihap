import { type VariantProps, cva } from "class-variance-authority";
import { forwardRef } from "react";
import { cn } from "@/lib/utils";

export const buttonVariants = cva(
  "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-lg text-sm font-semibold transition-all duration-300 ease-[cubic-bezier(0.4,0,0.2,1)] disabled:pointer-events-none disabled:opacity-40 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand focus-visible:ring-offset-2 focus-visible:ring-offset-bg cursor-pointer",
  {
    variants: {
      variant: {
        primary:
          "bg-brand text-white shadow-button hover:-translate-y-0.5 hover:bg-brand-hover hover:shadow-button-hover active:translate-y-0 active:scale-[0.98]",
        outline:
          "border border-brand/40 text-brand-text hover:-translate-y-0.5 hover:border-brand hover:bg-brand-bg active:translate-y-0 active:scale-[0.98]",
        ghost: "text-text-muted hover:text-text-primary hover:bg-bg-subtle active:scale-[0.98]",
        critical:
          "border border-status-rejected/40 text-status-rejected-text hover:-translate-y-0.5 hover:border-status-rejected hover:bg-status-rejected-bg active:translate-y-0 active:scale-[0.98]",
      },
      size: {
        sm: "h-10 px-3.5 text-xs",
        md: "h-12 px-5",
        lg: "h-14 px-7 text-base",
      },
    },
    defaultVariants: { variant: "primary", size: "md" },
  },
);

export interface ButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {}

export const Button = forwardRef<HTMLButtonElement, ButtonProps>(({ className, variant, size, ...props }, ref) => {
  return <button ref={ref} className={cn(buttonVariants({ variant, size }), className)} {...props} />;
});
Button.displayName = "Button";
