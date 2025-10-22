import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
import joblib
import numpy as np

# Load Dataset 1 (structured)
df1 = pd.read_csv("models/data/phishing.csv")
X1 = df1.drop("status", axis=1)
y1 = df1["status"]

# Load Dataset 2 (raw URLs)
df2 = pd.read_csv("models/data/malicious_phish.csv")
X2 = df2["url"]
y2 = df2["label"].apply(lambda x: 1 if x != "benign" else 0)

# TF-IDF on Dataset 2
vectorizer = TfidfVectorizer(max_features=3000, analyzer="char", ngram_range=(2,5))
X2_vec = vectorizer.fit_transform(X2)

# Align datasets (take min rows to simplify hybrid demo)
min_len = min(len(X1), X2_vec.shape[0])
X1 = X1.iloc[:min_len]
y = y2.iloc[:min_len]   # use labels from URL dataset
X2_vec = X2_vec[:min_len]

# Combine features
X_combined = np.hstack((X1.values, X2_vec.toarray()))

X_train, X_test, y_train, y_test = train_test_split(X_combined, y, test_size=0.2, random_state=42)

model = GradientBoostingClassifier()
model.fit(X_train, y_train)

print(classification_report(y_test, model.predict(X_test)))

joblib.dump(model, "backend/app/models/hybrid_model.pkl")
joblib.dump(vectorizer, "backend/app/models/hybrid_vectorizer.pkl")
