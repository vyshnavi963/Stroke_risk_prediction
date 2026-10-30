# Project Report Outline

## Title
Explainable AI-Based Stroke Risk Prediction and Personalized Preventive Healthcare Recommendation System

## Abstract (draft)
This project presents an educational prototype that combines a machine-learning classification model with explainable AI and a rule-based preventive-health education module. The workflow includes data preparation, class-imbalance-aware model training, evaluation using multiple metrics, and SHAP explanations to inspect feature contributions to model outputs. A Flask interface accepts sample health information, displays a model output or clearly labeled demonstration score, and presents general educational recommendations. The prototype is intended for academic demonstration only. It is not a clinically validated stroke-risk assessment tool and should not be used for diagnosis or treatment decisions.

## Objectives
- Explore a public stroke prediction dataset.
- Train and evaluate a baseline classifier.
- Use SHAP to explain model behavior.
- Provide general educational prevention recommendations.
- Develop a web interface for demonstration.

## Limitations to disclose
- The public dataset may not represent every population.
- Class imbalance affects performance.
- A high accuracy score can hide poor detection of minority-class cases.
- SHAP values describe model behavior, not causation.
- No external validation or clinical approval has been completed.
- The demo fallback score is not a learned prediction model.
