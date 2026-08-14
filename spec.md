# UniHAP — Product Intelligence Enrichment Pipeline 

## Thesis
LLM-written copy from thin data = confident, ungrounded content (explicitly scored zero by brief). Design constraint: LLM may only (a) pick from a controlled vocabulary, (b) cite a retrieved source span, or (c) abstain → human review. No layer generates facts without evidence.

## Pipeline (12 layers)

| # | Layer | Function | Tooling | Cost |
|---|-------|----------|---------|------|
| 0 | Ingest/Normalize | Parse messy XLSX (merged cells, multi-row headers); strip placeholders (`-- Unbranded --` etc.) to null | Python/pandas | Free |
| 1 | Entity Resolution | Fuzzy-match `Part_Manuf`/brand → canonical `MANUFACTURER_NAME`/`BRAND_NAME` (27k-row list) | rapidfuzz + sentence-transformers embeddings, local | Free |
| 2 | Classification | Description → Classpath (Dept>Class>Fine). 3-stage funnel: (a) keyword match vs LOV leaf/attribute names — free, instant; (b) local embedding cosine similarity, top-3 candidates — free; (c) LLM tie-break only on ambiguous cases (~10-20% of rows) | Local embeddings + Groq LLM (see LLM tier below) | Mostly free |
| 3 | Knowledge Graph | Classpath→Attribute→AllowedValue→UOM edges; many-to-one mappings (1,472 connection types→515 canonical; 464 materials→113 canonical) as graph, not flat lookups | Neo4j or NetworkX | Free |
| 4 | Source Discovery | Resolve manufacturer root domain, then find product/spec page for MPN | See Discovery stack below | Low |
| 5 | Document Intelligence | Fetch page → clean Markdown/tables; VLM pass for scanned/image-only specs, nameplates | Crawl4AI (self-hosted scrape) + VLM for images | Free (+compute) |
| 6 | Attribute Extraction (constrained RAG) | Per allowed attribute: retrieve (a) source spans, (b) similar already-enriched rows (few-shot/PatternRAG) → LLM emits LOV-only value + mandatory `evidence_span`; no span match = abstain | Groq LLM, JSON-schema constrained | Low |
| 7 | Normalization | UOM (~500 abbrev table), fraction↔decimal (63-row table), house-style rules — deterministic, no LLM | Python lookup tables | Free |
| 8 | Description Synthesis | 5 formats (Invoice ≤40 CAPS, Mobile 60-80, Short/Title, Long, Retail) — template-filled from validated attributes only, never free generation from raw text | Templates + Groq for phrasing (Long/Retail only) | Low |
| 9 | Validation/Confidence | Per-field: schema valid? LOV-member? char-limit? provenance present? → `auto-approved` / `needs-review` / `rejected` | Python rules engine | Free |
| 10 | Human-in-the-Loop | Review queue for flagged fields w/ source diff; corrections feed back into L6 few-shot store + L1/L2 rules | Simple UI | Free |
| 11 | Digital Assets | Manufacturer-only image/spec-sheet retrieval; VLM verifies image matches part before accepting; enforce filename convention | Crawl4AI + VLM | Low |
| 12 | Evaluation | Field accuracy vs 200-row ground truth; % values in-LOV; char-limit compliance; required-attr fill rate; provenance coverage %; confidence-tier breakdown | Python | Free |

Sourcing rule (hard filter, all layers): manufacturer's own domain only. Marketplace/distributor domains blocklisted in code, never trusted to LLM self-policing.

