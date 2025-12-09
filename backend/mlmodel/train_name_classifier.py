import panda as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from skleran.model_selection import train_test_split

# Load dataset
df = pd.read_csv("backend/mlmodel/name_dataset.csv")
X = df["word"]
y= df["label"]

vectorizer = TfidfVectorizer(analyzer="char", ngram_range=(2, 4))
X_vec = vectorizer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_vec, y, test_size=0.2, random_state=42
)

model = logisticRegression(max_iter=2000)
model.fit(X_train,y_train)

print("Train accuracy:", model.score(X_train, y_train))
print("Test accuracy:", model.score(X_test, y_test))

joblib.dump(model, "backend/mlmodel/name_classifier.pkl")
joblib.dump(vectorizer, "backend/mlmodel/name_vectorizer.pkl")

print("✔ Saved name_classifier.pkl and name_vectorizer.pkl")

