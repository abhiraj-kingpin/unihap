"use client";

import { motion } from "framer-motion";
import { ChevronDown } from "lucide-react";
import { createContext, useContext, useId, useState } from "react";
import { DURATION, EASE_OUT } from "@/lib/animations";
import { cn } from "@/lib/utils";

interface DisclosureContextValue {
  open: boolean;
  toggle: () => void;
  panelId: string;
}

const DisclosureContext = createContext<DisclosureContextValue | null>(null);

function useDisclosureContext() {
  const context = useContext(DisclosureContext);
  if (!context) throw new Error("Disclosure.* components must be used within <Disclosure>");
  return context;
}

export function Disclosure({
  defaultOpen = false,
  children,
}: {
  defaultOpen?: boolean;
  children: React.ReactNode;
}) {
  const [open, setOpen] = useState(defaultOpen);
  const panelId = useId();

  return (
    <DisclosureContext.Provider value={{ open, toggle: () => setOpen((v) => !v), panelId }}>
      {children}
    </DisclosureContext.Provider>
  );
}

export function DisclosureButton({ children, className }: { children: React.ReactNode; className?: string }) {
  const { open, toggle, panelId } = useDisclosureContext();

  return (
    <button
      type="button"
      onClick={toggle}
      aria-expanded={open}
      aria-controls={panelId}
      className={cn(
        "flex w-full cursor-pointer items-center justify-between gap-3 text-left focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand/40",
        className,
      )}
    >
      {children}
      <motion.span animate={{ rotate: open ? 180 : 0 }} transition={{ duration: DURATION.fast }}>
        <ChevronDown size={16} className="text-text-muted" />
      </motion.span>
    </button>
  );
}

export function DisclosurePanel({ children, className }: { children: React.ReactNode; className?: string }) {
  const { open, panelId } = useDisclosureContext();

  return (
    <motion.div
      id={panelId}
      initial={false}
      animate={{ height: open ? "auto" : 0, opacity: open ? 1 : 0 }}
      transition={{ duration: DURATION.base, ease: EASE_OUT }}
      className="overflow-hidden"
    >
      <div className={className}>{children}</div>
    </motion.div>
  );
}
