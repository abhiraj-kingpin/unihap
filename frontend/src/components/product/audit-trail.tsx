import { Disclosure, DisclosureButton, DisclosurePanel } from "@/components/ui/disclosure";

export function AuditTrail({ entries }: { entries: string[] }) {
  return (
    <Disclosure>
      <div className="p-5">
        <DisclosureButton>
          <span className="text-sm font-semibold uppercase tracking-wide text-text-muted">
            Audit Trail ({entries.length} events)
          </span>
        </DisclosureButton>
        <DisclosurePanel className="pt-4">
          <ol className="flex flex-col gap-2">
            {entries.map((entry, i) => (
              <li key={i} className="font-mono text-xs leading-relaxed text-text-muted">
                {entry}
              </li>
            ))}
          </ol>
        </DisclosurePanel>
      </div>
    </Disclosure>
  );
}
