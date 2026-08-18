import { Activity, ListChecks, ScanSearch, Table2, type LucideIcon } from "lucide-react";
import { ScrollReveal } from "@/components/common/scroll-reveal";

interface ShowcaseItem {
  icon: LucideIcon;
  title: string;
  description: string;
}

const ITEMS: ShowcaseItem[] = [
  {
    icon: Table2,
    title: "Catalog",
    description: "A searchable, filterable, sortable view of every product moving through the pipeline.",
  },
  {
    icon: ScanSearch,
    title: "Inspector",
    description: "Side-by-side view of every attribute alongside its exact source citation.",
  },
  {
    icon: ListChecks,
    title: "Bulk Actions",
    description: "Approve or reject entire batches of high-confidence records in a single action.",
  },
  {
    icon: Activity,
    title: "Metrics",
    description: "Live counts of approved, pending, and rejected records across the catalog.",
  },
];

export function FeatureShowcase() {
  return (
    <section className="bg-bg-subtle py-24">
      <div className="mx-auto max-w-6xl px-6">
        <ScrollReveal className="mb-12 max-w-xl">
          <h2 className="text-[32px] font-bold leading-tight text-text-primary sm:text-[42px]">
            Everything a curator needs, in one place
          </h2>
        </ScrollReveal>

        <ScrollReveal>
          <div className="grid grid-cols-1 gap-5 sm:grid-cols-2">
            {ITEMS.map(({ icon: Icon, title, description }) => (
              <div
                key={title}
                className="flex items-start gap-4 rounded-2xl border border-border bg-bg p-6 shadow-card"
              >
                <span className="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-brand-bg">
                  <Icon size={20} className="text-brand-text" strokeWidth={2.25} />
                </span>
                <div>
                  <h3 className="text-base font-bold text-text-primary">{title}</h3>
                  <p className="mt-1.5 text-sm leading-relaxed text-text-muted">{description}</p>
                </div>
              </div>
            ))}
          </div>
        </ScrollReveal>
      </div>
    </section>
  );
}
