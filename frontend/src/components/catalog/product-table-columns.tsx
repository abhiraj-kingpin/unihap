import { createColumnHelper } from "@tanstack/react-table";
import Link from "next/link";
import { ConfidenceMeter } from "@/components/common/confidence-meter";
import { StatusBadge } from "@/components/common/status-badge";
import { Checkbox } from "@/components/ui/checkbox";
import type { ProductSummary } from "@/types";

const columnHelper = createColumnHelper<ProductSummary>();

interface BuildColumnsArgs {
  selected: Set<string>;
  allSelected: boolean;
  onToggleRow: (id: string) => void;
  onToggleAll: () => void;
}

export function buildColumns({ selected, allSelected, onToggleRow, onToggleAll }: BuildColumnsArgs) {
  return [
    columnHelper.display({
      id: "select",
      header: () => <Checkbox checked={allSelected} onChange={onToggleAll} aria-label="Select all rows on this page" />,
      cell: ({ row }) => (
        <Checkbox
          checked={selected.has(row.original.id)}
          onChange={() => onToggleRow(row.original.id)}
          onClick={(e) => e.stopPropagation()}
          aria-label={`Select ${row.original.name}`}
          className="relative z-10"
        />
      ),
    }),
    columnHelper.accessor("name", {
      header: "Product",
      cell: ({ row }) => (
        <div className="min-w-0">
          <Link
            href={`/catalog/${row.original.id}`}
            className="static truncate text-sm font-semibold text-text-primary after:absolute after:inset-0 hover:text-brand-text"
          >
            {row.original.name}
          </Link>
          <p className="truncate font-mono text-xs text-text-faint">{row.original.sku}</p>
        </div>
      ),
    }),
    columnHelper.accessor("brand", {
      header: "Brand",
      cell: (info) => <span className="text-sm text-text-muted">{info.getValue()}</span>,
    }),
    columnHelper.accessor("classpath", {
      header: "Classification",
      cell: (info) => <span className="text-xs text-text-muted">{info.getValue()}</span>,
    }),
    columnHelper.accessor("confidence", {
      header: "Confidence",
      cell: (info) => <ConfidenceMeter confidence={info.getValue()} />,
    }),
    columnHelper.accessor("status", {
      header: "Status",
      cell: (info) => <StatusBadge status={info.getValue()} />,
    }),
    columnHelper.accessor("evidence_count", {
      header: "Evidence",
      cell: (info) => (
        <span className="font-mono tabular text-xs text-text-muted">
          {info.getValue()}/{info.row.original.attribute_count}
        </span>
      ),
    }),
  ];
}
