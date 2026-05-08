import pandas as pd

def generate_monthly_timeline(
        df: pd.DataFrame
) -> list:
    """
    Generate monthly cashflow timeline.
    Returns:
    -inflows
    -outflows
    -net flow
    -end-of-month balance
    """
    # Create dataframe copy
    # Prevents modifying original dataframe
    timeline_df = df.copy()

    # Ensure data column is datetime
    # This avoids .dt accessor errors
    timeline_df["date"] = pd.to_datetime(timeline_df["date"], errors="coerce")

    # Remove rows with invalid dates
    timeline_df = timeline_df.dropna(subset=["date"])

    # Create month column from date
    # Example: 2025-07
    timeline_df["month"] = timeline_df["date"].dt.strftime("%Y-%m")

    monthly_timeline = []

    # Group transactions month-wise
    grouped_data = timeline_df.groupby("month")

    for month, group in grouped_data:
        # inflows = credit transaction
        inflows = group[group["type"] == "credit"]["amount"].sum()

        # outflows = debit transaction
        # Convert to positive value
        outflows = abs(group[group["type"] == "debit"]["amount"].sum())

        # Net Cashflow
        net_flow = inflows - outflows

        # End balance = last transaction balance in the month
        end_balance = (group.sort_values("date").iloc[-1]["balance_after"])

        # Append month summary
        monthly_timeline.append({

            "month": month,
            "total_inflows": round(inflows, 2),
            "total_outflows": round(outflows, 2),
            "net_flow": round(net_flow, 2),
            "end_balance": round(end_balance, 2)
        })
    return monthly_timeline