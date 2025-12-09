import joblib
import os
import re

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "name_classifier.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "name_vectorizer.pkl")

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

def preprocess(word):
    word = re.sub(r"[^A-Za-z]", "", word)
    return word.strip()

def is_name(word):
    clean = preprocess(word)
    if not clean:
        return False

    X = vectorizer.transform([clean])
    pred = model.predict(X)[0]
    return int(pred) == 1
