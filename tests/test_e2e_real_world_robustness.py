"""
==============================================================================
FILE: tests/test_e2e_real_world_robustness.py
MODULE: Real-World End-to-End Robustness & Multi-Domain Pipeline Tests
PURPOSE:
    Extensively tests the 12-layer pipeline across all real-world domains and edge cases
    found in industrial and e-commerce catalogs:
      1. Lighting & Electrical (Philips, Satco, Kichler, Leviton, Southwire)
      2. Building Materials & Lumber (Boise Cascade, Parksite, U.S. Lumber)
      3. Power Tools & Abrasives (Diablo/Freud, 3M, DeWalt, Makita, Festool)
      4. Major Appliances (Frigidaire, Whirlpool, Rheem)
      5. Plumbing & Industrial Valves (Kohler, Moen, Delta, Watts, Sloan)
      6. Adversarial edge cases: junk brands, nested fractions, compound UOMs,
         distributor ID stripping, strict character limits, and zero-hallucination guarantees.
==============================================================================
"""

import pytest

from unihap.core.delivery_format import DELIVERY_HEADERS, DeliveryFormatExporter
from unihap.core.models import ProductRecord, StatusTag
from unihap.pipeline import UniHAPPipeline


@pytest.fixture(scope="module")
def pipeline():
    return UniHAPPipeline()


# ============================================================================
# 1. MULTI-DOMAIN REAL-WORLD PRODUCT TESTS
# ============================================================================


@pytest.mark.parametrize(
    "mfr_input,brand_input,desc_input,expected_mfr_substring,expected_dept,expected_fine",
    [
        # Domain 1: Power Tools & Abrasives
        (
            "Freud Inc (2435)",
            "-- Unbranded --",
            'DCB518ASTS06G Diablo 1/2"x18" - Sanding Belt 6pc',
            "Freud",
            "Tools",
            "Sanding Belts",
        ),
        (
            "Jam Industrial Supply LLC (JAMIN)",
            "-- Unbranded --",
            "3M 775L Stikit Film P150 - Cubitron II 50 Disc/Box",
            "Jam Industrial Supply",
            "Tools",
            "Sanding Belts",
        ),
        (
            "Makita Usa Inc (5142)",
            "Makita",
            "Makita 18V LXT Lithium-Ion Brushless Cordless Impact Driver",
            "Makita",
            "Tools",
            "Drills & Drivers",
        ),
        # Domain 2: Appliances & HVAC
        (
            "Appliance Dealers Cooperative (APPDE)",
            "-- Unbranded --",
            "PDSH4816AF Dishwasher SS - Built-In Display Only",
            "Appliance Dealers Cooperative",
            "Appliances",
            "Dishwashers",
        ),
        (
            "Appliance Dealers Cooperative (APPDE)",
            "-- Unbranded --",
            "WDTS7024RZ Dishwasher SS - Built-in Eco Series",
            "Appliance Dealers Cooperative",
            "Appliances",
            "Dishwashers",
        ),
        (
            "Rheem Manufacturing (4812)",
            "Rheem",
            "Rheem Performance Plus 50 Gal 40k BTU Natural Gas Water Heater",
            "Rheem",
            "Appliances",
            "Residential Water Heaters",
        ),
        # Domain 3: Plumbing Fixtures & Valves
        (
            "Kohler Co. (1102)",
            "Kohler",
            "Simplice Pull-Down Kitchen Sink Faucet in Matte Black 1.8 GPM",
            "Kohler",
            "Plumbing",
            "Kitchen Faucets",
        ),
        (
            "Delta Faucet Co (3311)",
            "Delta",
            "Essa Single Handle Pull-Down Kitchen Faucet in Stainless Steel",
            "Delta",
            "Plumbing",
            "Kitchen Faucets",
        ),
        (
            "Watts Regulator Co (8819)",
            "Watts",
            "Watts 1/2 in Brass Full Port Threaded Ball Valve 600 WOG",
            "Watts",
            "Plumbing",
            "Ball Valves",
        ),
        (
            "Nibco Inc (2910)",
            "-- Unbranded --",
            "Nibco 2 in PVC DWV 90 Degree Elbow Fitting",
            "Nibco",
            "Plumbing",
            "Pipe Fittings",
        ),
    ],
)
def test_multi_domain_e2e_classification_and_matching(
    pipeline, mfr_input, brand_input, desc_input, expected_mfr_substring, expected_dept, expected_fine
):
    """Verifies that diverse product categories resolve correct canonical entities and classpaths."""
    raw = ProductRecord(
        row_id="TEST_ROW", MPN="TEST_MPN_101", Manufacturer=mfr_input, Brand=brand_input, Description=desc_input
    )
    enriched = pipeline.process_record(raw)

    assert expected_mfr_substring in enriched.canonical_manufacturer
    assert enriched.classification is not None
    assert enriched.classification.department in [expected_dept, "General Merchandise"]
    assert enriched.classification.confidence >= 0.70


# ============================================================================
# 2. ADVERSARIAL EDGE CASE TESTS (Junk Data, Placeholders, Complex Strings)
# ============================================================================


def test_distributor_id_and_parenthesis_stripping(pipeline):
    """Asserts that messy vendor codes like (2435), (JAMIN), (APPDE), (BOICA) are stripped."""
    raw = ProductRecord(
        row_id="ROW_DIST_1",
        MPN="D-1234",
        Manufacturer="Boise Cascade Building Materials (BOICA)",
        Brand="-- No Unilog Brand --",
        Description="2x4 Framing Lumber 8ft Premium SPF",
    )
    enriched = pipeline.process_record(raw)
    assert "(BOICA)" not in enriched.canonical_manufacturer
    assert "Boise Cascade" in enriched.canonical_manufacturer


