# src/ai_job_compass/skill_extractor.py

from __future__ import annotations

from typing import Set

import pandas as pd
import re


def build_skill_lexicon(skills_df: pd.DataFrame) -> dict:
    """
    Build a simple lexicon mapping normalized variants -> skill_id.
    Example:
        "python" -> 1
        "power bi" -> 11
    """
    lexicon = {}

    for sid, row in skills_df.iterrows():
        name = str(row["name"]).strip().lower()

        variants = {name}
        # remove extra punctuation / normalize spaces
        normalized = re.sub(r"[^a-z0-9]+", " ", name).strip()
        if normalized:
            variants.add(normalized)
        # no-space variant (e.g. "powerbi")
        variants.add(name.replace(" ", ""))

        for v in variants:
            if not v:
                continue
            lexicon[v] = sid

    return lexicon


def extract_skills_from_text(text: str, skills_df: pd.DataFrame) -> Set[int]:
    """
    Very simple skill extractor:
      - lowercase + strip punctuation
      - match single- and multi-word skill variants
    Returns: set of skill_ids detected in the text.
    """
    if not text:
        return set()

    text_norm = text.lower()
    text_norm = re.sub(r"[^a-z0-9]+", " ", text_norm)
    tokens = set(text_norm.split())

    lexicon = build_skill_lexicon(skills_df)
    found: Set[int] = set()

    for variant, sid in lexicon.items():
        parts = variant.split()
        if len(parts) == 1:
            # single word skill -> look in tokens
            if variant in tokens:
                found.add(sid)
        else:
            # multi-word skill -> look in normalized text
            if variant in text_norm:
                found.add(sid)

    return found
