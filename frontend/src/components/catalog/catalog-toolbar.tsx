"use client";

import { StatusFilterChips } from "@/components/catalog/status-filter-chips";
import { SearchInput } from "@/components/common/search-input";
import { Select } from "@/components/ui/select";
import { SORT_OPTIONS } from "@/lib/constants";
import type { CatalogFilterStatus } from "@/types";

interface CatalogToolbarProps {
  search: string;
  onSearchChange: (value: string) => void;
  status: CatalogFilterStatus;
  onStatusChange: (value: CatalogFilterStatus) => void;
  sort: string;
  onSortChange: (value: string) => void;
}

export function CatalogToolbar({ search, onSearchChange, status, onStatusChange, sort, onSortChange }: CatalogToolbarProps) {
  return (
    <div className="flex flex-col gap-4">
      <div className="flex flex-wrap items-center gap-3">
        <SearchInput
          value={search}
          onChange={onSearchChange}
          label="Search catalog"
          placeholder="Search by SKU, name, or brand…"
          className="min-w-[240px] flex-1"
        />
        <Select value={sort} onChange={(e) => onSortChange(e.target.value)} aria-label="Sort products">
          {SORT_OPTIONS.map((option) => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </Select>
      </div>
      <StatusFilterChips value={status} onChange={onStatusChange} />
    </div>
  );
}
