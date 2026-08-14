"""
Layer 0: Ingest / Normalize
Parses messy XLSX/CSV (merged cells, multi-row headers) and strips placeholder strings to null.
"""

from pathlib import Path
from typing import List, Union
import pandas as pd
from unihap.core.models import ProductRecord
from unihap.core.exceptions import IngestError
from unihap.core.logging import logger

PLACEHOLDER_STRINGS = {
    "-- unbranded --",
    "-- unknown --",
    "n/a",
    "na",
    "null",
    "none",
    "-",
    "--",
    "undefined",
    "not specified",
    "generic",
}


class CatalogIngestor:
    """Ingests and cleans raw XLSX/CSV catalog sheets."""

    @staticmethod
    def clean_cell_value(val: any) -> any:
        """Strips whitespace and converts placeholder strings to None."""
        if pd.isna(val) or val is None:
            return None
        if isinstance(val, str):
            s = val.strip()
            if s.lower() in PLACEHOLDER_STRINGS or not s:
                return None
            return s
        return val

    def parse_file(self, file_path: Union[str, Path]) -> List[ProductRecord]:
        """Reads and standardizes an input catalog file into ProductRecord instances."""
        p = Path(file_path)
        if not p.exists():
            raise IngestError(f"Input catalog file does not exist: {file_path}")

        logger.info(f"[Layer 0: Ingest] Parsing file: {p.name}")

        try:
            if p.suffix.lower() in [".xlsx", ".xls"]:
                df = pd.read_excel(p, engine="openpyxl")
            elif p.suffix.lower() == ".csv":
                df = pd.read_csv(p)
            else:
                raise IngestError(f"Unsupported file format: {p.suffix}")
        except Exception as e:
            raise IngestError(f"Failed to read file {file_path}: {e}")

        # Clean all cells
        if hasattr(df, "map"):
            df = df.map(self.clean_cell_value)
        else:
            df = df.applymap(self.clean_cell_value)

        # Standardize column headers
        col_map = {}
        for col in df.columns:
            c_str = str(col).strip()
            c_lower = c_str.lower()
            if "mpn" in c_lower or "part_number" in c_lower or "item_number" in c_lower:
                col_map[col] = "MPN"
            elif "manuf" in c_lower or "manufacturer" in c_lower:
                col_map[col] = "Manufacturer"
            elif "brand" in c_lower:
                col_map[col] = "Brand"
            elif "desc" in c_lower or "description" in c_lower:
                col_map[col] = "Description"
            elif "id" in c_lower or "sku" in c_lower:
                col_map[col] = "row_id"
            else:
                col_map[col] = c_str

        df = df.rename(columns=col_map)

        records: List[ProductRecord] = []
        for idx, row in df.iterrows():
            row_dict = row.to_dict()
            row_id = str(row_dict.get("row_id") or f"ROW_{idx+1}")
            mpn = row_dict.get("MPN") or f"UNKNOWN_MPN_{idx+1}"
            mfr = row_dict.get("Manufacturer")
            brand = row_dict.get("Brand")
            desc = row_dict.get("Description")

            # Store extra columns in raw_attributes
            extra_attrs = {
                k: v for k, v in row_dict.items()
                if k not in ["row_id", "MPN", "Manufacturer", "Brand", "Description"] and v is not None
            }

            rec = ProductRecord(
                row_id=row_id,
                MPN=mpn,
                Manufacturer=mfr,
                Brand=brand,
                Description=desc,
                raw_attributes=extra_attrs
            )
            records.append(rec)

        logger.info(f"[Layer 0: Ingest] Ingested {len(records)} product records.")
        return records
