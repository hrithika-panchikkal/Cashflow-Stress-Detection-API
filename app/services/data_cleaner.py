import pandas as pd

def clean_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and normalize trransaction dataframe.
    
    Handles:
    -malformed dates
    -invalid amounts
    -missing balances
    -inconsistent casing
    """
    # Create copy to avoid mutating original dataframe
    cleaned_df = df.copy()

    # Normalize column names
    # Example: " Date" -> "date"
    cleaned_df.columns = [
        col.strip().lower()
        for col in cleaned_df.columns
    ]

    # Convert date column safely
    # Invalid dates become NaT
    cleaned_df["date"] = pd.to_datetime(cleaned_df["date"],errors="coerce")

    # Convert amount to numeric
    # Invalid values become NaN
    cleaned_df["amount"] = pd.to_numeric(cleaned_df["amount"], errors="coerce")

    # Convert balance_after to numeric
    cleaned_df["balance_after"] = pd.to_numeric(cleaned_df["balance_after"], errors="coerce")

    # Normalize description casing
    cleaned_df["description"] = (cleaned_df["description"].astype(str).str.strip().str.lower())

    # Normalize transaction type
    # Example: Credit -> credit
    cleaned_df["type"] = (cleaned_df["type"].astype(str).str.strip().str.lower())

    # Remove rows with critical nulls
    # These rows are unstable
    cleaned_df = cleaned_df.dropna(subset=["date", "amount", "balance_after"])

    # Sort by transaction date
    cleaned_df = cleaned_df.sort_values(by="date")

    # Reset dataframe index
    cleaned_df = cleaned_df.reset_index(drop=True)

    return cleaned_df