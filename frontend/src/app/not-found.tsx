import { Compass } from "lucide-react";
import Link from "next/link";
import { EmptyState } from "@/components/common/empty-state";
import { PageShell } from "@/components/layout/page-shell";
import { buttonVariants } from "@/components/ui/button";
import { cn } from "@/lib/utils";

export default function NotFound() {
  return (
    <PageShell>
      <EmptyState icon={Compass} title="Page not found" description="The page you're looking for doesn't exist." />
      <div className="mt-6 flex justify-center">
        <Link href="/" className={cn(buttonVariants({ variant: "outline" }))}>
          Back to Home
        </Link>
      </div>
    </PageShell>
  );
}
