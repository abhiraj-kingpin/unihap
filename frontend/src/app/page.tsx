import { dehydrate, HydrationBoundary } from "@tanstack/react-query";
import type { Metadata } from "next";
import { LandingView } from "@/components/landing/landing-view";
import { SoftwareApplicationJsonLd } from "@/components/landing/software-application-jsonld";
import { api, metricsKeys } from "@/lib/api";
import { getQueryClient } from "@/lib/query-client";

export const metadata: Metadata = {
  title: "UniHAP HITL Dashboard - AI Product Review & Curation",
};

export default async function HomePage() {
  const queryClient = getQueryClient();
  await queryClient.prefetchQuery({ queryKey: metricsKeys.all, queryFn: api.getMetrics });

  return (
    <HydrationBoundary state={dehydrate(queryClient)}>
      <SoftwareApplicationJsonLd />
      <LandingView />
    </HydrationBoundary>
  );
}
