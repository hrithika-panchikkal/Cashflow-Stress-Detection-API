def generate_forward_view(stress_score: int, stress_indicators: list) -> dict:
    """
    Generate lending recommendation 
    based on stress score
    """
    # Low risk
    if stress_score <= 20:
        status = "low_risk"
    # Moderate risk
    elif stress_score <= 50:
        status = "moderate_risk"
    # High risk
    elif stress_score <= 80:
        status = "high_risk"
    # Decline
    else:
        status = "decline"
    
    # Generate explaination
    indicator_types = [
        indicator["type"]
        for indicator in stress_indicators
    ]

    reason = (
        "Risk assessment based on detected indicators: " + ", ".join(indicator_types)
    )

    return {
        "status": status,
        "reason": reason
    }