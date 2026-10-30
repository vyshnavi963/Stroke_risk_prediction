"""Train a baseline model using the public stroke dataset CSV.
Expected path: dataset/healthcare-dataset-stroke-data.csv
This educational model is not validated for clinical use.
"""
from pathlib import Path
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, average_precision_score

ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "dataset" / "healthcare-dataset-stroke-data.csv"
MODEL_DIR = ROOT / "models"
MODEL_DIR.mkdir(exist_ok=True)

if not DATA_PATH.exists():
    raise FileNotFoundError(
        f"Dataset not found: {DATA_PATH}\n"
        "Place healthcare-dataset-stroke-data.csv in the dataset folder, then run this script again."
    )

df = pd.read_csv(DATA_PATH)
required = {"stroke", "id", "bmi"}
if not required.issubset(df.columns):
    raise ValueError("Dataset does not appear to be the expected stroke dataset.")

df = df.drop(columns=["id"])
y = df["stroke"].astype(int)
X = df.drop(columns=["stroke"])
# Keep preprocessing fitted to the available dataset for this compact classroom baseline.
# For research-grade evaluation, use a train-only sklearn Pipeline/ColumnTransformer.
X["bmi"] = X["bmi"].fillna(X["bmi"].median())
X = pd.get_dummies(X, drop_first=True, dtype=int)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
model = LogisticRegression(max_iter=1000, class_weight="balanced", random_state=42)
model.fit(X_train, y_train)
pred = model.predict(X_test)
prob = model.predict_proba(X_test)[:, 1]
print("Classification report at default threshold 0.5:")
print(classification_report(y_test, pred, zero_division=0))
print("Confusion matrix:")
print(confusion_matrix(y_test, pred))
print("Average precision:", round(average_precision_score(y_test, prob), 4))
joblib.dump({"model": model, "feature_columns": list(X.columns)}, MODEL_DIR / "stroke_model.joblib")
print(f"Saved model to {MODEL_DIR / 'stroke_model.joblib'}")
print("Reminder: educational baseline only; not clinically validated.")
