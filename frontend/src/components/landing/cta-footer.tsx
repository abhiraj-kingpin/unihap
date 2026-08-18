import { ArrowRight } from "lucide-react";
import Link from "next/link";
import { ScrollReveal } from "@/components/common/scroll-reveal";
import { buttonVariants } from "@/components/ui/button";
import { cn } from "@/lib/utils";

export function CtaFooter() {
  return (
    <section className="px-6 py-24">
      <ScrollReveal>
        <div
          className="mx-auto max-w-4xl rounded-3xl px-8 py-16 text-center"
          style={{ background: "linear-gradient(135deg, var(--color-brand), var(--color-text-primary))" }}
        >
          <h2 className="text-[32px] font-extrabold leading-tight text-white sm:text-[42px]">
            Start reviewing the catalog
          </h2>
          <p className="mx-auto mt-3 max-w-md text-base font-medium text-white/85">
            Every record is one click away from an evidence-backed decision.
          </p>
          <Link
            href="/catalog"
            className={cn(
              buttonVariants({ variant: "primary", size: "lg" }),
              "mt-8 bg-white text-brand-text shadow-none hover:-translate-y-0.5 hover:bg-white hover:brightness-105",
            )}
          >
            Open Catalog
            <ArrowRight size={17} />
          </Link>
        </div>
      </ScrollReveal>
    </section>
  );
}
