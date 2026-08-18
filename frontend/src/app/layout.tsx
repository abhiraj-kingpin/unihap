import type { Metadata } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";
import { Providers } from "@/app/providers";
import "./globals.css";

const inter = Inter({
  subsets: ["latin"],
  variable: "--font-inter",
  display: "swap",
});

const jetbrainsMono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-jetbrains-mono",
  display: "swap",
});

export const metadata: Metadata = {
  metadataBase: new URL("http://localhost:3000"),
  title: {
    default: "UniHAP HITL Dashboard - AI Product Review & Curation",
    template: "%s | UniHAP",
  },
  description:
    "Approve or reject AI-enriched products with evidence-based curation. Real-time metrics, bulk actions, and complete audit trails.",
  openGraph: {
    title: "UniHAP HITL Dashboard - AI Product Review & Curation",
    description:
      "Approve or reject AI-enriched products with evidence-based curation. Real-time metrics, bulk actions, and complete audit trails.",
    type: "website",
  },
};

export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en" className={`${inter.variable} ${jetbrainsMono.variable}`}>
      <body className="antialiased">
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
