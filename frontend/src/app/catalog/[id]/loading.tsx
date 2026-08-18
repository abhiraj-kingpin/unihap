import { PageShell } from "@/components/layout/page-shell";
import { Skeleton } from "@/components/ui/skeleton";

export default function Loading() {
  return (
    <PageShell>
      <Skeleton className="mb-6 h-5 w-32" />
      <Skeleton className="mb-4 h-10 w-64" />
      <Skeleton className="h-64 w-full" />
    </PageShell>
  );
}
