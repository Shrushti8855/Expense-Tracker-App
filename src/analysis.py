
"""Analyze expense transactions and generate reports and charts."""

from pathlib import Path

import pandas as pd
import matplotlib

matplotlib.use("Agg")  # Save charts without requiring a GUI.
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = ROOT / "data" / "processed" / "cleaned_expenses.csv"
CHART_DIR = ROOT / "outputs" / "charts"
REPORT_DIR = ROOT / "outputs" / "reports"

sns.set_theme(style="whitegrid")


def analyze_expenses():
    """Generate financial summaries, charts, and insights."""

    print("=" * 60)
    print("EXPENSE TRACKER - EXPLORATORY DATA ANALYSIS")
    print("=" * 60)

    # Load cleaned transactions.
    df = pd.read_csv(INPUT_FILE, parse_dates=["Date"])

    # Create output folders.
    CHART_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    # Separate expenses and income.
    expenses = df[df["Type"] == "Expense"].copy()
    income = df[df["Type"] == "Income"].copy()

    total_expenses = expenses["Amount"].sum()
    total_income = income["Amount"].sum()
    net_balance = total_income - total_expenses

    print("\n1. FINANCIAL SUMMARY")
    print("-" * 40)
    print(f"Total transactions : {len(df):,}")
    print(f"Expense transactions: {len(expenses):,}")
    print(f"Income transactions : {len(income):,}")
    print(f"Total income        : Rs. {total_income:,.2f}")
    print(f"Total expenses      : Rs. {total_expenses:,.2f}")
    print(f"Net balance         : Rs. {net_balance:,.2f}")

    # --------------------------------------------------
    # 2. CATEGORY-WISE EXPENSE ANALYSIS
    # --------------------------------------------------
    category_summary = (
        expenses.groupby("Category")["Amount"]
        .agg(Total_Expense="sum", Transactions="count",
             Average_Transaction="mean")
        .sort_values("Total_Expense", ascending=False)
        .reset_index()
    )

    category_summary.to_csv(
        REPORT_DIR / "category_summary.csv", index=False
    )

    print("\n2. TOP SPENDING CATEGORIES")
    print("-" * 40)
    print(category_summary.head(5).to_string(index=False))

    # Bar chart.
    plt.figure(figsize=(11, 6))
    sns.barplot(
        data=category_summary,
        x="Category",
        y="Total_Expense",
        hue="Category",
        legend=False,
    )
    plt.title("Total Expenses by Category")
    plt.xlabel("Category")
    plt.ylabel("Total expenses (INR)")
    plt.xticks(rotation=35, ha="right")
    plt.tight_layout()
    plt.savefig(CHART_DIR / "category_expenses.png", dpi=150)
    plt.close()

    # Pie chart.
    plt.figure(figsize=(8, 8))
    plt.pie(
        category_summary["Total_Expense"],
        labels=category_summary["Category"],
        autopct="%1.1f%%",
        startangle=90,
    )
    plt.title("Expense Distribution by Category")
    plt.tight_layout()
    plt.savefig(CHART_DIR / "expense_distribution.png", dpi=150)
    plt.close()

    # --------------------------------------------------
    # 3. MONTHLY INCOME AND EXPENSE ANALYSIS
    # --------------------------------------------------
    monthly_expenses = (
        expenses.groupby("Year_Month")["Amount"]
        .sum()
        .rename("Total_Expenses")
    )

    monthly_income = (
        income.groupby("Year_Month")["Amount"]
        .sum()
        .rename("Total_Income")
    )

    monthly_summary = pd.concat(
        [monthly_income, monthly_expenses], axis=1
    ).fillna(0)

    monthly_summary["Net_Balance"] = (
        monthly_summary["Total_Income"]
        - monthly_summary["Total_Expenses"]
    )

    monthly_summary.index.name = "Year_Month"
    monthly_summary.to_csv(REPORT_DIR / "monthly_summary.csv")

    print("\n3. MONTHLY FINANCIAL SUMMARY")
    print("-" * 40)
    print(monthly_summary.round(2).to_string())

    monthly_summary[["Total_Income", "Total_Expenses"]].plot(
        figsize=(12, 6), marker="o"
    )
    plt.title("Monthly Income vs Expenses")
    plt.xlabel("Month")
    plt.ylabel("Amount (INR)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(CHART_DIR / "monthly_income_vs_expenses.png", dpi=150)
    plt.close()

    # Monthly net balance chart.
    monthly_summary["Net_Balance"].plot(
        kind="bar", figsize=(12, 5)
    )
    plt.axhline(0, linewidth=1)
    plt.title("Monthly Net Balance")
    plt.xlabel("Month")
    plt.ylabel("Income minus expenses (INR)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(CHART_DIR / "monthly_net_balance.png", dpi=150)
    plt.close()

    # --------------------------------------------------
    # 4. PAYMENT METHOD ANALYSIS
    # --------------------------------------------------
    payment_summary = (
        expenses.groupby("Payment_Method")
        .agg(
            Total_Expense=("Amount", "sum"),
            Transactions=("Transaction_ID", "count"),
        )
        .sort_values("Total_Expense", ascending=False)
        .reset_index()
    )

    payment_summary.to_csv(
        REPORT_DIR / "payment_method_summary.csv", index=False
    )

    print("\n4. EXPENSES BY PAYMENT METHOD")
    print("-" * 40)
    print(payment_summary.to_string(index=False))

    plt.figure(figsize=(9, 5))
    sns.barplot(
        data=payment_summary,
        x="Payment_Method",
        y="Total_Expense",
        hue="Payment_Method",
        legend=False,
    )
    plt.title("Expenses by Payment Method")
    plt.xlabel("Payment method")
    plt.ylabel("Total expenses (INR)")
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    plt.savefig(CHART_DIR / "payment_method_expenses.png", dpi=150)
    plt.close()

    # --------------------------------------------------
    # 5. WEEKDAY TRANSACTION PATTERNS
    # --------------------------------------------------
    weekday_order = [
        "Monday", "Tuesday", "Wednesday", "Thursday",
        "Friday", "Saturday", "Sunday",
    ]

    weekday_summary = (
        expenses.groupby("Weekday")
        .agg(
            Transactions=("Transaction_ID", "count"),
            Total_Expense=("Amount", "sum"),
        )
        .reindex(weekday_order, fill_value=0)
    )

    weekday_summary.to_csv(REPORT_DIR / "weekday_summary.csv")

    plt.figure(figsize=(10, 5))
    sns.barplot(
        x=weekday_summary.index,
        y=weekday_summary["Transactions"],
    )
    plt.title("Expense Transactions by Weekday")
    plt.xlabel("Day of week")
    plt.ylabel("Number of transactions")
    plt.xticks(rotation=25)
    plt.tight_layout()
    plt.savefig(CHART_DIR / "weekday_transactions.png", dpi=150)
    plt.close()

    # --------------------------------------------------
    # 6. AUTOMATIC INSIGHTS
    # --------------------------------------------------
    highest_category = category_summary.iloc[0]
    highest_expense_month = monthly_summary["Total_Expenses"].idxmax()
    lowest_expense_month = monthly_summary["Total_Expenses"].idxmin()
    highest_payment = payment_summary.iloc[0]

    insights = [
        "EXPENSE TRACKER - AUTOMATED INSIGHTS",
        "=" * 45,
        f"Total income: Rs. {total_income:,.2f}",
        f"Total expenses: Rs. {total_expenses:,.2f}",
        f"Net balance: Rs. {net_balance:,.2f}",
        (
            f"Highest spending category: {highest_category['Category']} "
            f"(Rs. {highest_category['Total_Expense']:,.2f})"
        ),
        f"Highest expense month: {highest_expense_month}",
        f"Lowest expense month: {lowest_expense_month}",
        (
            f"Payment method with highest expense total: "
            f"{highest_payment['Payment_Method']}"
        ),
    ]

    if net_balance < 0:
        insights.append(
            "Alert: total expenses exceed total income for this dataset."
        )
    elif net_balance > 0:
        insights.append(
            "Positive balance: total income exceeds total expenses."
        )
    else:
        insights.append("Income and expenses are equal.")

    insight_text = "\n".join(insights)

    (REPORT_DIR / "insights.txt").write_text(
        insight_text, encoding="utf-8"
    )

    print("\n5. AUTOMATED INSIGHTS")
    print("-" * 40)
    print(insight_text)

    print("\nAnalysis completed successfully.")
    print(f"Charts saved in: {CHART_DIR}")
    print(f"Reports saved in: {REPORT_DIR}")

    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net_balance": net_balance,
        "category_summary": category_summary,
        "monthly_summary": monthly_summary,
        "payment_summary": payment_summary,
    }


if __name__ == "__main__":
    analyze_expenses()
