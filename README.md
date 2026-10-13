# 🏦 Bank Customer Churn Analysis

![Python](https://img.shields.io/badge/Python-3.12-blue)
![pandas](https://img.shields.io/badge/pandas-2.2-green)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.5-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-1.39-red)
![SQLite](https://img.shields.io/badge/SQLite-3.45-lightgrey)

End-to-end data analyst project on **10,000 bank customers**: SQL analysis, exploratory data
analysis, churn prediction with machine learning, and an interactive Streamlit dashboard.

## 🎯 Problem statement

Customer churn is one of the costliest problems in banking — acquiring a new customer costs
far more than retaining an existing one. This project answers three questions for a bank's
retention team:

1. **Which** customers are leaving? (segmentation via SQL + EDA)
2. **Why** are they leaving? (drivers via correlation + feature importance)
3. **Who** is likely to leave next? (a Random Forest churn-risk model + an at-risk explorer)

## 📊 Dataset

Public Kaggle **Bank Customer Churn** dataset (`Churn_Modelling.csv`), committed in [`data/`](data/):

- **10,000 rows × 13 columns**, zero missing values, zero duplicates
- Columns: credit score, geography (France / Germany / Spain), gender, age, tenure, balance,
  number of products, credit-card ownership, active membership, estimated salary
- **Target:** `Churn` (1 = exited, 0 = retained) — overall churn rate **20.37%** (2,037 exited)
- Full column reference: [`data/data_dictionary.md`](data/data_dictionary.md)

### Live demo data

The deployed dashboard runs on a documented **1,500-row seeded sample** (`data_sample/churn_sample.csv`,
~95KB) so the repo stays small and the demo loads fast. The sample is a stratified
draw (seed 42) preserving the original 20.4% churn rate. The full 10,000-row file the
SQL analysis and notebooks ran on is in `data/` locally (reproducible from the public
Kaggle **Bank Customer Churn** dataset) — **every figure reported below comes from the
full dataset**, not the sample. The dashboard retrains its Random Forest on the sample
at startup, so no model binary is needed in the repo.

## 🔍 Key findings (all computed from the data)

| Finding | Numbers |
|---|---|
| 🇩🇪 Germany churns at **2×** the rate of France/Spain | Germany **32.44%** (814/2,509) vs France 16.15%, Spain 16.67% |
| 👵 Age 50–60 is the danger zone | **56.04%** churn; under-40s are loyal (<11%) |
| 🛍️ 2 products = loyalty sweet spot | 1 product → 27.71% churn · 2 products → **7.58%** · 3–4 products extreme but tiny cohorts |
| 😴 Inactive members churn ~2× more | 26.85% vs 14.27% for active members |
| 💰 **The wealthy leave** — the bank loses high-value accounts | Avg balance: churned **€91,109** vs retained €72,745; churn rises with balance decile |
| 👩 Women churn more than men | 25.07% vs 16.46% |
| 🚫 Credit score & tenure barely matter | Flat ~19–22% across all bands — don't spend retention budget there |
| 🎯 Priority cohort: **inactive Germans aged 40–60** | **61.24% churn** — 565 customers, 17% of ALL exits in one callable segment |

## 🤖 Model results (held-out test set, 2,000 customers, stratified 80/20 split)

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---|---|---|---|---|
| Logistic Regression | 80.75% | 58.46% | 18.67% | 28.31% | 0.7745 |
| **Random Forest** | **84.25%** | **60.18%** | **66.83%** | **63.33%** | **0.8644** |

Random Forest was selected for the dashboard's risk scoring — recall is what matters in churn
(it catches **2 out of 3** churners vs fewer than 1 in 5 for Logistic Regression), because
missing a churner costs the bank more than a false alarm.

**Top churn drivers** (Random Forest feature importance): Age (0.31) → NumOfProducts (0.19) →
Balance (0.11) → EstimatedSalary (0.09) → CreditScore (0.09) — consistent with the EDA story.

## 🛠️ Tech stack

- **Python** — pandas, NumPy, scikit-learn, Plotly
- **SQL** — SQLite (12 analytical queries: CTEs, window functions, segmentation)
- **Dashboard** — Streamlit (free Community Cloud deploy)
- No BI tools — everything is code, reproducible, and version-controlled.

## 📁 Project structure

```
bank-churn-analysis/
├── streamlit_app.py        # Interactive dashboard (deploy entry point)
├── requirements.txt        # Pinned dependencies for Streamlit Cloud
├── src/
│   └── data_loader.py      # Shared load/clean/feature helpers (used by notebooks + app)
├── data/
│   ├── churn_customers.csv # The 10,000-row dataset (analysis; not in repo — see "Live demo data")
│   └── data_dictionary.md  # Column reference
└── data_sample/
    └── churn_sample.csv    # 1,500-row stratified sample — powers the live demo dashboard
│   └── data_dictionary.md  # Column reference
├── sql/                    # 12 verified analytical queries (SQLite syntax)
│   ├── q01_churn_overview.sql
│   └── ... q12_zero_balance_churn.sql
├── notebooks/
│   ├── 01_eda.ipynb        # Full exploratory analysis with charts
│   └── 02_churn_prediction.ipynb  # Logistic Regression vs Random Forest
└── models/                 # Saved artifacts (metrics, feature importance) — created by notebook 02
```

## 🚀 How to run locally

```bash
git clone <this-repo>
cd bank-churn-analysis

python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Dashboard
streamlit run streamlit_app.py

# Notebooks
jupyter notebook notebooks/

# SQL (SQLite)
sqlite3 churn.db < sql/q01_churn_overview.sql   # after creating + importing the table, see sql/README.md
```

## 🎤 Interview talking points

- **Business framing first:** "I framed churn as a retention-ROI problem — 20% churn on 10k customers — and worked backwards to the segments worth calling."
- **The counterintuitive finding:** "Everyone expects dormant accounts to leave. The data says the opposite: churned customers are *wealthier* (€91k vs €73k average balance). The bank is losing its best customers, not its worst."
- **Actionable segmentation:** "I isolated one callable cohort — inactive Germans aged 40–60, 61% churn — that's a concrete campaign list, not a vague insight."
- **Modeling honesty:** "I compared Logistic Regression with Random Forest on a stratified 80/20 split and picked the winner on recall and ROC-AUC, because missing a churner costs more than a false alarm."
- **Reproducibility:** "One shared `src/data_loader.py` feeds the notebooks and the dashboard, so the numbers always agree."

## 📌 Notes

- Built by **Muzamil Khan** (B.Sc IT, Mumbai) as a portfolio project for fresher Data Analyst roles.
- All analysis code and numbers are reproducible from the committed dataset — no fabricated figures.
