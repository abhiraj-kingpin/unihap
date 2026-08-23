import type { Variants } from "framer-motion";

export const EASE_OUT = [0.4, 0, 0.2, 1] as const;

export const DURATION = {
  fast: 0.15,
  base: 0.25,
  slow: 0.4,
  scroll: 0.8,
} as const;

export const HOVER_SCALE = 1.03;
export const TAP_SCALE = 0.98;

export const viewportDefault = { once: true, amount: 0.3 } as const;

export const fadeIn: Variants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { duration: DURATION.scroll, ease: EASE_OUT } },
};

export const fadeInUp: Variants = {
  hidden: { opacity: 0, y: 24 },
  visible: { opacity: 1, y: 0, transition: { duration: DURATION.scroll, ease: EASE_OUT } },
};

export const fadeInScale: Variants = {
  hidden: { opacity: 0, scale: 0.95 },
  visible: { opacity: 1, scale: 1, transition: { duration: DURATION.scroll, ease: EASE_OUT } },
};

export const slideInLeft: Variants = {
  hidden: { opacity: 0, x: -40 },
  visible: { opacity: 1, x: 0, transition: { duration: DURATION.scroll, ease: EASE_OUT } },
};

const MAX_TOTAL_STAGGER_SECONDS = 0.4;
const DEFAULT_STAGGER_MS = 100;

export function buildStagger(itemCount: number, baseStaggerMs = DEFAULT_STAGGER_MS): Variants {
  const capped = Math.min(baseStaggerMs, (MAX_TOTAL_STAGGER_SECONDS * 1000) / Math.max(itemCount, 1));
  return {
    hidden: {},
    visible: {
      transition: {
        staggerChildren: capped / 1000,
      },
    },
  };
}

export const staggerItem: Variants = {
  hidden: { opacity: 0, y: 14 },
  visible: { opacity: 1, y: 0, transition: { duration: DURATION.scroll, ease: EASE_OUT } },
};
