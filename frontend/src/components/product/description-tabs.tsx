import { Tab, TabList, TabPanel, Tabs } from "@/components/ui/tabs";
import type { DescriptionSetOut } from "@/types";

const TABS = [
  { id: "invoice_caps", label: "Invoice" },
  { id: "mobile", label: "Mobile" },
  { id: "short_title", label: "Short" },
  { id: "long_desc", label: "Long" },
  { id: "retail_bullet_points", label: "Retail" },
] as const;

export function DescriptionTabs({ descriptions }: { descriptions: DescriptionSetOut }) {
  return (
    <Tabs defaultTabId="invoice_caps">
      <TabList label="Description formats">
        {TABS.map((tab) => (
          <Tab key={tab.id} id={tab.id}>
            {tab.label}
          </Tab>
        ))}
      </TabList>

      <TabPanel id="invoice_caps">
        <p className="font-mono tracking-wide text-text-primary">{descriptions.invoice_caps}</p>
      </TabPanel>
      <TabPanel id="mobile">
        <p className="text-text-primary">{descriptions.mobile}</p>
      </TabPanel>
      <TabPanel id="short_title">
        <p className="text-text-primary">{descriptions.short_title}</p>
      </TabPanel>
      <TabPanel id="long_desc">
        <p className="text-text-primary">{descriptions.long_desc}</p>
      </TabPanel>
      <TabPanel id="retail_bullet_points">
        <ul className="flex flex-col gap-2">
          {descriptions.retail_bullet_points.map((point) => (
            <li key={point} className="flex items-start gap-2 text-text-primary">
              <span className="mt-1.5 h-1 w-1 shrink-0 rounded-full bg-brand" />
              {point}
            </li>
          ))}
        </ul>
      </TabPanel>
    </Tabs>
  );
}
