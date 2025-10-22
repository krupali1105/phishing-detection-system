import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib

# Load malicious URL dataset
df = pd.read_csv("models/data/malicious_phish.csv")  # filename may differ
X = df["url"]
y = df["label"].apply(lambda x: 1 if x != "benign" else 0)  # binary

# TF-IDF Vectorization
vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(2,5), analyzer="char")
X_vec = vectorizer.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=42)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

print(classification_report(y_test, model.predict(X_test)))

# Save model + vectorizer
joblib.dump(model, "backend/app/models/text_model.pkl")
joblib.dump(vectorizer, "backend/app/models/text_vectorizer.pkl")
