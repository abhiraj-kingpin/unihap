"""
UniHAP Global Configuration and Settings using Pydantic Settings.
"""

import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

# Base Directory paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
LOOKUP_DIR = DATA_DIR / "lookup_tables"


class Settings(BaseSettings):
    """Global configuration settings for UniHAP pipeline."""
    model_config = SettingsConfigDict(
        env_file=str(PROJECT_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Environment
    unihap_env: str = Field(default="development", alias="UNIHAP_ENV")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    # API Keys & Endpoints
    groq_api_key: str | None = Field(default=None, alias="GROQ_API_KEY")
    groq_model: str = Field(default="llama-3.3-70b-versatile", alias="GROQ_MODEL")

    ollama_base_url: str = Field(default="http://localhost:11434", alias="OLLAMA_BASE_URL")
    ollama_model: str = Field(default="gemma3:4b", alias="OLLAMA_MODEL")

    firecrawl_api_key: str | None = Field(default=None, alias="FIRECRAWL_API_KEY")
    wikidata_user_agent: str = Field(
        default="UniHAP-CatalogBot/1.0 (contact@unihap.local)",
        alias="WIKIDATA_USER_AGENT"
    )

    # Knowledge Graph
    neo4j_uri: str | None = Field(default=None, alias="NEO4J_URI")
    neo4j_user: str | None = Field(default=None, alias="NEO4J_USER")
    neo4j_password: str | None = Field(default=None, alias="NEO4J_PASSWORD")

    # Local Models
    embedding_model_name: str = "all-MiniLM-L6-v2"

    # Confidence Thresholds
    confidence_auto_approve: float = Field(default=0.90, alias="CONFIDENCE_THRESHOLD_AUTO_APPROVE")
    confidence_needs_review: float = Field(default=0.70, alias="CONFIDENCE_THRESHOLD_NEEDS_REVIEW")


settings = Settings()
