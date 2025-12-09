import re
import spacy
from mlmodel.name_predictor import model, vectorizer

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

STOPWORDS = {
    "the","a","an","this","that","and","or","but","because","of","to","is","are",
    "we","you","they","he","she","it","in","on","for","with","at","by","as","please"
}

TECH_WORDS = {
    "ui","api","bug","database","server","deploy","performance",
    "frontend","backend","react","python","java","task","module","unit","login"
}

COMMON_VERBS = {
    "fix","update","create","design","optimize","write","build",
    "improve","implement","clean","add","remove","patch","test","write"
}

def preprocess(word):
    return re.sub(r"[^A-Za-z]", "", word)

def ml_prob(word):
    try:
        X = vectorizer.transform([word])
        return model.predict_proba(X)[0][1]
    except:
        return 0.0

def pattern_score(word):
    """Light structural rules only."""
    score = 0.0
    
    # name-like length
    if 3 <= len(word) <= 12:
        score += 0.2
    
    # no numbers
    if not re.search(r"\d", word):
        score += 0.1

    return score

def caps_score(word):
    """Names often start with capital letters."""
    if word.istitle():
        return 0.4
    if word.isupper():
        return -0.3
    return 0.0

def name_score(word):
    word = preprocess(word)
    if not word:
        return 0.0

    doc = nlp(word)
    token = doc[0]

    ml = ml_prob(word)
    pat = pattern_score(word)
    cap = caps_score(word)

    # spaCy PROPN detection
    propn_bonus = 0.6 if token.pos_ == "PROPN" else 0.0

    # NER detection (rare but ok)
    ner_bonus = 1.0 if token.ent_type_ == "PERSON" else 0.0

    # penalties
    verb_penalty = 1.0 if token.pos_ == "VERB" or word.lower() in COMMON_VERBS else 0.0
    stop_penalty = 1.2 if token.is_stop or word.lower() in STOPWORDS else 0.0
    tech_penalty = 1.3 if word.lower() in TECH_WORDS else 0.0

    final = ml + pat + cap + propn_bonus + ner_bonus - verb_penalty - stop_penalty - tech_penalty
    return final
