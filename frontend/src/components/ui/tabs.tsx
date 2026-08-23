"use client";

import { motion } from "framer-motion";
import { createContext, useContext, useId, useRef, useState } from "react";
import { DURATION } from "@/lib/animations";
import { cn } from "@/lib/utils";

interface TabsContextValue {
  activeId: string;
  setActiveId: (id: string) => void;
  idPrefix: string;
}

const TabsContext = createContext<TabsContextValue | null>(null);

function useTabsContext() {
  const context = useContext(TabsContext);
  if (!context) throw new Error("Tabs.* components must be used within <Tabs>");
  return context;
}

export function Tabs({
  defaultTabId,
  children,
  className,
}: {
  defaultTabId: string;
  children: React.ReactNode;
  className?: string;
}) {
  const [activeId, setActiveId] = useState(defaultTabId);
  const idPrefix = useId();

  return (
    <TabsContext.Provider value={{ activeId, setActiveId, idPrefix }}>
      <div className={className}>{children}</div>
    </TabsContext.Provider>
  );
}

export function TabList({ label, children }: { label: string; children: React.ReactNode }) {
  const ref = useRef<HTMLDivElement>(null);
  const { setActiveId } = useTabsContext();

  function handleKeyDown(event: React.KeyboardEvent) {
    const tabs = Array.from(ref.current?.querySelectorAll<HTMLElement>('[role="tab"]') ?? []);
    if (tabs.length === 0) return;

    const currentIndex = tabs.findIndex((tab) => tab === document.activeElement);
    let nextIndex = currentIndex;

    if (event.key === "ArrowRight") nextIndex = (currentIndex + 1) % tabs.length;
    else if (event.key === "ArrowLeft") nextIndex = (currentIndex - 1 + tabs.length) % tabs.length;
    else if (event.key === "Home") nextIndex = 0;
    else if (event.key === "End") nextIndex = tabs.length - 1;
    else return;

    event.preventDefault();
    const nextTab = tabs[nextIndex];
    nextTab.focus();
    const id = nextTab.dataset.tabId;
    if (id) setActiveId(id);
  }

  return (
    <div
      ref={ref}
      role="tablist"
      aria-label={label}
      onKeyDown={handleKeyDown}
      className="flex flex-wrap gap-1 border-b border-border px-2"
    >
      {children}
    </div>
  );
}

export function Tab({ id, children }: { id: string; children: React.ReactNode }) {
  const { activeId, setActiveId, idPrefix } = useTabsContext();
  const active = activeId === id;

  return (
    <button
      type="button"
      role="tab"
      data-tab-id={id}
      id={`${idPrefix}-tab-${id}`}
      aria-selected={active}
      aria-controls={`${idPrefix}-panel-${id}`}
      tabIndex={active ? 0 : -1}
      onClick={() => setActiveId(id)}
      className={cn(
        "-mb-px cursor-pointer border-b-2 px-3.5 py-2.5 text-sm font-semibold transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand/40",
        active
          ? "border-brand text-brand-text"
          : "border-transparent text-text-muted hover:text-text-primary",
      )}
    >
      {children}
    </button>
  );
}

export function TabPanel({ id, children }: { id: string; children: React.ReactNode }) {
  const { activeId, idPrefix } = useTabsContext();
  if (activeId !== id) return null;

  return (
    <motion.div
      role="tabpanel"
      id={`${idPrefix}-panel-${id}`}
      aria-labelledby={`${idPrefix}-tab-${id}`}
      tabIndex={0}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: DURATION.fast }}
      className="p-5 focus-visible:outline-none"
    >
      {children}
    </motion.div>
  );
}
