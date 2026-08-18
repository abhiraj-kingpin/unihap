"use client";

import { motion } from "framer-motion";
import { buildStagger, slideInLeft, viewportDefault } from "@/lib/animations";

const STEPS = [
  { number: "01", title: "Browse", description: "Filter the catalog by status, confidence, or search for a SKU." },
  { number: "02", title: "Inspect", description: "Open a record to see every attribute next to its source citation." },
  { number: "03", title: "Decide", description: "Approve or reject with one click, and leave a note if it matters." },
  { number: "04", title: "Impact", description: "Your decision updates the catalog and the audit trail instantly." },
];

export function WorkflowTimeline() {
  return (
    <section id="how-it-works" className="bg-bg-subtle py-24">
      <div className="mx-auto max-w-6xl px-6">
        <div className="mb-14 max-w-xl">
          <h2 className="text-[32px] font-bold leading-tight text-text-primary sm:text-[42px]">How review works</h2>
          <p className="mt-3 text-base text-text-muted">Four steps between a raw record and a trusted one.</p>
        </div>

        <motion.ol
          variants={buildStagger(STEPS.length)}
          initial="hidden"
          whileInView="visible"
          viewport={viewportDefault}
          className="grid grid-cols-1 gap-8 sm:grid-cols-2 lg:grid-cols-4"
        >
          {STEPS.map(({ number, title, description }) => (
            <motion.li key={number} variants={slideInLeft} className="relative">
              <span className="font-mono text-sm font-semibold text-brand-text">{number}</span>
              <h3 className="mt-2 text-lg font-bold text-text-primary">{title}</h3>
              <p className="mt-1.5 text-sm leading-relaxed text-text-muted">{description}</p>
            </motion.li>
          ))}
        </motion.ol>
      </div>
    </section>
  );
}
