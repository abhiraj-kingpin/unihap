"use client";

import { motion, type Variants } from "framer-motion";
import { fadeInUp, viewportDefault } from "@/lib/animations";
import { cn } from "@/lib/utils";

interface ScrollRevealProps {
  children: React.ReactNode;
  variants?: Variants;
  delay?: number;
  className?: string;
}

export function ScrollReveal({ children, variants = fadeInUp, delay = 0, className }: ScrollRevealProps) {
  return (
    <motion.div
      variants={variants}
      initial="hidden"
      whileInView="visible"
      viewport={viewportDefault}
      transition={{ delay }}
      className={cn(className)}
    >
      {children}
    </motion.div>
  );
}
