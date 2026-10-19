
"""Clean and validate the synthetic expense transaction dataset."""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = ROOT / "data" / "raw" / "synthetic_expenses.csv"
OUTPUT_FILE = ROOT / "data" / "processed" / "cleaned_expenses.csv"

REQUIRED_COLUMNS = [
    "Transaction_ID",
    "Date",
    "Category",
    "Description",
    "Amount",
    "Type",
    "Payment_Method",
]

VALID_TYPES = {"Expense", "Income"}


def clean_expenses(input_file=INPUT_FILE, output_file=OUTPUT_FILE):
    """Load, clean, validate, and save transaction data."""

    print("=" * 60)
    print("EXPENSE TRACKER - DATA CLEANING")
    print("=" * 60)

    # 1. Load the raw CSV.
    df = pd.read_csv(input_file)

    print(f"\nOriginal records: {len(df)}")

    # 2. Standardize column names.
    df.columns = df.columns.str.strip()

    # 3. Check required columns.
    missing_columns = set(REQUIRED_COLUMNS) - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    df = df[REQUIRED_COLUMNS].copy()

    # 4. Standardize text fields.
    text_columns = [
        "Transaction_ID",
        "Category",
        "Description",
        "Type",
        "Payment_Method",
    ]

    for column in text_columns:
        df[column] = df[column].astype("string").str.strip()

    # Treat empty strings as missing values.
    for column in text_columns:
        df[column] = df[column].replace("", pd.NA)

    # 5. Convert dates and amounts to valid data types.
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
    df["Amount"] = pd.to_numeric(df["Amount"], errors="coerce")

    # 6. Remove rows with missing critical fields.
    critical_columns = [
        "Transaction_ID",
        "Date",
        "Category",
        "Amount",
        "Type",
        "Payment_Method",
    ]

    missing_before = int(df[critical_columns].isna().any(axis=1).sum())

    df = df.dropna(subset=critical_columns).copy()

    # 7. Remove duplicate transaction IDs.
    # Keep the first occurrence to avoid counting the same ID twice.
    duplicate_ids = int(df["Transaction_ID"].duplicated().sum())

    df = df.drop_duplicates(
        subset=["Transaction_ID"], keep="first"
    ).copy()

    # 8. Normalize category and transaction-type labels.
    df["Category"] = df["Category"].str.title()
    df["Type"] = df["Type"].str.title()
    df["Payment_Method"] = df["Payment_Method"].str.title()

    # 9. Validate transaction type and amount.
    valid_rows = (
        df["Type"].isin(VALID_TYPES)
        & df["Amount"].gt(0)
    )

    invalid_rows = int((~valid_rows).sum())
    df = df.loc[valid_rows].copy()

    # 10. Add useful time-based features.
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Month_Name"] = df["Date"].dt.strftime("%B")
    df["Year_Month"] = df["Date"].dt.to_period("M").astype(str)
    df["Day"] = df["Date"].dt.day
    df["Weekday"] = df["Date"].dt.day_name()

    # 11. Sort and save the cleaned dataset.
    df = df.sort_values(
        ["Date", "Transaction_ID"]
    ).reset_index(drop=True)

    output_file = Path(output_file)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(output_file, index=False)

    # 12. Report data-quality results.
    print(f"Missing critical rows removed: {missing_before}")
    print(f"Duplicate transaction IDs removed: {duplicate_ids}")
    print(f"Invalid type/amount rows removed: {invalid_rows}")
    print(f"Final records: {len(df)}")
    print(f"Final columns: {len(df.columns)}")
    print(f"Missing values remaining: {int(df.isna().sum().sum())}")
    print(f"\nSaved cleaned data to:\n{output_file}")

    print("\nCleaned data preview:")
    print(df.head(10).to_string(index=False))

    print("\nTransaction type summary:")
    print(df["Type"].value_counts().to_string())

    return df


if __name__ == "__main__":
    clean_expenses()
