
"""Generate a reproducible synthetic expense-tracking dataset."""

from pathlib import Path

import numpy as np
import pandas as pd

# Project root: Expense-Tracker-App/
ROOT = Path(__file__).resolve().parent.parent
OUTPUT_FILE = ROOT / "data" / "raw" / "synthetic_expenses.csv"

# Fixed random seed ensures repeatable results.
rng = np.random.default_rng(42)

NUM_TRANSACTIONS = 1500

categories = [
    "Food",
    "Transport",
    "Rent",
    "Shopping",
    "Entertainment",
    "Healthcare",
    "Utilities",
    "Education",
    "Travel",
]

payment_methods = ["UPI", "Cash", "Debit Card", "Credit Card", "Net Banking"]

# Category probabilities simulate different spending frequencies.
category_probabilities = [
    0.22, 0.12, 0.08, 0.14, 0.10, 0.07, 0.10, 0.07, 0.10
]

# Category-specific typical transaction amounts in INR.
amount_ranges = {
    "Food": (50, 1200),
    "Transport": (30, 800),
    "Rent": (5000, 15000),
    "Shopping": (200, 5000),
    "Entertainment": (100, 2000),
    "Healthcare": (100, 4000),
    "Utilities": (300, 3500),
    "Education": (200, 6000),
    "Travel": (500, 10000),
}

# Generate transactions across 12 months.
start_date = pd.Timestamp("2025-01-01")
end_date = pd.Timestamp("2025-12-31")

date_offsets = rng.integers(
    0, (end_date - start_date).days + 1, NUM_TRANSACTIONS
)
dates = start_date + pd.to_timedelta(date_offsets, unit="D")

selected_categories = rng.choice(
    categories,
    size=NUM_TRANSACTIONS,
    p=category_probabilities,
)

amounts = [
    round(rng.uniform(*amount_ranges[category]), 2)
    for category in selected_categories
]

# Most records are expenses; some represent income.
transaction_types = rng.choice(
    ["Expense", "Income"],
    size=NUM_TRANSACTIONS,
    p=[0.92, 0.08],
)

# Use more realistic amounts for income transactions.
for index, transaction_type in enumerate(transaction_types):
    if transaction_type == "Income":
        amounts[index] = round(
            rng.choice([rng.uniform(1000, 10000),
                        rng.uniform(15000, 60000)]),
            2,
        )
        selected_categories[index] = rng.choice(
            ["Salary", "Freelance", "Other Income"]
        )

payment_method_values = rng.choice(
    payment_methods, size=NUM_TRANSACTIONS
)

descriptions = {
    "Food": "Food purchase",
    "Transport": "Local transport",
    "Rent": "Monthly rent",
    "Shopping": "Shopping purchase",
    "Entertainment": "Entertainment activity",
    "Healthcare": "Healthcare expense",
    "Utilities": "Utility payment",
    "Education": "Education expense",
    "Travel": "Travel booking",
    "Salary": "Salary received",
    "Freelance": "Freelance payment",
    "Other Income": "Other income received",
}

df = pd.DataFrame(
    {
        "Transaction_ID": [
            f"TXN{i:05d}" for i in range(1, NUM_TRANSACTIONS + 1)
        ],
        "Date": dates,
        "Category": selected_categories,
        "Description": [
            descriptions[category] for category in selected_categories
        ],
        "Amount": amounts,
        "Type": transaction_types,
        "Payment_Method": payment_method_values,
    }
)

# Sort transactions chronologically.
df = df.sort_values("Date").reset_index(drop=True)

# Ensure output directory exists.
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
df.to_csv(OUTPUT_FILE, index=False)

print("=" * 55)
print("SYNTHETIC EXPENSE DATASET GENERATED SUCCESSFULLY")
print("=" * 55)
print(f"File: {OUTPUT_FILE}")
print(f"Total transactions: {len(df)}")
print(f"Date range: {df['Date'].min().date()} to {df['Date'].max().date()}")
print(f"Total income: ₹{df.loc[df['Type'] == 'Income', 'Amount'].sum():,.2f}")
print(f"Total expenses: ₹{df.loc[df['Type'] == 'Expense', 'Amount'].sum():,.2f}")
print("\nDataset preview:")
print(df.head(10).to_string(index=False))
print("\nTransactions by type:")
print(df["Type"].value_counts())
print("\nCategory counts:")
print(df["Category"].value_counts())
