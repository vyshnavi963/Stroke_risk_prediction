def generate_recommendations(age, bmi, glucose, hypertension, heart_disease, smoking_status):
    """Return general educational suggestions, not diagnosis or treatment."""
    recommendations = [
        "Choose a balanced eating pattern with vegetables, fruit, whole grains, and appropriate portions.",
        "Aim for regular physical activity suited to your abilities and any advice from your healthcare professional."
    ]
    if bmi >= 25:
        recommendations.append("If appropriate for you, discuss sustainable weight-management goals with a healthcare professional.")
    if glucose >= 126:
        recommendations.append("Discuss your glucose result with a healthcare professional; one reading alone does not diagnose diabetes.")
    if hypertension == 1:
        recommendations.append("Follow professional guidance for blood-pressure monitoring and management.")
    if heart_disease == 1:
        recommendations.append("Discuss heart health and stroke prevention with your healthcare professional.")
    if smoking_status == "smokes":
        recommendations.append("Consider smoking-cessation support from a qualified healthcare professional.")
    if age >= 55:
        recommendations.append("Ask a healthcare professional which preventive checks are appropriate for your age and health history.")
    return recommendations
