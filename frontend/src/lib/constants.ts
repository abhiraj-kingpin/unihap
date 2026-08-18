export const PAGE_SIZE_OPTIONS = [10, 25, 50, 100] as const;

export const SORT_OPTIONS = [
  { value: "confidence_desc", label: "Confidence: High to Low" },
  { value: "confidence_asc", label: "Confidence: Low to High" },
  { value: "name_asc", label: "Name: A to Z" },
  { value: "created_desc", label: "Newest First" },
] as const;

export const NAV_LINKS = [
  { href: "/catalog", label: "Catalog" },
  { href: "/settings", label: "Settings" },
] as const;

export const DEFAULT_CURATOR_NAME = "curator";
export const DEFAULT_PAGE_SIZE = 25;
