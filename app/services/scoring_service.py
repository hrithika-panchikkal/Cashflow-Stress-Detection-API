def calculate_stress_score(stress_indicators: list) -> dict:
    """
    Calculate deterministic financial stress score from
    detected indicators.
    score range:
    0 -> no stress
    100 -> extreme financial stress
    """
    # Initial stress score
    score = 0

    # store scoring additions
    additions = []

    # Process stress indicators
    for indicator in stress_indicators:
        indicator_type = indicator["type"]

        # Bounced payments
        if indicator_type == "bounced_payments":
            points = (
                indicator["count"] * 3
            )
            score += points
            additions.append({
                "indicator": indicator_type,
                "points": points
            })
        
        # Negative cashflow months
        elif indicator_type == "negative_cashflow":
            points = (
                len(indicator["months"]) * 6
            )
            score += points
            additions.append({
                "indicator": indicator_type,
                "points": points
            })

        # Low balance period
        elif indicator_type == "low_balance_period":
            points = 10
            score += points
            additions.append({
                "indicator": indicator_type,
                "points": points
            })
        
        # Delayed salary payments
        elif indicator_type == "delayed_salary_payments":
            points = (
                len(indicator["months"]) * 2
            )
            score += points
            additions.append({
                "indicator": indicator_type,
                "points": points
            })

        # Revenue decline
        elif indicator_type == "revenue_decline":
            points = 8
            score += points
            additions.append({
                "indicator": indicator_type,
                "points": points
            })

    # Cap maximum score at 100
    score = min(score, 100)

    return {
        "final_score": score,
        "score_breakdown": additions
    }