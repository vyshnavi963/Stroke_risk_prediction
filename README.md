# Explainable AI-Based Stroke Risk Prediction and Personalized Preventive Healthcare Recommendation System

## Important
This is an educational academic prototype, not a medical device. It must not be used to diagnose stroke, estimate real individual clinical risk, or replace a clinician. The built-in demo score is a transparent placeholder only and is clearly labeled. Use the trained-model route only for coursework demonstrations after training with the intended dataset; even then, it is not clinically validated.

## Features
- Flask web application and input form
- Baseline Logistic Regression training script with class balancing
- SHAP-based local explanation attempt when a trained model is available
- Rule-based general educational recommendations
- Prediction history stored locally in `prediction_history.json`
- Demo mode so the interface can be shown without the dataset/model

## Project structure
```
Stroke_Risk_Prediction_Project/
  app.py
  recommendation.py
  train_model.py
  requirements.txt
  dataset/
  models/
  templates/
  static/
  docs/
```

## Setup on Windows / VS Code
1. Extract the ZIP.
2. Open the extracted `Stroke_Risk_Prediction_Project` folder in VS Code.
3. Open Terminal > New Terminal.
4. Create a virtual environment:
   ```
   python -m venv venv
   ```
5. Activate it in PowerShell:
   ```
   .\venv\Scripts\Activate.ps1
   ```
   If PowerShell blocks activation, use Command Prompt terminal and run:
   ```
   venv\Scripts\activate.bat
   ```
6. Install dependencies:
   ```
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```
7. Start the application:
   ```
   python app.py
   ```
8. Open `http://127.0.0.1:5000` in your browser.

## Train on the dataset
Place the CSV named `healthcare-dataset-stroke-data.csv` in `dataset/`.
Then run:
```
python train_model.py
```
The model is saved to `models/stroke_model.joblib`. Restart the Flask app after training to load it.

The expected CSV is commonly known as the Kaggle Healthcare Stroke Prediction dataset. Ensure your use complies with dataset licensing and institutional requirements. This ZIP does not claim to include that external dataset.

## Demo mode vs trained mode
- If no trained model is present, the app uses a demonstration-only rule score and labels it as demo mode.
- The demo score is not learned from data and is not a valid risk estimate.
- If a model is trained, the app uses the saved baseline model. Its output remains an unvalidated research/classroom prediction and must not be presented as a clinical result.

## SHAP
SHAP explanation is attempted for trained model predictions. If SHAP fails due to version/model compatibility, the prediction still renders and the explanation section may be empty. Your notebook's existing SHAP plots can also be included in the final report.

## Project report sections
1. Abstract
2. Introduction and problem statement
3. Literature review
4. Existing system and limitations
5. Proposed system and objectives
6. Dataset and preprocessing
7. Algorithms and model evaluation
8. Explainable AI using SHAP
9. Recommendation module
10. System architecture and implementation
11. Results and screenshots
12. Limitations, ethics and future work
13. Conclusion and references

## Suggested demo sequence
1. Launch app and show the home page.
2. Enter example values and submit.
3. Explain the score label, top contributing features if available, and general recommendations.
4. Open prediction history.
5. Explain that the demo score is a placeholder unless the trained dataset model is loaded.
6. Show SHAP plots from your notebook.

## Viva points
- Logistic Regression is a supervised classification algorithm.
- Class imbalance means stroke-positive rows are much fewer than stroke-negative rows.
- Accuracy alone can be misleading; recall, precision, F1 and average precision are useful additional metrics.
- SHAP explains contributions to a model output; it does not prove causation.
- The recommendation engine is rule-based and returns general educational suggestions.
- Limitations: class imbalance, single dataset, possible data leakage in a simple baseline, no external validation, and no clinical validation.
