import re
from backend.mlmodel.name_ranker import name_score

def extract_name(sentence: str):
    """Return most likely name in a sentence."""
    words = re.findall(r"[A-Za-z]+", sentence)
    if not words:
        return None

    # Score all words
    scored = [(w, name_score(w)) for w in words]

    # Pick highest-scoring word
    best_word, best_score = max(scored, key=lambda x: x[1])

    # Debug (optional)
    # print("DEBUG SCORES:", scored)
    # print("BEST:", best_word, best_score)

    # Threshold check
    if best_score >= 0.4:     # <= IMPORTANT FIX
        return best_word

    return None
