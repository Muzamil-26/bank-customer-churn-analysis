# SQL Analysis

12 analytical queries against `data/churn_customers.csv`, using **SQLite-compatible** syntax.

## Run

```bash
# 1. Create the table first (so headers with spaces survive the import)...
sqlite3 churn.db <<'EOF'
CREATE TABLE customers (
  CustomerId INTEGER, Surname TEXT, CreditScore INTEGER, Geography TEXT,
  Gender TEXT, Age INTEGER, Tenure INTEGER, Balance REAL,
  "Num Of Products" INTEGER, "Has Credit Card" INTEGER,
  "Is Active Member" INTEGER, "Estimated Salary" REAL, Churn INTEGER
);
EOF

# ...then import, skipping the CSV header line
sqlite3 churn.db <<'EOF'
.mode csv
.import --skip 1 ../data/churn_customers.csv customers
EOF

# 2. Run any query
sqlite3 churn.db < q01_churn_overview.sql
```

## What the queries cover

| # | File | Question answered |
|---|---|---|
| 1 | `q01_churn_overview.sql` | Overall churn KPIs |
| 2 | `q02_churn_by_geography.sql` | Churn by country |
| 3 | `q03_churn_by_gender.sql` | Churn by gender |
| 4 | `q04_churn_by_age_band.sql` | Churn by age band (`CASE` bucketing) |
| 5 | `q05_churn_by_products.sql` | Churn by number of products |
| 6 | `q06_active_member_effect.sql` | Active vs inactive members |
| 7 | `q07_balance_deciles.sql` | Balance deciles vs churn (`NTILE` window) |
| 8 | `q08_segment_ranking.sql` | Geography × Gender ranking (`CTE` + `RANK()`) |
| 9 | `q09_at_risk_segments.sql` | At-risk cohort identification |
| 10 | `q10_tenure_churn.sql` | Tenure vs churn |
| 11 | `q11_credit_score_bands.sql` | Credit-score bands vs churn |
| 12 | `q12_zero_balance_churn.sql` | Zero-balance accounts vs churn |
