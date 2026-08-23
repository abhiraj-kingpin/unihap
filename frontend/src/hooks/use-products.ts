"use client";

import { keepPreviousData, useQuery } from "@tanstack/react-query";
import { api, productKeys } from "@/lib/api";
import type { ListProductsParams } from "@/types";

export function useProductsQuery(params: ListProductsParams) {
  return useQuery({
    queryKey: productKeys.list(params),
    queryFn: () => api.listProducts(params),
    placeholderData: keepPreviousData,
  });
}

export function useProductQuery(id: string) {
  return useQuery({
    queryKey: productKeys.detail(id),
    queryFn: () => api.getProduct(id),
    enabled: Boolean(id),
  });
}
