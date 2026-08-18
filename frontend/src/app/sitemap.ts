import type { MetadataRoute } from "next";
import { SITE_URL } from "@/lib/constants";

export default function sitemap(): MetadataRoute.Sitemap {
  const lastModified = new Date();
  return [
    { url: SITE_URL, lastModified },
    { url: `${SITE_URL}/catalog`, lastModified },
    { url: `${SITE_URL}/settings`, lastModified },
  ];
}
