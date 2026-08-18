"use client";

import { useLiveAnnouncer } from "@/components/common/live-region";
import { Select } from "@/components/ui/select";
import { useCuratorSettings } from "@/hooks/use-curator-settings";
import { PAGE_SIZE_OPTIONS } from "@/lib/constants";

export function PageSizePreference() {
  const { defaultPageSize, setDefaultPageSize } = useCuratorSettings();
  const announce = useLiveAnnouncer();

  return (
    <div className="flex flex-col gap-3 p-5">
      <label htmlFor="default-page-size" className="text-xs font-semibold uppercase tracking-wide text-text-muted">
        Default Catalog Page Size
      </label>
      <p className="-mt-2 text-sm text-text-faint">Applied the next time you open the catalog.</p>
      <Select
        id="default-page-size"
        value={defaultPageSize}
        onChange={(e) => {
          const next = Number(e.target.value);
          setDefaultPageSize(next);
          announce(`Default page size set to ${next}.`);
        }}
        className="w-40"
      >
        {PAGE_SIZE_OPTIONS.map((size) => (
          <option key={size} value={size}>
            {size} rows
          </option>
        ))}
      </Select>
    </div>
  );
}
