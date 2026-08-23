"use client";

import { motion } from "framer-motion";
import { FileSearch, ShieldCheck, Sparkles, type LucideIcon } from "lucide-react";
import { buildStagger, EASE_OUT, staggerItem, viewportDefault } from "@/lib/animations";

interface Feature {
  icon: LucideIcon;
  title: string;
  description: string;
}

const FEATURES: Feature[] = [
  {
    icon: Sparkles,
    title: "AI Enrichment",
    description: "A 12-layer pipeline classifies, normalizes, and describes every product from raw manufacturer data.",
  },
  {
    icon: FileSearch,
    title: "Evidence-Based",
    description: "Every attribute cites an exact source span from the manufacturer's own page — or abstains entirely.",
  },
  {
    icon: ShieldCheck,
    title: "Human Review",
    description: "Records below the confidence threshold route straight to a curator before anything ships.",
  },
];

export function FeatureCards() {
  return (
    <section className="mx-auto max-w-6xl px-6 py-24">
      <motion.div
        variants={buildStagger(FEATURES.length)}
        initial="hidden"
        whileInView="visible"
        viewport={viewportDefault}
        className="grid grid-cols-1 gap-6 md:grid-cols-3"
      >
        {FEATURES.map(({ icon: Icon, title, description }) => (
          <motion.div
            key={title}
            variants={staggerItem}
            whileHover={{ y: -6 }}
            transition={{ duration: 0.3, ease: EASE_OUT }}
            className="group relative overflow-hidden rounded-2xl border border-border bg-bg p-8 shadow-card transition-shadow duration-300 hover:shadow-card-hover"
          >
            <span className="absolute inset-x-0 top-0 h-[3px] origin-left scale-x-0 bg-gradient-to-r from-brand to-brand-hover transition-transform duration-300 ease-[cubic-bezier(0.4,0,0.2,1)] group-hover:scale-x-100" />
            <span className="flex h-11 w-11 items-center justify-center rounded-xl bg-brand-bg">
              <Icon size={20} className="text-brand-text" strokeWidth={2.25} />
            </span>
            <h3 className="mt-5 text-lg font-bold text-text-primary">{title}</h3>
            <p className="mt-2 text-sm leading-relaxed text-text-muted">{description}</p>
          </motion.div>
        ))}
      </motion.div>
    </section>
  );
}
