import { Badge } from "@/components/ui/badge";
import { formatConfidence } from "@/lib/format";

function toneFor(confidence: number): "approved" | "pending" | "rejected" {
  if (confidence >= 0.9) return "approved";
  if (confidence >= 0.7) return "pending";
  return "rejected";
}

export function ConfidenceMeter({ confidence }: { confidence: number }) {
  return (
    <Badge tone={toneFor(confidence)} className="font-mono tabular">
      {formatConfidence(confidence)}
    </Badge>
  );
}
