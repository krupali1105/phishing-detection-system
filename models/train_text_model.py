import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
import joblib

def train_text_model():
    """Train text-based phishing detection model."""
    # Load phishing dataset (using available phishing.csv)
    df = pd.read_csv("data/phishing.csv")
    # For text model, we'll create synthetic text features from URL characteristics
    # This is a workaround since we don't have actual URL text
    X = df[["NumDots", "SubdomainLevel", "PathLevel", "UrlLength", "NumDash", "NumUnderscore"]].astype(str).agg(' '.join, axis=1)
    y = df["CLASS_LABEL"]  # 0=legitimate, 1=phishing

    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(2,5), analyzer="char")
    X_vec = vectorizer.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(X_vec, y, test_size=0.2, random_state=42)

    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)

    print(classification_report(y_test, model.predict(X_test)))

    # Save model + vectorizer
    joblib.dump(model, "../backend/app/models/text_model.pkl")
    joblib.dump(vectorizer, "../backend/app/models/tfidf_vectorizer.pkl")
    
    return model, vectorizer, ["synthetic_text_features"]

if __name__ == "__main__":
    train_text_model()
