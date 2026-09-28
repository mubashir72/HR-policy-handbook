"""Application configuration and secret loading."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Mapping

from dotenv import load_dotenv

DEFAULT_GROQ_MODEL = "openai/gpt-oss-20b"
MAX_UPLOAD_BYTES = 20 * 1024 * 1024
MAX_EXTRACTED_CHARACTERS = 1_500_000
RETRIEVAL_TOP_K = 4


@dataclass(frozen=True)
class AppConfig:
    groq_api_key: str | None
    groq_model: str


def _secret_value(secrets: Mapping[str, Any] | None, name: str) -> str | None:
    if not secrets:
        return None
    value = secrets.get(name)
    return str(value).strip() if value else None


def load_config(secrets: Mapping[str, Any] | None = None) -> AppConfig:
    """Load non-persistent configuration from environment or Streamlit secrets."""
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY", "").strip() or _secret_value(secrets, "GROQ_API_KEY")
    model = (
        os.getenv("GROQ_MODEL", "").strip()
        or _secret_value(secrets, "GROQ_MODEL")
        or DEFAULT_GROQ_MODEL
    )
    return AppConfig(groq_api_key=api_key or None, groq_model=model)
