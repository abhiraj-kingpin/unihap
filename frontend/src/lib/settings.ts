import { DEFAULT_CURATOR_NAME, DEFAULT_PAGE_SIZE } from "@/lib/constants";

export const SETTINGS_KEYS = {
  curatorName: "unihap.curator_name",
  defaultPageSize: "unihap.default_page_size",
} as const;

export const SETTINGS_DEFAULTS = {
  curatorName: DEFAULT_CURATOR_NAME,
  defaultPageSize: DEFAULT_PAGE_SIZE,
} as const;
