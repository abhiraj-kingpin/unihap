"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { NAV_LINKS } from "@/lib/constants";
import { cn } from "@/lib/utils";

export function Header() {
  const pathname = usePathname();

  return (
    <header className="sticky top-0 z-40 border-b border-border bg-bg/90 backdrop-blur-sm" style={{ boxShadow: "var(--shadow-navbar)" }}>
      <div className="mx-auto flex h-16 max-w-6xl items-center justify-between px-5">
        <Link href="/" className="text-sm font-bold uppercase tracking-[0.3em] text-text-primary">
          Uni<span className="text-brand-text">HAP</span>
        </Link>
        <nav className="flex items-center gap-1">
          {NAV_LINKS.map(({ href, label }) => {
            const active = pathname === href || Boolean(pathname?.startsWith(`${href}/`));
            return (
              <Link
                key={href}
                href={href}
                aria-current={active ? "page" : undefined}
                className={cn(
                  "group relative rounded-lg px-3.5 py-2 text-sm font-semibold transition-colors",
                  active ? "bg-brand-bg text-brand-text" : "text-text-muted hover:text-text-primary",
                )}
              >
                {label}
                {!active && (
                  <span className="pointer-events-none absolute inset-x-3.5 bottom-1 h-[2px] origin-left scale-x-0 rounded-full bg-brand transition-transform duration-300 ease-[cubic-bezier(0.4,0,0.2,1)] group-hover:scale-x-100" />
                )}
              </Link>
            );
          })}
        </nav>
      </div>
    </header>
  );
}
