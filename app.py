from flask import Flask, render_template, request, redirect, url_for, session
import os, json
from datetime import datetime
from pathlib import Path
from recommendation import generate_recommendations

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "change-this-for-local-demo")
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "stroke_model.joblib"
HISTORY_PATH = BASE_DIR / "prediction_history.json"

model = None
feature_columns = None
model_status = "DEMO MODE — no trained model file found"
try:
    import joblib
    if MODEL_PATH.exists():
        bundle = joblib.load(MODEL_PATH)
        model = bundle["model"]
        feature_columns = bundle["feature_columns"]
        model_status = "Trained model loaded"
except Exception as exc:
    model_status = f"Model could not be loaded: {exc}"

def load_history():
    try:
        return json.loads(HISTORY_PATH.read_text(encoding="utf-8"))
    except Exception:
        return []

def save_history(items):
    HISTORY_PATH.write_text(json.dumps(items[-100:], indent=2), encoding="utf-8")

def demo_score(data):
    # Transparent demonstration score only; not a validated medical risk estimate.
    score = 0.05
    score += max(0, min(data["age"], 100)) * 0.002
    score += 0.10 if data["hypertension"] else 0
    score += 0.12 if data["heart_disease"] else 0
    score += max(0, min(data["glucose"] - 90, 150)) * 0.0008
    score += 0.06 if data["smoking_status"] == "smokes" else 0
    score += 0.03 if data["bmi"] >= 25 else 0
    return max(0.01, min(score, 0.95))

@app.route("/")
def index():
    return render_template("index.html", model_status=model_status)

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = {
            "age": float(request.form.get("age", 45)),
            "gender": request.form.get("gender", "Female"),
            "hypertension": int(request.form.get("hypertension", 0)),
            "heart_disease": int(request.form.get("heart_disease", 0)),
            "ever_married": request.form.get("ever_married", "Yes"),
            "work_type": request.form.get("work_type", "Private"),
            "Residence_type": request.form.get("Residence_type", "Urban"),
            "glucose": float(request.form.get("glucose", 90)),
            "bmi": float(request.form.get("bmi", 25)),
            "smoking_status": request.form.get("smoking_status", "never smoked"),
        }
        if data["age"] < 0 or data["age"] > 120 or data["bmi"] < 0 or data["glucose"] < 0:
            raise ValueError("Please enter valid non-negative values for age, BMI and glucose.")
    except (ValueError, TypeError):
        return render_template("index.html", error="Please enter valid numeric values.", model_status=model_status), 400

    is_demo = model is None
    probability = None
    explanation = []
    if model is not None:
        row = {
            "age": data["age"], "hypertension": data["hypertension"],
            "heart_disease": data["heart_disease"], "ever_married": data["ever_married"],
            "work_type": data["work_type"], "Residence_type": data["Residence_type"],
            "avg_glucose_level": data["glucose"], "bmi": data["bmi"],
            "gender": data["gender"], "smoking_status": data["smoking_status"]
        }
        import pandas as pd
        X = pd.DataFrame([row])
        X = pd.get_dummies(X, dtype=int)
        X = X.reindex(columns=feature_columns, fill_value=0)
        probability = float(model.predict_proba(X)[0, 1])
        label = "Higher model-estimated score" if probability >= 0.5 else "Lower model-estimated score"
        try:
            import shap
            explainer = shap.Explainer(model, X)
            sv = explainer(X)
            vals = sv.values
            if getattr(vals, "ndim", 0) == 3:
                vals = vals[0, :, 1]
            else:
                vals = vals[0]
            explanation = sorted(
                [{"feature": str(k), "contribution": float(v)} for k, v in zip(X.columns, vals)],
                key=lambda x: abs(x["contribution"]), reverse=True
            )[:5]
        except Exception:
            explanation = []
    else:
        probability = demo_score(data)
        label = "Demonstration score only"
        explanation = [
            {"feature": "Age", "contribution": 0.002 * data["age"]},
            {"feature": "Hypertension", "contribution": 0.10 if data["hypertension"] else 0},
            {"feature": "Heart disease", "contribution": 0.12 if data["heart_disease"] else 0},
            {"feature": "Glucose (demo rule)", "contribution": max(0, min(data["glucose"] - 90, 150)) * 0.0008},
        ]

    recommendations = generate_recommendations(
        age=data["age"], bmi=data["bmi"], glucose=data["glucose"],
        hypertension=data["hypertension"], heart_disease=data["heart_disease"],
        smoking_status=data["smoking_status"]
    )
    record = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "age": data["age"], "score": round(probability * 100, 1),
        "label": label, "demo": is_demo
    }
    history = load_history()
    history.append(record)
    save_history(history)
    return render_template(
        "result.html", data=data, probability=round(probability * 100, 1),
        label=label, recommendations=recommendations,
        explanation=explanation, is_demo=is_demo
    )

@app.route("/history")
def history():
    items = list(reversed(load_history()))
    return render_template("history.html", items=items, model_status=model_status)

@app.route("/about")
def about():
    return render_template("about.html", model_status=model_status)

if __name__ == "__main__":
    app.run(debug=True)
