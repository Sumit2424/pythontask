import re
from backend.mlmodel.name_ranker import name_score


def extract_name(sentence: str):
    words = re.findall(r"[A-Za-z]+", sentence)

    if not words:
        return None

    scored = [(w, name_score(w)) for w in words]
    best_word, best_score = max(scored, key=lambda x: x[1])
    if best_score >= 0.4:
        return best_word
    return None