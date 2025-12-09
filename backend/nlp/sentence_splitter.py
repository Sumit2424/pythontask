"""Sentence splitting utilities for meeting transcripts."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List
import re

from .spacy_utils import get_nlp

_SENTENCE_MIN_CHARS = 8
_SPLIT_REGEX = re.compile(r"(?<=[.!?])\s+|\n")


@dataclass
class SentenceSplitter:
    """Split transcripts into clean, non-empty sentences using spaCy first."""

    enforce_min_length: bool = True

    def __post_init__(self) -> None:
        self._nlp = get_nlp()

    def split(self, transcript: str) -> List[str]:
        if not transcript:
            return []

        doc = self._nlp(transcript)
        sentences = [sent.text.strip() for sent in doc.sents if sent.text.strip()]

        if not sentences:
            sentences = [part.strip() for part in _SPLIT_REGEX.split(transcript) if part.strip()]

        if self.enforce_min_length:
            sentences = [s for s in sentences if len(s) >= _SENTENCE_MIN_CHARS]

        return sentences

    def split_many(self, transcripts: Iterable[str]) -> List[str]:
        sentences: List[str] = []
        for block in transcripts:
            sentences.extend(self.split(block))
        return sentences
