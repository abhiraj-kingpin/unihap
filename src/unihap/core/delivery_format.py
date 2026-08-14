"""
UniHAP 252-Column Delivery Format Exporter.
Aligns pipeline outputs with the exact Unihack Expected Delivery Format schema.
"""

from typing import Dict, List, Any
import csv
from pathlib import Path
from unihap.core.models import EnrichedProductRecord

# Exact 252-column delivery header list from the Unihack benchmark
DELIVERY_HEADERS: List[str] = [
    'MFR URL', 'Ref URL 1', 'Ref URL 2', 'Ref URL 3', 'Ref URL 4', 'Ref URL 5',
    'PART_NUMBER', 'Dept', 'Class', 'Fine', 'SKU - MY_PART_NUMBER', 'Mfg_Part_Num',
    'Part_Desc', 'E1_Brand', 'Unilog_Brand', 'DIB_Brand', 'Part_Manuf',
    'MANUFACTURER_NAME', 'BRAND_NAME', 'TRADE_NAME', 'MANUFACTURER_PART_NUMBER',
    'ALTERNATE_PART_NUMBER', 'Classpath', 'MOBILE_DESC', 'INVOICE_DESC', 'SHORT_DESC',
    'LONG_DESC1', 'RETAIL_DESC', 'MARKETING_DESCRIPTION',
    'ITEM_FEATURES_1', 'ITEM_FEATURES_2', 'ITEM_FEATURES_3', 'ITEM_FEATURES_4', 'ITEM_FEATURES_5',
    'ITEM_FEATURES_6', 'ITEM_FEATURES_7', 'ITEM_FEATURES_8', 'ITEM_FEATURES_9', 'ITEM_FEATURES_10',
    'ITEM_FEATURES_11', 'ITEM_FEATURES_12', 'ITEM_FEATURES_13', 'ITEM_FEATURES_14', 'ITEM_FEATURES_15',
    'ITEM_FEATURES_16', 'ITEM_FEATURES_17', 'ITEM_FEATURES_18', 'ITEM_FEATURES_19', 'ITEM_FEATURES_20',
    'With', 'Standard/Approvals', 'Prop 65', 'Application', 'Includes', 'Product Name'
]

# Add 50 Attribute Triplets (Label, Value, UOM) -> 150 columns
for i in range(1, 51):
    DELIVERY_HEADERS.extend([f'ATTRIBUTE_LABEL {i}', f'ATTRIBUTE_VALUE {i}', f'ATTRIBUTE_UOM {i}'])

# Add Universal Identifiers, Dimensions & Assets -> 46 columns
DELIVERY_HEADERS.extend([
    'UPC', 'EAN', 'GTIN', 'UNSPSC', 'Warranty', 'List Price', 'Selling Qty', 'Selling UOM',
    'Standard Packaging Information', 'LENGTH', 'LENGTH_UOM', 'HEIGHT', 'HEIGHT_UOM',
    'WIDTH', 'WIDTH_UOM', 'WEIGHT', 'WEIGHT_UOM', 'VOLUME', 'VOLUME_UOM',
    'Product Image', 'Alternate Image 1', 'Alternate Image 2', 'Alternate Image 3', 'Alternate Image 4',
    'SDS', 'SDS_1', 'Warranty Information', 'Catalog', 'Specification Sheet',
    'Instruction/Installation Manual', 'Service Manual', 'Owners/User Manual', 'Line Drawing',
    'MTR', 'RoHS', 'Full Engineering Drawing', 'Energy Star Guide', 'Technical Bulletin',
    'Submittal', 'Compatibility Chart', 'Size Chart', 'Product Label/Insert', 'Video Link',
    'Video Link 1', 'Country Of Origin', 'Discontinued', 'Actual Image (Yes/No)'
])


class DeliveryFormatExporter:
    """Exports enriched catalog records to the canonical 252-column delivery format."""

    @staticmethod
    def record_to_delivery_row(record: EnrichedProductRecord) -> Dict[str, Any]:
        """Maps an EnrichedProductRecord to a 252-column dictionary."""
        row: Dict[str, str] = {h: "" for h in DELIVERY_HEADERS}

        # URLs
        row['MFR URL'] = record.spec_source_url or (f"https://{record.manufacturer_domain}" if record.manufacturer_domain else "")
        if record.spec_sheet_pdf_urls:
            row['Ref URL 1'] = record.spec_sheet_pdf_urls[0]

        # Identifiers
        row['PART_NUMBER'] = record.row_id
        row['Mfg_Part_Num'] = record.mpn
        row['MANUFACTURER_PART_NUMBER'] = record.mpn
        row['MANUFACTURER_NAME'] = record.canonical_manufacturer
        row['BRAND_NAME'] = record.canonical_brand or record.canonical_manufacturer

        # Taxonomy
        if record.classification:
            row['Dept'] = record.classification.department
            row['Class'] = record.classification.category_class
            row['Fine'] = record.classification.fine_category
            row['Classpath'] = record.classification.full_path.replace(" > ", ">")
            row['Product Name'] = record.classification.fine_category

        # Descriptions
        if record.descriptions:
            row['MOBILE_DESC'] = record.descriptions.mobile
            row['INVOICE_DESC'] = record.descriptions.invoice_caps
            row['SHORT_DESC'] = record.descriptions.short_title
            row['LONG_DESC1'] = record.descriptions.long_desc
            row['RETAIL_DESC'] = record.descriptions.long_desc
            row['MARKETING_DESCRIPTION'] = record.descriptions.long_desc

            # Features
            for idx, feat in enumerate(record.descriptions.retail_bullet_points[:20]):
                row[f'ITEM_FEATURES_{idx+1}'] = feat

        # Attributes (Triplets: Label, Value, UOM)
        attr_idx = 1
        for attr_name, attr_val in record.attributes.items():
            if attr_idx > 50:
                break
            if attr_val.normalized_value:
                row[f'ATTRIBUTE_LABEL {attr_idx}'] = attr_name
                row[f'ATTRIBUTE_VALUE {attr_idx}'] = attr_val.normalized_value
                if attr_val.uom:
                    row[f'ATTRIBUTE_UOM {attr_idx}'] = attr_val.uom
                attr_idx += 1

        # Assets
        if record.verified_image_urls:
            row['Product Image'] = record.verified_image_urls[0]
            for idx, img in enumerate(record.verified_image_urls[1:5]):
                row[f'Alternate Image {idx+1}'] = img

        if record.spec_sheet_pdf_urls:
            row['Specification Sheet'] = record.spec_sheet_pdf_urls[0]

        return row

    @classmethod
    def export_to_csv(cls, records: List[EnrichedProductRecord], output_path: Path):
        """Writes enriched records to 252-column CSV file."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=DELIVERY_HEADERS)
            writer.writeheader()
            for r in records:
                writer.writerow(cls.record_to_delivery_row(r))
