# UniHAP Technical Architecture

## 1. Zero-Hallucination Pipeline Design

UniHAP enforces an absolute zero-hallucination constraint across all 12 layers:
1. **Controlled Vocabulary Enforcement**: Values must resolve to a valid List of Values (LOV) node in the Layer 3 Knowledge Graph.
2. **Mandatory Provenance Spans**: In Layer 6, the LLM must return the exact substring from the scraped manufacturer page (`evidence_span`). If no evidence span exists, the model must **ABSTAIN** rather than generate ungrounded values.
3. **Domain Blocklisting**: In Layer 4, marketplace and distributor domains are filtered out in code before any scraping occurs.

## 2. LLM Cascade Strategy
- **Tier 1 (Local)**: Ollama + Gemma 3 4B for quick classification tie-breaks and local taxonomy mapping (<1k token prompts).
- **Tier 2 (Cloud)**: Groq LLaMA-3.3-70B for JSON-constrained attribute extraction and description synthesis.

## 3. Human-in-the-Loop Feedback Loop
Items falling below the 90% confidence threshold enter the Layer 10 Review Queue. Human corrections are saved and continuously update the few-shot PatternRAG cache for subsequent runs.
