"use client";

import { useState } from "react";
import { useLiveAnnouncer } from "@/components/common/live-region";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useCuratorSettings } from "@/hooks/use-curator-settings";

export function CuratorNameForm() {
  const { curatorName, setCuratorName } = useCuratorSettings();
  const [draft, setDraft] = useState(curatorName);
  const announce = useLiveAnnouncer();

  function handleSubmit(event: React.FormEvent) {
    event.preventDefault();
    const trimmed = draft.trim();
    if (!trimmed) return;
    setCuratorName(trimmed);
    announce("Curator name saved.");
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-3 p-5">
      <label htmlFor="curator-name" className="text-xs font-semibold uppercase tracking-wide text-text-muted">
        Curator Name
      </label>
      <p className="-mt-2 text-sm text-text-faint">Attached to every approve/reject decision you make.</p>
      <div className="flex gap-2">
        <Input id="curator-name" value={draft} onChange={(e) => setDraft(e.target.value)} className="flex-1" />
        <Button type="submit" variant="primary" disabled={draft.trim() === curatorName}>
          Save
        </Button>
      </div>
    </form>
  );
}
