"use client";

import { motion } from "framer-motion";
import { StatCard } from "@/components/ui/stat-card";
import { buildStagger, staggerItem, viewportDefault } from "@/lib/animations";
import { formatPct } from "@/lib/format";
import type { ProductDetail } from "@/types";

export function StatStrip({ product }: { product: ProductDetail }) {
  const stats = [
    { label: "Manufacturer", value: product.manufacturer },
    { label: "LOV Conformance", value: formatPct(product.lov_conformance_pct) },
    { label: "Provenance Coverage", value: formatPct(product.provenance_coverage_pct) },
    { label: "Evidence", value: `${product.evidence_count}/${product.attribute_count}` },
  ];

  return (
    <motion.div
      variants={buildStagger(stats.length)}
      initial="hidden"
      whileInView="visible"
      viewport={viewportDefault}
      className="grid grid-cols-2 gap-3 sm:grid-cols-4"
    >
      {stats.map((stat) => (
        <motion.div key={stat.label} variants={staggerItem}>
          <StatCard label={stat.label} value={stat.value} />
        </motion.div>
      ))}
    </motion.div>
  );
}
