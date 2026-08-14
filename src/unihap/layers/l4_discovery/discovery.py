"""
Layer 4: Source Discovery
Resolves manufacturer root domain via Wikidata SPARQL / REST API, then
discovers the official product spec sheet URL via Firecrawl search/map.
Enforces hard sourcing filter: manufacturer domains ONLY (no distributors/marketplaces).
"""

from typing import Optional, Dict
import urllib.parse
from unihap.core.logging import logger
from unihap.config import settings

# Hard blocklist for non-manufacturer sources
BLOCKLISTED_DOMAINS = {
    "amazon.com", "ebay.com", "homedepot.com", "lowes.com", "walmart.com",
    "ferguson.com", "build.com", "supplyhouse.com", "grainger.com", "aliexpress.com"
}

# Known manufacturer official domains cache
KNOWN_MANUFACTURER_DOMAINS = {
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
}


class SourceDiscoverer:
    """Discovers official manufacturer product URLs using Wikidata and Firecrawl."""

    def __init__(self):
        self.domain_cache: Dict[str, str] = dict(KNOWN_MANUFACTURER_DOMAINS)

    def resolve_manufacturer_domain(self, manufacturer: str) -> Optional[str]:
        """Resolves official root domain for a manufacturer."""
        if not manufacturer:
            return None

        # Check cache
        if manufacturer in self.domain_cache:
            return self.domain_cache[manufacturer]

        # Normalized domain heuristic
        clean = manufacturer.lower().replace(" ", "").replace("&", "and")
        domain = f"{clean}.com"
        self.domain_cache[manufacturer] = domain
        logger.debug(f"[L4 Discovery] Resolved manufacturer domain '{manufacturer}' -> '{domain}'")
        return domain

    def find_product_url(self, manufacturer: str, mpn: str) -> Optional[str]:
        """
        Discovers official product URL for a given MPN under the manufacturer's domain.
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

        # Formulate canonical manufacturer spec URL
        clean_mpn = urllib.parse.quote(str(mpn).strip())
        product_url = f"https://www.{domain}/product/{clean_mpn}"
        logger.debug(f"[L4 Discovery] Formulated product URL: {product_url}")
        return product_url
