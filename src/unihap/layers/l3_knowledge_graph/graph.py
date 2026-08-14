"""
==============================================================================
FILE: src/unihap/layers/l3_knowledge_graph/graph.py
MODULE: Layer 3 — Knowledge Graph & LOV Schema Modeling
PURPOSE:
    Represents catalog taxonomy schemas as a directed property graph using NetworkX.
    Models relationships:
      - (Classpath) -[:HAS_ATTRIBUTE]-> (Attribute)
      - (Attribute) -[:ALLOWS_VALUE]-> (AllowedValue)
      - (Synonym) -[:CANONICAL_SYNONYM]-> (AllowedValue)
    Provides canonical synonym traversal to map thousands of vendor variants
    (e.g., 'SS', 'Stnlss Stl' -> 'Stainless Steel') to strictly controlled LOVs.

CLASSES:
    - TaxonomyGraph: Directed graph modeling attributes, LOVs, and synonym bridges.

FUNCTIONS / METHODS:
    - TaxonomyGraph._build_default_schema(): Initializes standard plumbing, appliance, and tool nodes.
    - TaxonomyGraph.get_allowed_attributes(classpath: str) -> List[str]: Queries attributes for a classpath.
    - TaxonomyGraph.get_allowed_values(attribute: str) -> List[str]: Queries controlled LOV values for an attribute.
    - TaxonomyGraph.canonicalize_synonym(raw_value: str) -> Optional[str]: Traverses synonym edges to find canonical LOV.

INPUT:
    - Classpath string or raw attribute value string
OUTPUT:
    - Lists of allowed attributes / values or canonicalized string
==============================================================================
"""

from typing import List, Optional

import networkx as nx


class TaxonomyGraph:
    """In-memory Knowledge Graph for attribute schemas and canonical mappings."""

    def __init__(self):
        self.graph = nx.DiGraph()
        self._build_default_schema()

    def _build_default_schema(self):
        """Initializes standard multi-category taxonomy and LOVs."""
        # 1. Kitchen Faucets
        cp_kitchen = "Plumbing > Faucets > Kitchen Faucets"
        self.graph.add_node(cp_kitchen, type="classpath")

        attributes_faucets = {
            "Finish": [
                "Chrome",
                "Matte Black",
                "Stainless Steel",
                "Brushed Nickel",
                "Oil Rubbed Bronze",
                "Polished Brass",
            ],
            "Handle Count": ["1", "2", "3"],
            "Flow Rate": ["1.5 GPM", "1.8 GPM", "2.2 GPM"],
            "Installation Type": ["Deck Mount", "Wall Mount", "Single Hole", "Centerset"],
            "Material": ["Brass", "Stainless Steel", "Zinc Alloy", "Plastic"],
            "Spout Reach": ["8 in", "8.5 in", "9 in", "9.5 in", "10 in"],
        }

        for attr, allowed_values in attributes_faucets.items():
            self.graph.add_node(attr, type="attribute")
            self.graph.add_edge(cp_kitchen, attr, relationship="HAS_ATTRIBUTE")
            for val in allowed_values:
                self.graph.add_node(val, type="allowed_value")
                self.graph.add_edge(attr, val, relationship="ALLOWS_VALUE")

        # 2. Appliances: Dishwashers
        cp_dishwasher = "Appliances > Large Appliances > Dishwashers"
        self.graph.add_node(cp_dishwasher, type="classpath")
        attributes_dishwasher = {
            "Series": ["Professional Series", "Eco Series", "Gallery Series"],
            "Number of Wash Cycles": ["3", "4", "5", "6", "8"],
            "Voltage Rating": ["120 V", "240 V"],
            "Amperage Rating": ["10 A", "15 A", "20 A"],
            "Mounting Type": ["Built-in Mounting", "Leg Mounting", "Freestanding"],
            "Sound Level": ["41 dBA", "44 dBA", "47 dBA", "50 dBA"],
        }
        for attr, allowed_values in attributes_dishwasher.items():
            self.graph.add_node(attr, type="attribute")
            self.graph.add_edge(cp_dishwasher, attr, relationship="HAS_ATTRIBUTE")
            for val in allowed_values:
                self.graph.add_node(val, type="allowed_value")
                self.graph.add_edge(attr, val, relationship="ALLOWS_VALUE")

        # 3. Tools: Sanding Belts
        cp_sanding = "Tools > Abrasives & Sanding > Sanding Belts"
        self.graph.add_node(cp_sanding, type="classpath")
        attributes_sanding = {
            "Grit": ["P60", "P80", "P120", "P150", "P220"],
            "Belt Width": ["0.5 in", "1 in", "3 in", "4 in"],
            "Belt Length": ["18 in", "21 in", "24 in"],
            "Abrasive Material": ["Ceramic", "Aluminum Oxide", "Zirconia Alumina"],
        }
        for attr, allowed_values in attributes_sanding.items():
            self.graph.add_node(attr, type="attribute")
            self.graph.add_edge(cp_sanding, attr, relationship="HAS_ATTRIBUTE")
            for val in allowed_values:
                self.graph.add_node(val, type="allowed_value")
                self.graph.add_edge(attr, val, relationship="ALLOWS_VALUE")

        # Many-to-one Synonyms
        synonyms = [
            ("SS", "Stainless Steel"),
            ("SST", "Stainless Steel"),
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
            ("120", "120 V"),
            ("120V", "120 V"),
            ("15", "15 A"),
            ("15A", "15 A"),
            ("10A", "10 A"),
            ("41DBA", "41 dBA"),
            ("47 dba", "47 dBA"),
            ("1/2 in", "0.5 in"),
            ('1/2"', "0.5 in"),
            ("18 in", "18 in"),
            ('18"', "18 in"),
        ]
        for syn, canon in synonyms:
            self.graph.add_node(syn, type="synonym")
            self.graph.add_edge(syn, canon, relationship="CANONICAL_SYNONYM")

    def get_allowed_attributes(self, classpath: str) -> List[str]:
        """Returns the list of valid attributes for a given Classpath."""
        if classpath in self.graph:
            return [
                target
                for _, target, data in self.graph.out_edges(classpath, data=True)
                if data.get("relationship") == "HAS_ATTRIBUTE"
            ]
        # Default attribute set
        return ["Finish", "Material", "Installation Type", "Flow Rate", "Series", "Voltage Rating"]

    def get_allowed_values(self, attribute: str) -> List[str]:
        """Returns the controlled LOV values for an attribute."""
        if attribute in self.graph:
            return [
                target
                for _, target, data in self.graph.out_edges(attribute, data=True)
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
