import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATASET_PATH = os.path.join(BASE_DIR, "name_dataset.csv")
MODEL_PATH = os.path.join(BASE_DIR, "name_classifier.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "name_vectorizer.pkl")

df = pd.read_csv(DATASET_PATH)

X = df["word"].astype(str)
y = df["label"]

# Character TF-IDF → allows recognizing unseen names
vectorizer = TfidfVectorizer(analyzer="char", ngram_range=(2, 4))
X_vec = vectorizer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_vec, y, test_size=0.2, random_state=42
)

model = LogisticRegression(max_iter=2000)
model.fit(X_train, y_train)

print("Train accuracy:", model.score(X_train, y_train))
print("Test accuracy:", model.score(X_test, y_test))

joblib.dump(model, MODEL_PATH)
joblib.dump(vectorizer, VECTORIZER_PATH)

print("✔ Saved:", MODEL_PATH)
print("✔ Saved:", VECTORIZER_PATH)