## LLM Tier Strategy (cascade, cheapest first)
1. **Local Gemma 3 4B** (Ollama) — short-prompt, low-ambiguity calls only (e.g. simple classification tie-breaks, <~1k token prompts). Free, offline, data stays local (privacy angle for pitch). Known weakness: degrades on long (~2.5k+ token) instructions — do not use for attribute extraction.
2. **Groq (llama-3.3-70b-versatile)** — default for classification tie-break + attribute extraction + description phrasing. Free tier: 14,400 req/day, 500K tok/day (org-level) — sufficient for hackathon demo. Paid: $0.59/$0.79 per 1M in/out tokens; ~800 in / ~300 out tokens per row ≈ $0.0002-0.0004/row.
3. Escalate 1→2 only on low local-model confidence (validated pattern: Instacart's PARSE platform uses this exact cascade in production).

## Discovery Stack (Layer 4)
1. **Wikidata** (free, no key) — manufacturer name → official website property → root domain. Cache per manufacturer (few hundred–few thousand unique mfrs per catalog, not per-row).
2. **Firecrawl `search`** scoped `site:domain.com "<part number>"` — replaces unofficial DDGS scraping (flagged as production-fragile). 2 credits/10 results.
3. **Firecrawl `map`** on root domain if no direct hit (sitemap discovery).
4. Fallback: blank + `needs-manufacturer-source-review` flag. Never guess.

## Scrape Stack (Layer 5)
**Crawl4AI** (self-hosted, Apache-2.0, free) for page→Markdown once URL is known. Not a search tool — pairs with Firecrawl (discovery), doesn't replace it. Tradeoffs: self-hosted compute, may need proxies for anti-bot sites at scale, active security-patch cadence if running its Docker API (fine for local/demo use). **Action item: test hit-rate against a sample of the 200-row ground-truth manufacturer sites before committing at scale.**

## Cost Model (750k rows/month, steady-state)
| Component | Cost driver | Est. monthly |
|---|---|---|
| Clean/match/embed/classify (L0-3,7,9) | Local compute only | ~$10s |
| LLM calls (L2c,6,8) | Groq paid tier, tight prompts, batch mode | ~$75-150 |
| Discovery (L4) | Firecrawl search/map, cached per-manufacturer, only new/flagged SKUs need fresh lookup | ~$100s-low $1000s (not $1000s/mo — caching cuts a $3-4k worst-case ceiling by >80%) |
| Scrape (L5,11) | Crawl4AI self-hosted + occasional proxy cost | Infra only, no per-call fee |
| **Total** | | **~$200-2,000/mo** vs. ~500+ person-months/yr manual labor equivalent |

Two-mode note: hackathon demo can run 100% free (Wikidata+Firecrawl free tier+Crawl4AI+Groq free tier+local Gemma) on the 200-row ground truth; production swaps only the rate-limited pieces (Groq free→paid, Firecrawl free→paid tier) — cleaning/matching/classification/normalization layers are unchanged and were never the expensive part.

## Validation Against Prior Art
- **Walmart PAE**: separate extraction agent + separate QC/scoring agent; auto-ingest only above 90-95% per-attribute accuracy threshold → validates decoupling L6 (extract) from L9 (validate).
- **Instacart PARSE**: multi-modal (text+image) extraction, LLM cascade by confidence, entailment-style second pass ("is this value actually supported by evidence?") → validates L5 (VLM), LLM-tier cascade, and L6's `evidence_span` requirement.

## Evaluation Metrics (score against 200-row ground truth)
- Field-level exact/near-match accuracy
- % attribute values inside LOV vocabulary
- Character-limit/format/casing compliance per description field
- Fill rate on *required* attributes (not just any-attribute-filled)
- Provenance coverage: % filled fields with a real citable source
- Confidence-tier distribution (auto-approved/needs-review/rejected) per category

## Scope Recommendation
Depth over breadth (brief's own guidance). Build full 12-layer pipeline against **one fully-specified category (Faucets or Fittings)** on the 200-row ground truth first; widen to a slice of the 1000-row file with confidence flags, not forced answers, once L0-3/7/9 (deterministic layers) hit near-100% and L4-6/8 (LLM/retrieval layers) are measured honestly.

## Open Risk / Unverified
1. Crawl4AI scrape hit-rate on real long-tail manufacturer sites — untested, needs sample run.
2. Classpath accuracy at "Fine" granularity — no external benchmark for this specific taxonomy depth; mitigated by L9/L10 (confidence + human review), not assumed away.