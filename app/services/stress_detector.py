import pandas as pd

from app.utils.constants import (
    BOUNCED_KEYWORDS,
    LOW_BALANCE_THRESHOLD
)

def detect_stress_indicators(
        df: pd.DataFrame,
        monthly_timeline: list
) -> list:
    """
    Detect financial stress indicators 
    from transaction data"""

    stress_indicators = []

    # Create dataframe copy
    stress_df = df.copy()

    # Ensure datetime format
    stress_df["date"] = pd.to_datetime(stress_df["date"], errors="coerce")

    # 1. Detect bounced/ returned payments

    bounce_pattern = "|".join(BOUNCED_KEYWORDS)
    bounced_transactions = stress_df[stress_df["description"].str.contains(bounce_pattern, case=False, na=False)]
    if len(bounced_transactions) > 0:
        stress_indicators.append({
            "type": "bounced_payments",
            "count": int(len(bounced_transactions)),
            "severity": "high"
        })

    # 2. Negative cashflow months

    negative_months = []
    for month_data in monthly_timeline:
        if month_data["net_flow"] < 0:
            negative_months.append(month_data["month"])
    if negative_months:
        stress_indicators.append({
            "type": "negative_cashflow",
            "months": negative_months,
            "severity": "medium"
        })

    # 3. Sustained low balance periods

    low_balance_days = stress_df[stress_df["balance_after"] < LOW_BALANCE_THRESHOLD]
    if len(low_balance_days) >= 10:
        stress_indicators.append({
            "type": "low_balance_period",
            "days": int(len(low_balance_days)),
            "threshold": LOW_BALANCE_THRESHOLD,
            "severity": "high"
        })

    # 4. Salary delay detection

    # Detect salary-related outgoing transcations
    # Assumptions:
    # Salary payments made after the 7th day of a month are considered delayed

    salary_transactions = stress_df[stress_df["description"].str.contains("salary", case=False, na=False) & (stress_df["type"] == "debit")].copy()
    delayed_salary_months = []
    # Proceed onyl if salary transactions exist
    if not salary_transactions.empty:
        # Create month column
        salary_transactions["month"] = (salary_transactions["date"].dt.strftime("%Y-%m"))

        # Get earliest salary payment date for each month
        grouped_salary = (salary_transactions.groupby("month")["date"].min())

        # Check salary payment delay
        for month, salary_date in grouped_salary.items():
            # Salary paid after 7th day consider delayed
            if salary_date.day > 7:
                delayed_salary_months.append({
                    "month": month,
                    "salary_day": int(salary_date.day)
                })
    # Add stress indicator if delayed salary payments detected
    if delayed_salary_months:
        stress_indicators.append({
            "type": "delayed_salary_payments",
            "months": delayed_salary_months,
            "severity": "medium"
        })

    # 5. Revenue decline detection

    inflow_values = [
        month["total_inflows"]
        for month in monthly_timeline
    ]

    declining_trend = 0
    for i in range(1, len(inflow_values)):
        if inflow_values[i] < inflow_values[i - 1]:
            declining_trend += 1
    # Detect continuous revenue decline
    if declining_trend >= 3:
        stress_indicators.append({
            "type": "revenue_decline",
            "declining_months": declining_trend,
            "severity": "high"
        })
    return stress_indicators


