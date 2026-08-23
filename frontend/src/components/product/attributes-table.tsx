import { AttributeRow } from "@/components/product/attribute-row";
import { EmptyState } from "@/components/common/empty-state";
import { ListX } from "lucide-react";
import type { AttributeOut } from "@/types";

export function AttributesTable({ attributes }: { attributes: AttributeOut[] }) {
  if (attributes.length === 0) {
    return <EmptyState icon={ListX} title="No attributes extracted for this record" />;
  }

  return (
    <div>
      {attributes.map((attribute) => (
        <AttributeRow key={attribute.name} attribute={attribute} />
      ))}
    </div>
  );
}
