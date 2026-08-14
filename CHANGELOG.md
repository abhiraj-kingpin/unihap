# Changelog

All notable changes to the **UniHAP** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.1.0] - 2026-08-14

### Initial Release — 12-Layer Product Intelligence & Attribute Enrichment Pipeline

#### 🏛️ Core Architecture & Pipeline
- **Layer 0 (Ingest & Normalize)**: Robust Excel/CSV ingestion engine resolving merged cells, multi-row headers, and stripping noisy placeholder strings (`-- Unbranded --`, `N/A`, `NULL`, `none`) into clean nullable types.
- **Layer 1 (Entity Resolution)**: Fuzzy string matching (`rapidfuzz`) and semantic embeddings (`sentence-transformers`) resolving noisy manufacturer and brand names against a canonical dictionary.
- **Layer 2 (3-Stage Classification Funnel)**: Hierarchical Classpath resolution (Department > Class > Fine Category) utilizing instant keyword lookups, cosine similarity on taxonomy embeddings, and LLM tie-breaks.
- **Layer 3 (Knowledge Graph Schema)**: In-memory `NetworkX` graph modeling `Classpath -> Attribute -> AllowedValue -> UOM` schemas and many-to-one synonym edges (e.g. connection types, materials, finishes).
- **Layer 4 (Source Discovery)**: Official manufacturer root domain resolution (via Wikidata API) and product spec URL discovery (via Firecrawl search/map) with strict domain blocklisting for third-party marketplaces and distributors.
- **Layer 5 (Document Intelligence)**: Web scraping interface using `Crawl4AI` (Playwright/Chromium) for clean Markdown/table extraction, paired with multimodal VLM inspection for scanned drawings and nameplates.
- **Layer 6 (Constrained Attribute Extraction)**: Constrained RAG architecture extracting List of Values (LOV) attributes paired with mandatory `evidence_span` provenance strings. Implements strict **ABSTAIN** rule to eliminate hallucinations.
- **Layer 7 (Deterministic Normalization)**: Pure Python unit of measure (UOM) and fraction-to-decimal standardizers backed by static lookup tables (`~500` UOM rules, `63` fraction entries).
- **Layer 8 (Description Synthesis)**: Template-based synthesis generating 5 compliant e-commerce formats (`Invoice <= 40 CAPS`, `Mobile 60-80`, `Short Title`, `Long Narrative`, `Retail Bullet Points`) strictly from validated attributes.
- **Layer 9 (Validation & Confidence Engine)**: Pydantic v2 validation engine calculating LOV conformance, provenance coverage, character limit adherence, and assigning status tags (`auto-approved`, `needs-review`, `rejected`).
- **Layer 10 (Human-in-the-Loop Review Queue)**: Triage queue interface managing ambiguous items with source diff views and human correction feedback loops.
- **Layer 11 (Digital Assets Pipeline)**: Discovery and linkage of verified manufacturer high-resolution imagery and PDF specification sheets.
- **Layer 12 (Benchmark & Evaluation)**: Precision scoring engine evaluating predictions against ground-truth benchmarks across field accuracy, fill rates, and confidence-tier distributions.

#### 🛠️ Tooling, CLI & UI
- **Python Runtime**: Built for **Python 3.11+** with fast, reproducible environment locking via **`uv`**.
- **Typer & Rich CLI**: Interactive terminal commands (`unihap run`, `unihap ui`, `unihap info`).
- **Streamlit Review Dashboard**: Interactive web UI (`src/unihap/ui/app.py`) for catalog curators to inspect provenance and approve corrections.
- **Test Suite**: Automated `pytest` suite validating normalization, ingestion, and end-to-end 12-layer pipeline execution.
