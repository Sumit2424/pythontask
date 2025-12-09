import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle

# ======================================================
# 1. Load Your Custom Dataset (500 sentences)
# ======================================================

custom_data_path = "custom_500.csv"
df = pd.read_csv(custom_data_path)

# Shuffle dataset for randomness
df = shuffle(df, random_state=42)

print("Dataset Loaded:")
print(df.head())
print("\nTotal Samples:", len(df))

# ======================================================
# 2. Preprocess + Vectorize (Convert text → numbers)
# ======================================================

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(df["sentence"])   # input features
y = df["label"]                                 # target labels (1/0)

# ======================================================
# 3. Train / Test Split
# ======================================================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, random_state=42
)

# ======================================================
# 4. Train Model (Logistic Regression)
# ======================================================

model = LogisticRegression(max_iter=2000)
model.fit(X_train, y_train)

print("\nTraining Complete.")
print("Train Accuracy:", model.score(X_train, y_train))
print("Test Accuracy:", model.score(X_test, y_test))

# ======================================================
# 5. Save Model + Vectorizer
# ======================================================


joblib.dump(model, "task_classifier.pkl")
joblib.dump(vectorizer, "task_vectorizer.pkl")

print("\n✔ Saved: task_classifier.pkl & task_vectorizer.pkl")
