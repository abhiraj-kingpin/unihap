"use client";

import { flexRender, getCoreRowModel, useReactTable } from "@tanstack/react-table";
import { motion } from "framer-motion";
import { PackageSearch } from "lucide-react";
import { useMemo } from "react";
import { EmptyState } from "@/components/common/empty-state";
import { buildColumns } from "@/components/catalog/product-table-columns";
import { buildStagger, staggerItem } from "@/lib/animations";
import type { ProductSummary } from "@/types";

interface ProductTableProps {
  items: ProductSummary[];
  selected: Set<string>;
  onToggleRow: (id: string) => void;
  onToggleAll: () => void;
  revealKey: string;
}

export function ProductTable({ items, selected, onToggleRow, onToggleAll, revealKey }: ProductTableProps) {
  const allSelected = items.length > 0 && items.every((item) => selected.has(item.id));

  const columns = useMemo(
    () => buildColumns({ selected, allSelected, onToggleRow, onToggleAll }),
    [selected, allSelected, onToggleRow, onToggleAll],
  );

  const table = useReactTable({ data: items, columns, getCoreRowModel: getCoreRowModel() });

  if (items.length === 0) {
    return <EmptyState icon={PackageSearch} title="No records match these filters" description="Try adjusting the search or status filter." />;
  }

  return (
    <div className="overflow-x-auto rounded-2xl border border-border">
      <table className="w-full min-w-[860px] border-collapse text-left">
        <thead>
          {table.getHeaderGroups().map((headerGroup) => (
            <tr key={headerGroup.id} className="border-b border-border bg-bg-subtle">
              {headerGroup.headers.map((header) => (
                <th key={header.id} className="whitespace-nowrap px-4 py-3 text-xs font-semibold uppercase tracking-wide text-text-muted">
                  {flexRender(header.column.columnDef.header, header.getContext())}
                </th>
              ))}
            </tr>
          ))}
        </thead>
        <motion.tbody
          key={revealKey}
          variants={buildStagger(table.getRowModel().rows.length)}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, amount: "some" }}
        >
          {table.getRowModel().rows.map((row) => (
            <motion.tr
              key={row.id}
              variants={staggerItem}
              whileHover={{ y: -1 }}
              transition={{ duration: 0.15 }}
              className="relative border-b border-border transition-colors last:border-0 hover:bg-bg-subtle"
            >
              {row.getVisibleCells().map((cell) => (
                <td key={cell.id} className="px-4 py-3">
                  {flexRender(cell.column.columnDef.cell, cell.getContext())}
                </td>
              ))}
            </motion.tr>
          ))}
        </motion.tbody>
      </table>
    </div>
  );
}
