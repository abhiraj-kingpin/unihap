"""
Layer 3: Knowledge Graph
Models Classpath -> Attribute -> AllowedValue -> UOM relationships and
many-to-one synonym edges (e.g. 1,472 connection types -> 515 canonical).
Uses NetworkX for high-speed in-memory graph operations with Neo4j compatibility.
"""

from typing import List, Dict, Set, Optional
import networkx as nx
from unihap.core.logging import logger


class TaxonomyGraph:
    """In-memory Knowledge Graph for attribute schemas and canonical mappings."""

    def __init__(self):
        self.graph = nx.DiGraph()
        self._build_default_schema()

    def _build_default_schema(self):
        """Initializes standard plumbing domain taxonomy and LOVs."""
        # Classpath: Kitchen Faucets
        cp_kitchen = "Plumbing > Faucets > Kitchen Faucets"
        self.graph.add_node(cp_kitchen, type="classpath")

        attributes = {
            "Finish": ["Chrome", "Matte Black", "Stainless Steel", "Brushed Nickel", "Oil Rubbed Bronze", "Polished Brass"],
            "Handle Count": ["1", "2", "3"],
            "Flow Rate": ["1.5 GPM", "1.8 GPM", "2.2 GPM"],
            "Installation Type": ["Deck Mount", "Wall Mount", "Single Hole", "Centerset"],
            "Material": ["Brass", "Stainless Steel", "Zinc Alloy", "Plastic"],
            "Spout Reach": ["8 in", "8.5 in", "9 in", "9.5 in", "10 in"],
        }

        for attr, allowed_values in attributes.items():
            self.graph.add_node(attr, type="attribute")
            self.graph.add_edge(cp_kitchen, attr, relationship="HAS_ATTRIBUTE")

            for val in allowed_values:
                self.graph.add_node(val, type="allowed_value")
                self.graph.add_edge(attr, val, relationship="ALLOWS_VALUE")

        # Synonyms / Mappings (Many-to-one)
        synonyms = [
            ("SS", "Stainless Steel"),
            ("Stnlss Stl", "Stainless Steel"),
            ("MB", "Matte Black"),
            ("Blk", "Matte Black"),
            ("BN", "Brushed Nickel"),
            ("1-Handle", "1"),
            ("Single Handle", "1"),
            ("2-Handle", "2"),
            ("Double Handle", "2"),
            ("1.8gpm", "1.8 GPM"),
            ("1.5gpm", "1.5 GPM"),
        ]
        for syn, canon in synonyms:
            self.graph.add_node(syn, type="synonym")
            self.graph.add_edge(syn, canon, relationship="CANONICAL_SYNONYM")

    def get_allowed_attributes(self, classpath: str) -> List[str]:
        """Returns the list of valid attributes for a given Classpath."""
        if classpath in self.graph:
            return [
                target for _, target, data in self.graph.out_edges(classpath, data=True)
                if data.get("relationship") == "HAS_ATTRIBUTE"
            ]
        return ["Finish", "Material", "Installation Type", "Flow Rate"]

    def get_allowed_values(self, attribute: str) -> List[str]:
        """Returns the controlled LOV values for an attribute."""
        if attribute in self.graph:
            return [
                target for _, target, data in self.graph.out_edges(attribute, data=True)
                if data.get("relationship") == "ALLOWS_VALUE"
            ]
        return []

    def canonicalize_synonym(self, raw_value: str) -> Optional[str]:
        """Traverses synonym edges to return the canonical LOV value if present."""
        if raw_value in self.graph:
            for _, target, data in self.graph.out_edges(raw_value, data=True):
                if data.get("relationship") == "CANONICAL_SYNONYM":
                    return target
        return None
