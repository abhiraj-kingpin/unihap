"""
UniHAP — Enterprise Product Intelligence & Attribute Enrichment Pipeline
12-layer evidence-grounded architecture for high-precision catalog enrichment.
"""

__version__ = "0.1.0"
__author__ = "Mani Joshi"

from unihap.pipeline import UniHAPPipeline
from unihap.core.models import ProductRecord, EnrichedProductRecord, PipelineResult

__all__ = [
    "UniHAPPipeline",
    "ProductRecord",
    "EnrichedProductRecord",
    "PipelineResult",
    "__version__",
]
