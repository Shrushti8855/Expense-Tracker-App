# 💰 Expense Tracker App — Data Science & Financial Analytics

An interactive personal finance analytics dashboard built using Python, Pandas, NumPy, Matplotlib, Seaborn, and Streamlit. The application analyzes synthetic financial transactions, visualizes spending patterns, monitors monthly budgets, and generates automated financial insights.

> **Note:** This project uses synthetic data for educational and portfolio demonstration purposes. It does not connect to real bank accounts or represent actual personal financial records.

## 🚀 Features

- **Financial KPI Dashboard:** Track total income, total expenses, net balance, and transaction counts.
- **Expense Category Analysis:** Identify the largest spending categories through charts.
- **Monthly Financial Trends:** Compare income and expenses over time.
- **Payment Method Analysis:** Compare spending across UPI, cash, debit cards, credit cards, and net banking.
- **Budget Monitoring:** Set a monthly budget and receive spending alerts.
- **Interactive Filters:** Filter transactions by date, category, transaction type, and payment method.
- **Transaction Explorer:** View filtered transaction records.
- **CSV Export:** Download filtered transactions.
- **Automated Reporting:** Generate category summaries, monthly summaries, payment summaries, weekday analysis, and text-based insights.
- **Data Quality Checks:** Handle missing values, duplicate transaction IDs, invalid amounts, and inconsistent text formatting.

## 🛠️ Tech Stack

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn
- Streamlit
- Git and GitHub

## 📁 Project Structure

```text
Expense-Tracker-App/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── data/
│   ├── raw/
│   │   └── synthetic_expenses.csv
│   └── processed/
│       └── cleaned_expenses.csv
├── src/
│   ├── generate_data.py
│   ├── data_cleaning.py
│   └── analysis.py
├── outputs/
│   ├── charts/
│   └── reports/
└── images/
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/Expense-Tracker-App.git
cd Expense-Tracker-App
```

Replace `YOUR_USERNAME` with your GitHub username after publishing the repository.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Generate the synthetic dataset

```bash
python src/generate_data.py
```

### 5. Clean the data

```bash
python src/data_cleaning.py
```

### 6. Generate analysis reports and charts

```bash
python src/analysis.py
```

### 7. Launch the dashboard

```bash
streamlit run app.py
```

Open the local URL displayed in the terminal, typically `http://localhost:8501`.

## 📊 Dataset

The project generates 1,500 synthetic transactions covering January–December 2025.

The dataset contains transaction IDs, dates, categories, descriptions, amounts, transaction types, and payment methods. The cleaning pipeline adds derived date features and saves the processed dataset.

## 📈 Analysis Outputs

The exploratory data analysis produces:

- Expense totals by category
- Expense distribution by category
- Monthly income versus expenses
- Monthly net balance
- Expenses by payment method
- Expense transaction counts by weekday

It also exports CSV summaries and an automated insights report.

## 🧠 Skills Demonstrated

- Data generation and preprocessing
- Data cleaning and validation
- Exploratory data analysis (EDA)
- Data aggregation and grouping
- Time-based analysis
- Data visualization
- Financial KPI calculations
- Interactive dashboard development
- CSV reporting
- Python project organization
- Git and GitHub version control

## 🔮 Future Improvements

- Persistent monthly budget settings
- User-defined transaction entry
- Database integration
- Recurring transaction detection
- Expense anomaly detection
- Spending forecasts using time-series methods
- Automated unit tests
- Deployment to Streamlit Community Cloud

## 👩‍💻 Author

**Shrushti Shewale**

GitHub: [Shrushti8855](https://github.com/Shrushti8855)

---

Built as a practical Data Science and financial analytics portfolio project.
