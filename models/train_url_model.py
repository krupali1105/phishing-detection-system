import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import joblib

# Load structured phishing dataset
df = pd.read_csv("models/data/phishing.csv")

X = df.drop("status", axis=1)   # features
y = df["status"]                # target (0=legit, 1=phish)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, max_depth=20, class_weight="balanced", random_state=42)
model.fit(X_train, y_train)

print(classification_report(y_test, model.predict(X_test)))

joblib.dump(model, "backend/app/models/url_model.pkl")
