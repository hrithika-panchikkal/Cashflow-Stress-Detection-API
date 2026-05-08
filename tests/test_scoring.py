from app.services.scoring_service import (
    calculate_stress_score
)


def test_high_risk_stress_score():
    """
    Test high-risk financial profile.
    """

    stress_indicators = [
        {
            "type": "bounced_payments",
            "count": 10
        },
        {
            "type": "negative_cashflow",
            "months": [
                "2025-11",
                "2025-12"
            ]
        },
        {
            "type": "revenue_decline"
        }
    ]

    result = calculate_stress_score(
        stress_indicators
    )

    # Assert score exists
    assert result["final_score"] > 0

    # Assert high stress detected
    assert result["final_score"] >= 50


def test_low_risk_stress_score():
    """
    Test low-risk financial profile.
    """

    stress_indicators = []

    result = calculate_stress_score(
        stress_indicators
    )

    # No stress indicators
    assert result["final_score"] == 0


def test_score_never_exceeds_100():
    """
    Ensure score is capped at 100.
    """

    stress_indicators = [
        {
            "type": "bounced_payments",
            "count": 100
        }
    ]

    result = calculate_stress_score(
        stress_indicators
    )

    assert result["final_score"] <= 100