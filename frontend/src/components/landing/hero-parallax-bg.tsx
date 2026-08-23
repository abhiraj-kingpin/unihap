"use client";

import { motion, useScroll, useTransform } from "framer-motion";
import { useRef } from "react";

export function HeroParallaxBg() {
  const ref = useRef<HTMLDivElement>(null);
  const { scrollYProgress } = useScroll({ target: ref, offset: ["start start", "end start"] });
  const y1 = useTransform(scrollYProgress, [0, 1], [0, 140]);
  const opacity = useTransform(scrollYProgress, [0, 1], [1, 0]);

  return (
    <div ref={ref} aria-hidden="true" className="pointer-events-none absolute inset-0 overflow-hidden">
      <motion.div
        style={{ y: y1, opacity }}
        className="absolute -left-24 top-10 h-72 w-72 rounded-full bg-brand/10 blur-[100px]"
      />
      <motion.div
        style={{
          opacity,
          background: "radial-gradient(circle at 50% 50%, rgba(59,130,246,0.28), rgba(59,130,246,0) 70%)",
        }}
        animate={{ y: [0, -18, 0] }}
        transition={{ duration: 8, repeat: Infinity, ease: "easeInOut" }}
        className="absolute -right-20 top-24 h-[420px] w-[420px] rounded-full blur-[70px]"
      />
    </div>
  );
}
