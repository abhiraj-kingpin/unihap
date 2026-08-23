import { AlertTriangle } from "lucide-react";

interface ErrorStateProps {
  title: string;
  description?: string;
  hint?: string;
}

export function ErrorState({ title, description, hint }: ErrorStateProps) {
  return (
    <div className="flex flex-col items-center gap-3 rounded-2xl border border-status-rejected/25 bg-status-rejected-bg px-6 py-14 text-center">
      <AlertTriangle size={26} className="text-status-rejected-text" />
      <p className="text-sm font-semibold text-status-rejected-text">{title}</p>
      {description && <p className="max-w-md text-sm text-text-muted">{description}</p>}
      {hint && <code className="mt-1 rounded-md bg-bg px-3 py-1.5 font-mono text-xs text-text-primary">{hint}</code>}
    </div>
  );
}
