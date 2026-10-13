# Data Dictionary — `churn_customers.csv`

**Source:** Public Kaggle "Bank Customer Churn" dataset (`Churn_Modelling.csv`), 10,000 customer records. Zero missing values.  
**Target variable:** `Churn` (1 = customer exited the bank, 0 = retained).

| Column | Type | Description |
|---|---|---|
| `CustomerId` | Integer | Unique customer identifier (dropped from analysis — no predictive signal) |
| `Surname` | Text | Customer surname (dropped — free text, no signal) |
| `CreditScore` | Integer | Customer credit score, range 350–850 |
| `Geography` | Category | Customer country: France, Germany, or Spain |
| `Gender` | Category | Male / Female |
| `Age` | Integer | Customer age in years |
| `Tenure` | Integer | Years the customer has been with the bank (0–10) |
| `Balance` | Float | Account balance at the end of the period (EUR) |
| `Num Of Products` | Integer | Number of bank products the customer holds (1–4) |
| `Has Credit Card` | 0 / 1 | 1 = holds a credit card |
| `Is Active Member` | 0 / 1 | 1 = active member (uses the account regularly) |
| `Estimated Salary` | Float | Estimated annual salary (EUR) |
| `Churn` | 0 / 1 | **Target** — 1 = exited, 0 = stayed |

## Derived columns (created by `src/data_loader.py`)

| Column | Description |
|---|---|
| `AgeBand` | `<30`, `30-40`, `40-50`, `50-60`, `60+` |
| `CreditBand` | FICO-style bands: Poor (<580), Fair (580-669), Good (670-739), Very Good (740+) |
| `TenureBand` | New (0-2y), Established (3-7y), Loyal (8-10y) |
| `ZeroBalance` | 1 if Balance = 0 |
| `BalanceSalaryRatio` | Balance ÷ EstimatedSalary (share of annual salary held at the bank) |

## Quick facts

- 10,000 rows × 13 columns, no nulls, no duplicates.
- Overall churn rate: **20.37%** (2,037 exited).
- Note: `Num Of Products` uses spaces in the raw file — SQL queries in `sql/` quote it as `"Num Of Products"`.
