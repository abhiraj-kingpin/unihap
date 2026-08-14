"""
==============================================================================
FILE: tests/test_layers_unit.py
MODULE: Unit Tests for 12 Pipeline Layers
PURPOSE:
    Tests each individual layer in isolation:
      - Layer 0: Ingest & placeholder filtering
      - Layer 1: Fuzzy entity matching & vendor ID stripping
      - Layer 2: 3-stage taxonomy classification
      - Layer 3: Knowledge Graph traversal & synonym canonicalization
      - Layer 4: Manufacturer domain discovery & blocklist enforcement
      - Layer 5: Crawl4AI scraping & VLM nameplate inspection
      - Layer 6: Constrained RAG attribute extraction & abstain logic
      - Layer 7: UOM & fraction normalization
      - Layer 8: 5 description formats synthesis
      - Layer 9: Quality validation & confidence scoring
      - Layer 10: HITL review queue & correction feedback
      - Layer 11: Digital asset discovery
      - Layer 12: Benchmark evaluation engine
==============================================================================
"""

import pytest

from unihap.core.models import (
    AttributeValue,
    Classpath,
    EnrichedProductRecord,
    ProductDescriptionSet,
    ProvenanceSpan,
    StatusTag,
)
from unihap.layers.l0_ingest import CatalogIngestor
from unihap.layers.l1_entity_res import EntityResolver
from unihap.layers.l2_classify import ProductClassifier
from unihap.layers.l3_knowledge_graph import TaxonomyGraph
from unihap.layers.l4_discovery import SourceDiscoverer
from unihap.layers.l5_document_intel import DocumentScraper
from unihap.layers.l6_extraction import AttributeExtractor
from unihap.layers.l7_normalize import AttributeNormalizer
from unihap.layers.l8_synthesis import DescriptionSynthesizer
from unihap.layers.l9_validation import QualityValidator
from unihap.layers.l10_hitl import ReviewQueueManager
from unihap.layers.l11_digital_assets import DigitalAssetManager
from unihap.layers.l12_evaluation import BenchmarkEvaluator


def test_layer_0_ingest_placeholders():
    ingestor = CatalogIngestor()
    assert ingestor.clean_cell_value("-- Unbranded --") is None
    assert ingestor.clean_cell_value("-- No Unilog Brand --") is None
    assert ingestor.clean_cell_value("N/A") is None
    assert ingestor.clean_cell_value("Valid Product") == "Valid Product"


def test_layer_1_entity_resolution():
    resolver = EntityResolver()
    # Test vendor code stripping
    assert resolver.strip_distributor_codes("Freud Inc (2435)") == "Freud"
    assert resolver.strip_distributor_codes("Jam Industrial Supply LLC (JAMIN)") == "Jam Industrial Supply"

    # Test fuzzy matching
    mfr, conf = resolver.resolve_manufacturer("Freud Inc (2435)")
    assert "Freud" in mfr
    assert conf >= 0.70

    mfr2, conf2 = resolver.resolve_manufacturer("Kohler Co.")
    assert mfr2 == "Kohler"
    assert conf2 >= 0.90


def test_layer_2_classification_funnel():
    classifier = ProductClassifier()
    # Plumbing
    cp1 = classifier.classify("Simplice Pull-Down Kitchen Faucet in Matte Black")
    assert cp1.department == "Plumbing"
    assert cp1.category_class == "Faucets"
    assert cp1.fine_category == "Kitchen Faucets"

    # Appliances
    cp2 = classifier.classify("PDSH4816AF Dishwasher SS - Built-in")
    assert cp2.department == "Appliances"
    assert cp2.fine_category == "Dishwashers"

    # Tools
    cp3 = classifier.classify('Diablo 1/2"x18" - Sanding Belt 6pc')
    assert cp3.department == "Tools"
    assert cp3.fine_category == "Sanding Belts"


def test_layer_3_knowledge_graph_and_synonyms():
    graph = TaxonomyGraph()
    kitchen_attrs = graph.get_allowed_attributes("Plumbing > Faucets > Kitchen Faucets")
    assert "Finish" in kitchen_attrs
    assert "Flow Rate" in kitchen_attrs

    # Check synonym canonicalization
    assert graph.canonicalize_synonym("SS") == "Stainless Steel"
    assert graph.canonicalize_synonym("MB") == "Matte Black"
    assert graph.canonicalize_synonym("1.8gpm") == "1.8 GPM"


def test_layer_4_source_discovery_and_blocklist():
    discoverer = SourceDiscoverer()
    # Official resolution
    assert discoverer.resolve_manufacturer_domain("Kohler") == "kohler.com"
    assert discoverer.resolve_manufacturer_domain("Frigidaire") == "frigidaire.com"

    # Valid product URL
    url = discoverer.find_product_url("Kohler", "K-596-BL")
    assert "kohler.com" in url
    assert "K-596-BL" in url


