"use client";

import { ChevronLeft, ChevronRight } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Select } from "@/components/ui/select";
import { PAGE_SIZE_OPTIONS } from "@/lib/constants";

interface PaginationProps {
  page: number;
  limit: number;
  total: number;
  hasNext: boolean;
  onPageChange: (page: number) => void;
  onLimitChange: (limit: number) => void;
}

export function Pagination({ page, limit, total, hasNext, onPageChange, onLimitChange }: PaginationProps) {
  const totalPages = Math.max(Math.ceil(total / limit), 1);

  return (
    <div className="flex flex-wrap items-center justify-between gap-3 pt-2 text-sm text-text-muted">
      <span>
        Page <span className="font-mono tabular text-text-primary">{page}</span> of{" "}
        <span className="font-mono tabular text-text-primary">{totalPages}</span> ·{" "}
        <span className="font-mono tabular text-text-primary">{total.toLocaleString()}</span> records
      </span>

      <div className="flex items-center gap-3">
        <Select
          value={limit}
          onChange={(e) => onLimitChange(Number(e.target.value))}
          aria-label="Rows per page"
          className="h-9 text-xs"
        >
          {PAGE_SIZE_OPTIONS.map((size) => (
            <option key={size} value={size}>
              {size} / page
            </option>
          ))}
        </Select>

        <div className="flex items-center gap-1.5">
          <Button
            variant="ghost"
            size="sm"
            disabled={page <= 1}
            onClick={() => onPageChange(page - 1)}
            aria-label="Previous page"
          >
            <ChevronLeft size={14} />
          </Button>
          <Button
            variant="ghost"
            size="sm"
            disabled={!hasNext}
            onClick={() => onPageChange(page + 1)}
            aria-label="Next page"
          >
            <ChevronRight size={14} />
          </Button>
        </div>
      </div>
    </div>
  );
}