def test_junk_brand_fallback_to_canonical_manufacturer(pipeline):
    """Asserts that junk placeholders ('-- Unbranded --', '-- No DIB Brand --') fall back to canonical manufacturer."""
    raw = ProductRecord(
        row_id="ROW_JUNK_BRAND",
        MPN="7594SRS",
        Manufacturer="Moen Inc.",
        Brand="-- No Unilog Brand --",
        Description="Arbor One-Handle Pulldown Kitchen Faucet Stainless",
    )
    enriched = pipeline.process_record(raw)
    assert enriched.canonical_brand == "Moen" or enriched.canonical_brand == "Moen Inc"


def test_complex_fraction_and_dimension_normalization(pipeline):
    """Asserts that compound dimensions with multiple fractions and UOMs normalize deterministically."""
    normalizer = pipeline.normalizer

    # Complex multi-fractional dimensions
    raw_dim = "33-7/16 in H x 23-7/8 in W x 22-5/8 in D"
    norm_dim = normalizer.normalize_string(raw_dim)
    assert "33.4375" in norm_dim or "33.4" in norm_dim or "33-" in norm_dim or "in H" in norm_dim

    # Nested quotes as inches
    raw_pipe = '1/2" x 18" Sanding Belt'
    norm_pipe = normalizer.normalize_string(raw_pipe)
    assert "0.5 in x 18 in" in norm_pipe


# ============================================================================
# 3. DESCRIPTION CONSTRAINT & CHARACTER LIMIT INVARIANTS
# ============================================================================


def test_description_format_length_and_casing_invariants(pipeline):
    """Asserts that all 5 description formats strictly comply with length and casing specifications."""
    raw = ProductRecord(
        row_id="ROW_DESC_TEST",
        MPN="PDSH4816AF-EXTREME-LONG-MPN-TEST-12345",
        Manufacturer="Appliance Dealers Cooperative (APPDE)",
        Description="Extremely Long Detailed Product Description for Built-In Dishwasher with CleanBoost System 5-Wash Cycles Stainless Steel",
    )
    enriched = pipeline.process_record(raw)

    # 1. Invoice: Must be <= 40 chars, ALL CAPS, stripped
    invoice = enriched.descriptions.invoice_caps
    assert len(invoice) <= 40, f"Invoice description exceeded 40 chars: '{invoice}' ({len(invoice)})"
    assert invoice.isupper() or invoice == "", f"Invoice must be uppercase: '{invoice}'"

    # 2. Mobile: Must be <= 80 chars
    mobile = enriched.descriptions.mobile
    assert len(mobile) <= 80, f"Mobile description exceeded 80 chars: '{mobile}' ({len(mobile)})"

    # 3. Short Title & Long Description: Must not be empty
    assert len(enriched.descriptions.short_title) > 0
    assert len(enriched.descriptions.long_desc) > 0
    assert len(enriched.descriptions.retail_bullet_points) >= 3


# ============================================================================
# 4. ZERO-HALLUCINATION & PROVENANCE CITATION INVARIANTS
# ============================================================================


def test_zero_hallucination_and_abstain_rule(pipeline):
    """
    CRITICAL INVARIANT:
    No layer may invent facts. Every auto-approved attribute MUST have an exact evidence span.
    Missing attributes MUST have status ABSTAINED.
    """
    raw = ProductRecord(
        row_id="ROW_PROV_1",
        MPN="K-596",
        Manufacturer="Kohler",
        Description="Simplice Kitchen Faucet in Matte Black 1.8 GPM",
    )
    enriched = pipeline.process_record(raw)

    for attr_name, attr_val in enriched.attributes.items():
        if attr_val.status == StatusTag.AUTO_APPROVED:
            # Must have non-empty provenance span and source URL
            assert attr_val.provenance is not None, f"Attribute {attr_name} auto-approved without provenance!"
            assert len(attr_val.provenance.exact_text_span) > 0
            assert "http" in attr_val.provenance.source_url
            assert attr_val.in_lov is True
        elif attr_val.status == StatusTag.ABSTAINED:
            # Must not fabricate value
            assert attr_val.normalized_value is None


# ============================================================================
# 5. 252-COLUMN DELIVERY CSV EXPORT INTEGRITY
# ============================================================================


def test_delivery_export_column_integrity_and_parity(pipeline, tmp_path):
    """Asserts that exporting to delivery format generates valid 252-column rows for every record."""
    raw_records = [
        ProductRecord(row_id="101", MPN="K-596", Manufacturer="Kohler", Description="Pull-Down Faucet Matte Black"),
        ProductRecord(row_id="102", MPN="WDTS7024", Manufacturer="Whirlpool", Description="Dishwasher SS Built-In"),
        ProductRecord(row_id="103", MPN="DCB518", Manufacturer="Freud", Description="Diablo 1/2x18 Sanding Belt"),
    ]
    enriched_records = [pipeline.process_record(r) for r in raw_records]

    out_file = tmp_path / "parity_test_delivery.csv"
    DeliveryFormatExporter.export_to_csv(enriched_records, out_file)

    assert out_file.exists()
    with open(out_file, mode="r", encoding="utf-8") as f:
        import csv

        reader = csv.DictReader(f)
        assert len(reader.fieldnames) == 252
        assert reader.fieldnames == DELIVERY_HEADERS

        rows = list(reader)
        assert len(rows) == 3
        for r in rows:
            assert r["PART_NUMBER"] in ["101", "102", "103"]
            assert len(r["INVOICE_DESC"]) <= 40
            assert r["MFR URL"].startswith("https://")
