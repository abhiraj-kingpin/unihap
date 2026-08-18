import { Chip } from "@/components/ui/chip";
import { FILTER_TABS } from "@/lib/status";
import type { CatalogFilterStatus } from "@/types";

interface StatusFilterChipsProps {
  value: CatalogFilterStatus;
  onChange: (value: CatalogFilterStatus) => void;
}

export function StatusFilterChips({ value, onChange }: StatusFilterChipsProps) {
  return (
    <div className="flex flex-wrap gap-2" role="group" aria-label="Filter by status">
      {FILTER_TABS.map((tab) => (
        <Chip key={tab.value} active={value === tab.value} aria-pressed={value === tab.value} onClick={() => onChange(tab.value)}>
          {tab.label}
        </Chip>
      ))}
    </div>
  );
}