@pytest.mark.asyncio
async def test_layer_5_document_intelligence():
    scraper = DocumentScraper()
    md = await scraper.scrape_page_to_markdown("https://www.kohler.com/product/K-596-BL")
    assert "Matte Black" in md
    assert "1.8 GPM" in md

    vlm_res = scraper.process_scanned_image_vlm("sample_nameplate.jpg")
    assert vlm_res["vlm_status"] == "inspected"


def test_layer_6_constrained_rag_and_abstain():
    extractor = AttributeExtractor()
    sample_md = "**Finish**: Matte Black\n**Flow Rate**: 1.8 GPM"
    attrs = extractor.extract_attributes(
        markdown_text=sample_md,
        source_url="https://www.kohler.com/product/K-596-BL",
        classpath="Plumbing > Faucets > Kitchen Faucets",
    )
    # Grounded values must have provenance
    assert attrs["Finish"].in_lov is True
    assert attrs["Finish"].normalized_value == "Matte Black"
    assert attrs["Finish"].provenance is not None

    # Missing values must ABSTAIN (zero ungrounded facts)
    assert attrs["Spout Reach"].status == StatusTag.ABSTAINED
    assert attrs["Spout Reach"].normalized_value is None


def test_layer_7_normalization():
    normalizer = AttributeNormalizer()
    assert normalizer.normalize_string("1/2 inch pipe 1.8 gpm") == "0.5 in pipe 1.8 GPM"
    assert normalizer.normalize_string('1-1/4" fitting 60 psi') == "1.25 in fitting 60 PSI"
    assert normalizer.normalize_string("41 dba sound") == "41 dBA sound"


def test_layer_8_description_synthesis():
    synthesizer = DescriptionSynthesizer()
    cp = Classpath(department="Plumbing", category_class="Faucets", fine_category="Kitchen Faucets")
    attrs = {
        "Finish": AttributeValue(attribute_name="Finish", normalized_value="Matte Black", in_lov=True),
        "Flow Rate": AttributeValue(attribute_name="Flow Rate", normalized_value="1.8 GPM", in_lov=True),
    }
    desc_set = synthesizer.synthesize("Kohler", "K-596-BL", cp, attrs)
    assert len(desc_set.invoice_caps) <= 40
    assert desc_set.invoice_caps.isupper()
    assert len(desc_set.mobile) <= 80
    assert "Kohler" in desc_set.short_title
    assert len(desc_set.retail_bullet_points) >= 3


def test_layer_9_validation_and_scoring():
    validator = QualityValidator()
    prov = ProvenanceSpan(source_url="https://kohler.com", exact_text_span="Finish: Matte Black")
    rec = EnrichedProductRecord(
        row_id="1",
        mpn="K-596",
        canonical_manufacturer="Kohler",
        manufacturer_confidence=0.98,
        classification=Classpath(
            department="Plumbing", category_class="Faucets", fine_category="Kitchen Faucets", confidence=0.95
        ),
        descriptions=ProductDescriptionSet(invoice_caps="KOHLER K-596 KITCHEN FAUCET"),
        attributes={
            "Finish": AttributeValue(
                attribute_name="Finish", normalized_value="Matte Black", in_lov=True, provenance=prov
            )
        },
    )
    scored = validator.validate_and_score(rec)
    assert scored.overall_confidence > 0.85
    assert scored.overall_status == StatusTag.AUTO_APPROVED
    assert scored.overall_status in [StatusTag.AUTO_APPROVED, StatusTag.NEEDS_REVIEW]


def test_layer_10_hitl_review_queue():
    queue = ReviewQueueManager()
    rec = EnrichedProductRecord(
        row_id="ROW_100", mpn="TEST_MPN", canonical_manufacturer="Unknown", overall_status=StatusTag.NEEDS_REVIEW
    )
    queue.add_to_queue(rec)
    assert len(queue.queue) == 1

    corrected = queue.apply_human_correction("ROW_100", {"Finish": "Chrome"})
    assert corrected is not None
    assert corrected.overall_status == StatusTag.AUTO_APPROVED
    assert "Human correction" in corrected.audit_trail[-1]


def test_layer_11_digital_assets():
    assets = DigitalAssetManager().retrieve_verified_assets("kohler.com", "K-596-BL")
    assert len(assets["images"]) > 0
    assert len(assets["pdfs"]) > 0
    assert "kohler.com" in assets["images"][0]


def test_layer_12_benchmark_evaluator():
    evaluator = BenchmarkEvaluator()
    rec = EnrichedProductRecord(
        row_id="1",
        mpn="K-596",
        canonical_manufacturer="Kohler",
        overall_status=StatusTag.AUTO_APPROVED,
        overall_confidence=0.95,
        lov_conformance_pct=100.0,
        provenance_coverage_pct=100.0,
    )
    metrics = evaluator.evaluate_batch([rec])
    assert metrics["total_records"] == 1
    assert metrics["auto_approved_rate_pct"] == 100.0
    assert metrics["avg_lov_conformance_pct"] == 100.0
