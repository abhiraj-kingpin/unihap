import type { Metadata } from "next";
import { PageShell } from "@/components/layout/page-shell";
import { SettingsView } from "@/components/settings/settings-view";

export const metadata: Metadata = {
  title: "Settings",
  description: "Manage your curator profile and catalog preferences.",
};

export default function SettingsPage() {
  return (
    <PageShell>
      <SettingsView />
    </PageShell>
  );
}
