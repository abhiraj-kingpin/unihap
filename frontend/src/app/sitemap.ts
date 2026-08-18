import type { MetadataRoute } from "next";

const BASE_URL = "http://localhost:3000";

export default function sitemap(): MetadataRoute.Sitemap {
  const lastModified = new Date();
  return [
    { url: BASE_URL, lastModified },
    { url: `${BASE_URL}/catalog`, lastModified },
    { url: `${BASE_URL}/settings`, lastModified },
  ];
}
