"use client";

import { useQuery } from "@tanstack/react-query";
import { api, metricsKeys } from "@/lib/api";

export function useMetricsQuery() {
  return useQuery({
    queryKey: metricsKeys.all,
    queryFn: api.getMetrics,
    staleTime: 30_000,
  });
}
