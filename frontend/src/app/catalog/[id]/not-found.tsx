import { PackageX } from "lucide-react";
import Link from "next/link";
import { EmptyState } from "@/components/common/empty-state";
import { PageShell } from "@/components/layout/page-shell";
import { buttonVariants } from "@/components/ui/button";
import { cn } from "@/lib/utils";

export default function ProductNotFound() {
  return (
    <PageShell>
      <EmptyState icon={PackageX} title="Record not found" description="This product may have been removed or the ID is incorrect." />
      <div className="mt-6 flex justify-center">
        <Link href="/catalog" className={cn(buttonVariants({ variant: "outline" }))}>
          Back to Catalog
        </Link>
      </div>
    </PageShell>
  );
}
