import Link from "next/link";

export function Footer() {
  return (
    <footer className="border-t border-border">
      <div className="mx-auto flex max-w-6xl flex-col items-center justify-between gap-3 px-6 py-8 text-sm text-text-muted sm:flex-row">
        <p>© {new Date().getFullYear()} UniHAP.</p>
        <div className="flex items-center gap-5">
          <Link href="/catalog" className="transition-colors hover:text-text-primary">
            Catalog
          </Link>
          <Link href="/settings" className="transition-colors hover:text-text-primary">
            Settings
          </Link>
        </div>
      </div>
    </footer>
  );
}
