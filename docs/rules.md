# UniHAP Team & Contribution Rules

This document defines the engineering standards, architectural invariants, git workflow, and collaboration rules for all contributors and agents working on the **UniHAP** repository.

---

## 🏛️ 1. Core Architectural Invariants (Non-Negotiable)

1. **Zero-Hallucination Mandate**:
   - An LLM or extraction layer may **NEVER** generate a product attribute, specification, or factual claim from raw weights without citable proof.
   - Every extracted attribute must be accompanied by an exact `evidence_span` and official `source_url`.
   - If no direct source text span exists, the extractor **MUST ABSTAIN** (`status: abstained`). Unbacked hallucinated guesses are explicitly penalized.

2. **Hard Manufacturer Sourcing Rule**:
   - All external data, URLs, and specifications must originate from **official manufacturer domains only** (resolved via Wikidata / official sites).
   - Third-party marketplaces and distributor domains (`amazon.com`, `ebay.com`, `homedepot.com`, `lowes.com`, `ferguson.com`, `build.com`, `grainger.com`, etc.) are hard-blocklisted in code and must never be used as ground truth.

3. **Controlled Vocabulary (LOV) Conformance**:
   - Extracted and normalized attribute values must strictly map to the controlled List of Values (LOV) defined in the Knowledge Graph (`src/unihap/layers/l3_knowledge_graph/graph.py`).
   - Synonyms must be mapped to canonical forms using many-to-one graph edges rather than arbitrary ad-hoc strings.

4. **Deterministic Normalization**:
   - Unit of measure (UOM) abbreviations, fraction-to-decimal conversions, and description formatting must remain 100% deterministic (lookup tables in `data/lookup_tables/`), not delegated to non-deterministic LLM prompts.

---

## 🌿 2. Git & Collaboration Workflow

1. **Branching Model**:
   - Direct pushes to `main` are restricted. All work must be developed on feature branches:
     - `feat/<feature-name>` (e.g. `feat/wikidata-sparql-cache`)
     - `fix/<bug-name>` (e.g. `fix/uom-fraction-regex`)
     - `docs/<topic>` (e.g. `docs/evaluation-guide`)
     - `data/<dataset>` (e.g. `data/add-fittings-taxonomy`)
2. **Commit Conventions**:
   - Use [Conventional Commits](https://www.conventionalcommits.org/):
     - `feat:` New layer, feature, or capability
     - `fix:` Bug fix or regex correction
     - `docs:` Documentation updates
     - `test:` Adding or updating unit/integration tests
     - `refactor:` Code restructuring without behavior changes
     - `perf:` Performance or latency optimizations
3. **Pull Request Requirements**:
   - Every PR must include:
     - Clear description of the change and affected layers (L0 – L12).
     - Test evidence showing passing `uv run pytest`.
     - Impact analysis on benchmark accuracy / LOV conformance if taxonomy or normalizers were modified.

---

## ⚙️ 3. Environment & Tooling Standards

1. **Package Management with `uv`**:
   - **`uv` is the mandatory package and virtual environment manager.**
   - Do **NOT** use raw `pip install`, `pip-compile`, or `poetry`.
   - Add new dependencies using:
     ```bash
     uv add <package_name>
     # Or for dev dependencies:
     uv add --dev <package_name>
     ```
   - Always commit both `pyproject.toml` and `uv.lock`.
2. **Python 3.11+ Standards**:
   - Use strict type hints (`typing.Optional`, `typing.List`, `typing.Dict`, union syntax `str | None`).
   - All inter-layer data transfer must use Pydantic v2 schemas defined in `src/unihap/core/models.py`.
3. **Automated Testing**:
   - All PRs must pass the test suite:
     ```bash
     uv run pytest
     ```
   - New layers, normalizers, or exporters must include corresponding unit tests under `tests/`.

---

## 🔒 4. Security, Credentials & Data Privacy

1. **API Keys & Secrets**:
   - Never commit `.env` files, API keys (`GROQ_API_KEY`, `FIRECRAWL_API_KEY`), or sensitive tokens to git.
   - Use `.env.example` as the canonical template for required environment variables.
2. **Client Catalog Data**:
   - Proprietary supplier raw catalogs placed in `data/raw/` must adhere to client data-governance policies.
   - Cached scraping artifacts must remain in `.gitignore`-tracked locations (`data/cache/`, `data/temp/`).

---

## 📊 5. Evaluation & Quality Gates

Before merging any layer updates to `main`:
1. **Schema Check**: Output must pass `DeliveryFormatExporter` validation (all 252 columns intact).
2. **LOV Conformance Gate**: LOV conformance rate must not regress on the 200-row ground truth.
3. **Provenance Gate**: Provenance coverage must maintain 100% verifiable source links for all non-null attributes.
