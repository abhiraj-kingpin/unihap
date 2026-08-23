export function SoftwareApplicationJsonLd() {
  const data = {
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    name: "UniHAP HITL Dashboard",
    applicationCategory: "BusinessApplication",
    operatingSystem: "Web",
    description:
      "Approve or reject AI-enriched products with evidence-based curation. Real-time metrics, bulk actions, and complete audit trails.",
  };

  return <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(data) }} />;
}
