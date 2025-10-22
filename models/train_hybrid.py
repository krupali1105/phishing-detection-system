import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
import joblib
import numpy as np

def train_hybrid_model():
    """Train hybrid phishing detection model."""
    # Load Dataset (structured phishing data)
    df = pd.read_csv("data/phishing.csv")
    X1 = df.drop("CLASS_LABEL", axis=1)  # All features except target
    y = df["CLASS_LABEL"]  # Target variable

    # Create synthetic text features from URL characteristics for hybrid model
    # This simulates text analysis using structured features
    text_features = df[["NumDots", "SubdomainLevel", "PathLevel", "UrlLength", "NumDash", "NumUnderscore"]].astype(str).agg(' '.join, axis=1)

    # TF-IDF on synthetic text features (reduced features for memory)
    vectorizer = TfidfVectorizer(max_features=1000, analyzer="char", ngram_range=(2,3))
    X2_vec = vectorizer.fit_transform(text_features)

    # Combine features
    X_combined = np.hstack((X1.values, X2_vec.toarray()))

    X_train, X_test, y_train, y_test = train_test_split(X_combined, y, test_size=0.2, random_state=42)

    model = GradientBoostingClassifier()
    model.fit(X_train, y_train)

    print(classification_report(y_test, model.predict(X_test)))

    joblib.dump(model, "../backend/app/models/hybrid_model.pkl")
    joblib.dump(vectorizer, "../backend/app/models/hybrid_vectorizer.pkl")
    
    return model, vectorizer, list(X1.columns) + ["synthetic_text_features"]

if __name__ == "__main__":
    train_hybrid_model()
