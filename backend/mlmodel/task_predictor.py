import os
import joblib
import re

# Load Model & Vectorizer Once
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "task_classifier.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "task_vectorizer.pkl")

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)


def preprocess(text: str) -> str:
    text = text.lower()

    # Remove punctuation
    text = re.sub(r"[^a-zA-Z0-9\s]", " ", text)

    # Normalize extra spaces
    text = re.sub(r"\s+", " ", text)

    return text.strip()


def is_task(sentence: str) -> bool:
    clean = preprocess(sentence)
    print("CLEANED SENTENCE →", clean)
    X = vectorizer.transform([clean])
    prediction = model.predict(X)[0]
    print("PREDICTION RAW →", prediction)
    return prediction == "1"

