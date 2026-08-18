import { SkipLink } from "@/components/common/skip-link";
import { Footer } from "@/components/layout/footer";
import { Header } from "@/components/layout/header";

export function PageShell({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex min-h-screen flex-col bg-bg">
      <SkipLink />
      <Header />
      <main id="main-content" className="mx-auto w-full max-w-6xl flex-1 px-6 py-10">
        {children}
      </main>
      <Footer />
    </div>
  );
}
