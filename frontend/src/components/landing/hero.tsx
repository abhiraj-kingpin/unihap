"use client";

import { motion } from "framer-motion";
import { ArrowRight, ShieldCheck } from "lucide-react";
import Link from "next/link";
import { HeroParallaxBg } from "@/components/landing/hero-parallax-bg";
import { buttonVariants } from "@/components/ui/button";
import { EASE_OUT } from "@/lib/animations";
import { cn } from "@/lib/utils";

export function Hero() {
  return (
    <section
      className="relative flex min-h-[92vh] flex-col items-center justify-center overflow-hidden px-6 text-center"
      style={{ background: "linear-gradient(135deg, #f8fbff 0%, #ffffff 50%, #f0f7ff 100%)" }}
    >
      <HeroParallaxBg />

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, ease: EASE_OUT }}
        className="relative z-10 mb-6 inline-flex items-center gap-2 rounded-full border border-brand/30 bg-brand-bg px-4 py-1.5 text-xs font-semibold uppercase tracking-[0.2em] text-brand-text"
      >
        <ShieldCheck size={13} />
        Evidence-Based Product Curation
      </motion.div>

      <motion.h1
        initial={{ opacity: 0, y: 28 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.7, delay: 0.1, ease: EASE_OUT }}
        className="relative z-10 max-w-4xl text-[40px] font-extrabold leading-[1.1] tracking-[-0.8px] text-text-primary sm:text-[56px]"
      >
        Review AI-enriched product data with total confidence
      </motion.h1>

      <motion.p
        initial={{ opacity: 0, y: 24 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.7, delay: 0.2, ease: EASE_OUT }}
        className="relative z-10 mt-6 max-w-xl text-base text-text-muted"
      >
        Every attribute traced to a citable source, or abstained entirely. UniHAP puts a human in the loop before
        anything ships.
      </motion.p>

      <motion.div
        initial={{ opacity: 0, y: 24 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.7, delay: 0.3, ease: EASE_OUT }}
        className="relative z-10 mt-10 flex flex-wrap items-center justify-center gap-4"
      >
        <Link href="/catalog" className={cn(buttonVariants({ variant: "primary", size: "lg" }))}>
          Browse Catalog
          <ArrowRight size={17} />
        </Link>
        <a href="#how-it-works" className={cn(buttonVariants({ variant: "outline", size: "lg" }))}>
          See How It Works
        </a>
      </motion.div>
    </section>
  );
}
