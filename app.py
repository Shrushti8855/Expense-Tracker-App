
"""Interactive Expense Tracker and Financial Analytics Dashboard."""

from pathlib import Path

import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parent
DATA_FILE = ROOT / "data" / "processed" / "cleaned_expenses.csv"

st.set_page_config(
    page_title="Expense Tracker | Data Science",
    page_icon="💰",
    layout="wide",
)

sns.set_theme(style="whitegrid")


@st.cache_data
def load_data():
    """Load and validate the cleaned transaction dataset."""
    df = pd.read_csv(DATA_FILE, parse_dates=["Date"])

    required = {
        "Transaction_ID",
        "Date",
        "Category",
        "Amount",
        "Type",
        "Payment_Method",
    }

    missing = required - set(df.columns)

    if missing:
        raise ValueError(f"Dataset is missing columns: {sorted(missing)}")

    return df


st.title("💰 Expense Tracker App")
st.caption(
    "Data Science | Personal Finance Analytics | Synthetic 2025 Dataset"
)

try:
    df = load_data()
except (FileNotFoundError, ValueError, pd.errors.ParserError) as error:
    st.error(f"Could not load the cleaned dataset: {error}")
    st.info("Run: python src\\data_cleaning.py")
    st.stop()

# --------------------------------------------------
# SIDEBAR FILTERS
# --------------------------------------------------
st.sidebar.header("🔎 Dashboard Filters")

min_date = df["Date"].min().date()
max_date = df["Date"].max().date()

date_range = st.sidebar.date_input(
    "Select date range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

all_categories = sorted(df["Category"].unique())

selected_categories = st.sidebar.multiselect(
    "Select categories",
    options=all_categories,
    default=all_categories,
)

selected_types = st.sidebar.multiselect(
    "Transaction type",
    options=["Expense", "Income"],
    default=["Expense", "Income"],
)

selected_methods = st.sidebar.multiselect(
    "Payment methods",
    options=sorted(df["Payment_Method"].unique()),
    default=sorted(df["Payment_Method"].unique()),
)

if len(date_range) == 2:
    start_date, end_date = date_range
else:
    start_date = end_date = date_range[0]

filtered = df[
    df["Date"].dt.date.between(start_date, end_date)
    & df["Category"].isin(selected_categories)
    & df["Type"].isin(selected_types)
    & df["Payment_Method"].isin(selected_methods)
].copy()

# --------------------------------------------------
# KEY PERFORMANCE INDICATORS
# --------------------------------------------------
expenses = filtered.loc[filtered["Type"] == "Expense", "Amount"].sum()
income = filtered.loc[filtered["Type"] == "Income", "Amount"].sum()
net_balance = income - expenses

col1, col2, col3, col4 = st.columns(4)

col1.metric("💵 Total Income", f"₹{income:,.2f}")
col2.metric("💸 Total Expenses", f"₹{expenses:,.2f}")
col3.metric(
    "📊 Net Balance",
    f"₹{net_balance:,.2f}",
    delta=f"₹{net_balance:,.2f}",
)
col4.metric("🧾 Transactions", f"{len(filtered):,}")

st.divider()

# --------------------------------------------------
# CATEGORY ANALYSIS
# --------------------------------------------------
st.subheader("📊 Category-wise Spending")

expense_data = filtered[filtered["Type"] == "Expense"]

if expense_data.empty:
    st.info("No expense records match the selected filters.")
else:
    category_totals = (
        expense_data.groupby("Category")["Amount"]
        .sum()
        .sort_values(ascending=False)
    )

    left, right = st.columns(2)

    with left:
        st.markdown("**Total expense by category**")
        st.bar_chart(category_totals)

    with right:
        st.markdown("**Expense distribution**")
        fig, ax = plt.subplots(figsize=(7, 5))
        ax.pie(
            category_totals,
            labels=category_totals.index,
            autopct="%1.1f%%",
            startangle=90,
        )
        ax.axis("equal")
        st.pyplot(fig)
        plt.close(fig)

    highest_category = category_totals.idxmax()
    highest_amount = category_totals.max()

    st.info(
        f"Highest spending category in the filtered data: "
        f"{highest_category} (₹{highest_amount:,.2f})."
    )

# --------------------------------------------------
# MONTHLY ANALYSIS
# --------------------------------------------------
st.subheader("📈 Monthly Income vs Expenses")

monthly = filtered.copy()
monthly["Year_Month"] = monthly["Date"].dt.to_period("M").astype(str)

monthly_summary = (
    monthly.pivot_table(
        index="Year_Month",
        columns="Type",
        values="Amount",
        aggfunc="sum",
        fill_value=0,
    )
    .reindex(columns=["Income", "Expense"], fill_value=0)
)

if monthly_summary.empty:
    st.info("No transactions are available for the selected filters.")
else:
    st.line_chart(monthly_summary)
    monthly_summary["Net_Balance"] = (
        monthly_summary["Income"] - monthly_summary["Expense"]
    )

    st.markdown("**Monthly financial summary**")
    st.dataframe(
        monthly_summary.style.format("₹{:,.2f}"),
        use_container_width=True,
    )

# --------------------------------------------------
# PAYMENT METHOD ANALYSIS
# --------------------------------------------------
st.subheader("💳 Spending by Payment Method")

if expense_data.empty:
    st.info("No expense records available for payment analysis.")
else:
    payment_summary = (
        expense_data.groupby("Payment_Method")["Amount"]
        .sum()
        .sort_values(ascending=False)
    )

    st.bar_chart(payment_summary)

# --------------------------------------------------
# BUDGET MONITORING
# --------------------------------------------------
st.subheader("🎯 Monthly Budget Monitoring")

st.caption(
    "Set an illustrative total monthly expense budget. "
    "The budget is for this dashboard session and is not persisted."
)

monthly_budget = st.number_input(
    "Monthly expense budget (₹)",
    min_value=0.0,
    value=30000.0,
    step=1000.0,
)

budget_month = st.selectbox(
    "Choose month",
    options=sorted(filtered["Year_Month"].unique(), reverse=True),
)

month_expenses = filtered[
    (filtered["Year_Month"] == budget_month)
    & (filtered["Type"] == "Expense")
]["Amount"].sum()

budget_col1, budget_col2 = st.columns(2)

budget_col1.metric("Selected month expenses", f"₹{month_expenses:,.2f}")

if monthly_budget > 0:
    utilization = month_expenses / monthly_budget
    budget_col2.metric("Budget used", f"{utilization:.1%}")
    st.progress(min(utilization, 1.0))

    if utilization > 1:
        st.error(
            f"Budget exceeded by ₹{month_expenses - monthly_budget:,.2f}."
        )
    elif utilization >= 0.8:
        st.warning("You have used at least 80% of the monthly budget.")
    else:
        st.success("Spending is within the selected monthly budget.")
else:
    st.warning("Enter a budget greater than zero to enable budget alerts.")

# --------------------------------------------------
# TRANSACTION TABLE AND DOWNLOAD
# --------------------------------------------------
st.subheader("📋 Transaction Records")

st.write(f"Records matching filters: {len(filtered):,}")

st.dataframe(
    filtered.sort_values("Date", ascending=False),
    use_container_width=True,
    hide_index=True,
)

csv_data = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download filtered transactions (CSV)",
    data=csv_data,
    file_name="filtered_expenses.csv",
    mime="text/csv",
)

st.caption(
    "Portfolio demonstration only. Uses synthetic data and does not "
    "connect to any bank or financial account."
)
