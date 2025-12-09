"""Shared spaCy utilities for the meeting task extraction pipeline."""
from functools import lru_cache
from typing import Optional

import spacy
from spacy.language import Language


@lru_cache(maxsize=1)
def get_nlp() -> Language:
    """Load the spaCy English model once and reuse it across modules."""
    try:
        return spacy.load("en_core_web_sm")
    except OSError as exc:  # pragma: no cover - provides actionable error for developers
        raise RuntimeError(
            "spaCy model 'en_core_web_sm' is not installed. "
            "Run `python -m spacy download en_core_web_sm` before starting the API."
        ) from exc


def ensure_doc(text: str) -> Optional[Language]:
    """Helper kept for backwards compatibility; preferred direct get_nlp usage."""
    if not text or not text.strip():
        return None
    return get_nlp()(text)
