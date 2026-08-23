import { ScrollReveal } from "@/components/common/scroll-reveal";
import { CuratorNameForm } from "@/components/settings/curator-name-form";
import { PageSizePreference } from "@/components/settings/page-size-preference";
import { Card, CardHeader, CardTitle } from "@/components/ui/card";

export function SettingsView() {
  return (
    <div>
      <div className="mb-8">
        <h1 className="text-[28px] font-bold text-text-primary">Settings</h1>
        <p className="mt-1 text-sm text-text-muted">Curator preferences for this browser.</p>
      </div>

      <div className="flex max-w-lg flex-col gap-6">
        <ScrollReveal>
          <Card>
            <CardHeader>
              <CardTitle>Profile</CardTitle>
            </CardHeader>
            <CuratorNameForm />
          </Card>
        </ScrollReveal>

        <ScrollReveal delay={0.05}>
          <Card>
            <CardHeader>
              <CardTitle>Catalog Defaults</CardTitle>
            </CardHeader>
            <PageSizePreference />
          </Card>
        </ScrollReveal>
      </div>
    </div>
  );
}
