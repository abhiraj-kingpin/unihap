"use client";

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { useLiveAnnouncer } from "@/components/common/live-region";
import { api, metricsKeys, productKeys } from "@/lib/api";
import type { ApprovalRequest, BulkActionRequest } from "@/types";

export function useApproveProduct() {
  const queryClient = useQueryClient();
  const announce = useLiveAnnouncer();

  return useMutation({
    mutationFn: ({ id, ...body }: ApprovalRequest & { id: string }) => api.approveProduct(id, body),
    onSuccess: (result) => {
      queryClient.invalidateQueries({ queryKey: productKeys.all });
      queryClient.invalidateQueries({ queryKey: metricsKeys.all });
      announce(`${result.name} approved.`);
    },
    onError: () => announce("Approval failed. Please try again."),
  });
}

export function useRejectProduct() {
  const queryClient = useQueryClient();
  const announce = useLiveAnnouncer();

  return useMutation({
    mutationFn: ({ id, ...body }: ApprovalRequest & { id: string }) => api.rejectProduct(id, body),
    onSuccess: (result) => {
      queryClient.invalidateQueries({ queryKey: productKeys.all });
      queryClient.invalidateQueries({ queryKey: metricsKeys.all });
      announce(`${result.name} rejected.`);
    },
    onError: () => announce("Rejection failed. Please try again."),
  });
}

export function useBulkAction() {
  const queryClient = useQueryClient();
  const announce = useLiveAnnouncer();

  return useMutation({
    mutationFn: (body: BulkActionRequest) => api.bulkAction(body),
    onSuccess: (result) => {
      queryClient.invalidateQueries({ queryKey: productKeys.all });
      queryClient.invalidateQueries({ queryKey: metricsKeys.all });
      announce(`${result.success_count} products updated${result.failed_count ? `, ${result.failed_count} failed` : ""}.`);
    },
    onError: () => announce("Bulk action failed. Please try again."),
  });
}
