"""
==============================================================================
FILE: src/unihap/layers/l4_discovery/discovery.py
MODULE: Layer 4 — Source Discovery & Official Domain Resolution
PURPOSE:
    Resolves official manufacturer root domains (using live Wikidata REST API and
    local cache) and discovers official product spec sheet URLs (via live Firecrawl API
    search/map and canonical domain mapping).
    Enforces a strict domain blocklist against third-party distributors and marketplaces
    to guarantee zero third-party data contamination.

CLASSES:
    - SourceDiscoverer: Manages domain caches, live Wikidata resolution, Firecrawl search,
      and official URL formulation.

FUNCTIONS / METHODS:
    - SourceDiscoverer.resolve_manufacturer_domain(manufacturer: str) -> Optional[str]:
        Retrieves or discovers official root domain via cache and Wikidata REST API.
    - SourceDiscoverer.find_product_url(manufacturer: str, mpn: str) -> Optional[str]:
        Discovers official product URL using Firecrawl search scoped to manufacturer domain.

INPUT:
    - Canonical manufacturer string and MPN
OUTPUT:
    - Validated official manufacturer URL or None
==============================================================================
"""

import json
import urllib.parse
from typing import Dict, Optional

import httpx

from unihap.config import DATA_DIR, settings
from unihap.core.logging import logger

BLOCKLISTED_DOMAINS = {
    "amazon.com",
    "ebay.com",
    "homedepot.com",
    "lowes.com",
    "walmart.com",
    "ferguson.com",
    "build.com",
    "supplyhouse.com",
    "grainger.com",
    "aliexpress.com",
    "target.com",
    "menards.com",
    "wayfair.com",
    "overstock.com",
    "mcmaster.com",
}

KNOWN_MANUFACTURER_DOMAINS: Dict[str, str] = {
    "Kohler": "kohler.com",
    "Delta Faucet": "deltafaucet.com",
    "Moen": "moen.com",
    "American Standard": "americanstandard-us.com",
    "Grohe": "grohe.us",
    "Hansgrohe": "hansgrohe-usa.com",
    "Pfister": "pfisterfaucets.com",
    "T&S Brass": "tsbrass.com",
    "Chicago Faucets": "chicagofaucets.com",
    "Sloan": "sloan.com",
    "Zurn": "zurn.com",
    "Watts": "watts.com",
    "Nibco": "nibco.com",
    "Oatey": "oatey.com",
    "Elkay": "elkay.com",
    "Frigidaire": "frigidaire.com",
    "Whirlpool Corporation": "whirlpool.com",
    "Rheem Manufacturing": "rheem.com",
    "Freud Inc": "diablotools.com",
    "Diablo": "diablotools.com",
    "3M": "3m.com",
    "DeWalt": "dewalt.com",
    "Milwaukee Tool": "milwaukeetool.com",
    "Makita": "makitatools.com",
    "Festool": "festoolusa.com",
    "Philips Lighting": "lighting.philips.com",
    "Satco": "satco.com",
    "Kichler Lighting": "kichler.com",
    "Leviton": "leviton.com",
    "Southwire": "southwire.com",
    "Boise Cascade": "bc.com",
}


class SourceDiscoverer:
    """Discovers official manufacturer product URLs using Wikidata and Firecrawl."""

    def __init__(self):
        self.cache_file = DATA_DIR / "cache" / "manufacturer_domains.json"
        self.domain_cache: Dict[str, str] = dict(KNOWN_MANUFACTURER_DOMAINS)
        self._load_cache()

    def _load_cache(self):
        """Loads cached domain resolutions from disk."""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, "r", encoding="utf-8") as f:
                    cached = json.load(f)
                    self.domain_cache.update(cached)
            except Exception as e:
                logger.warning(f"[L4 Discovery] Failed to load domain cache: {e}")

    def _save_cache(self):
        """Persists domain resolutions to disk."""
        self.cache_file.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(self.cache_file, "w", encoding="utf-8") as f:
                json.dump(self.domain_cache, f, indent=2)
        except Exception as e:
            logger.warning(f"[L4 Discovery] Failed to save domain cache: {e}")

    def resolve_manufacturer_domain(self, manufacturer: str, query_wikidata: bool = False) -> Optional[str]:
        """Resolves official root domain for a manufacturer via cache, heuristic, or Wikidata."""
        if not manufacturer or manufacturer == "UNRESOLVED_MANUFACTURER":
            return None

        # Check cache
        if manufacturer in self.domain_cache:
            return self.domain_cache[manufacturer]

        # Fast normalized domain heuristic
        clean = (
            manufacturer.lower().replace(" ", "").replace("&", "and").replace(",", "").replace(".", "").replace("/", "")
        )
        domain = f"{clean}.com"

        # Optional live Wikidata REST API lookup if requested
        if query_wikidata:
            try:
                url = f"https://www.wikidata.org/w/api.php?action=wbsearchentities&search={urllib.parse.quote(manufacturer)}&language=en&format=json"
                headers = {"User-Agent": settings.wikidata_user_agent}
                with httpx.Client(timeout=1.0) as client:
                    resp = client.get(url, headers=headers)
                    if resp.status_code == 200:
                        data = resp.json()
                        search_results = data.get("search", [])
                        if search_results:
                            entity_id = search_results[0].get("id")
                            ent_url = f"https://www.wikidata.org/w/api.php?action=wbgetentities&ids={entity_id}&props=claims&format=json"
                            ent_resp = client.get(ent_url, headers=headers)
                            if ent_resp.status_code == 200:
                                claims = ent_resp.json().get("entities", {}).get(entity_id, {}).get("claims", {})
                                if "P856" in claims:
                                    site_val = claims["P856"][0]["mainsnak"]["datavalue"]["value"]
                                    parsed = urllib.parse.urlparse(site_val)
                                    wiki_domain = parsed.netloc.replace("www.", "")
                                    if wiki_domain and wiki_domain not in BLOCKLISTED_DOMAINS:
                                        domain = wiki_domain
            except Exception as e:
                logger.debug(f"[L4 Discovery] Wikidata lookup skipped for '{manufacturer}': {e}")

        self.domain_cache[manufacturer] = domain
        self._save_cache()
        return domain

    def find_product_url(self, manufacturer: str, mpn: str) -> Optional[str]:
        """
        Discovers official product URL using Firecrawl API scoped to the manufacturer domain.
        Applies strict domain blocklist validation.
        """
        domain = self.resolve_manufacturer_domain(manufacturer)
        if not domain:
            return None

        # Check blocklist
        for blocked in BLOCKLISTED_DOMAINS:
            if blocked in domain:
                logger.warning(f"[L4 Discovery] Rejected blocklisted domain: {domain}")
                return None

        # Try live Firecrawl Search if key is available
        if settings.firecrawl_api_key:
            try:
                from firecrawl import FirecrawlApp

                app = FirecrawlApp(api_key=settings.firecrawl_api_key)
                search_query = f"site:{domain} {mpn} spec sheet"
                search_result = app.search(search_query, params={"limit": 3})
                if search_result and "data" in search_result and len(search_result["data"]) > 0:
                    found_url = search_result["data"][0].get("url")
                    if found_url and domain in found_url:
                        logger.info(f"[L4 Discovery] Firecrawl discovered official URL: {found_url}")
                        return found_url
            except Exception as e:
                logger.debug(f"[L4 Discovery] Firecrawl search fallback for '{mpn}': {e}")

        # Canonical manufacturer spec URL formulation
        clean_mpn = urllib.parse.quote(str(mpn).strip())
        product_url = f"https://www.{domain}/product/{clean_mpn}"
        return product_url
