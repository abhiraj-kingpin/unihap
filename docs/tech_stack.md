# UniHAP Tech Stack & Requirements

## Core Pipeline & Language
- **Python 3.11+**
- **uv 0.12+** (Package & environment manager)

## Data Processing & Normalization
- `pandas` (2.2+)
- `openpyxl` (3.1+)

## Matching & Classification
- `rapidfuzz` (3.9+)
- `sentence-transformers` (3.0+, `all-MiniLM-L6-v2`)
- `networkx` (3.3+)
- Optional: `neo4j` (5.0+)

## LLM & Inference Tier
- `groq` (0.9+, `llama-3.3-70b-versatile`)
- `ollama` (`gemma3:4b`)

## Scraping & Discovery
- `firecrawl-py` (1.0+)
- `crawl4ai` (0.3+)
- `requests` / `httpx`
- `Wikidata REST / SPARQL API`

## Validation, CLI & Dashboard
- `pydantic` (2.7+) & `pydantic-settings`
- `typer` (0.12+)
- `rich` (13.7+)
- `streamlit` (1.35+)
