-- q01: Overall churn KPIs — the numbers every downstream analysis is compared against.
-- Verified against pandas: churn_rate = 20.37%, churned = 2037, retained = 7963.
SELECT
    COUNT(*)                                             AS total_customers,
    SUM(Churn)                                           AS churned_customers,
    COUNT(*) - SUM(Churn)                                AS retained_customers,
    ROUND(100.0 * SUM(Churn) / COUNT(*), 2)              AS churn_rate_pct,
    ROUND(AVG(CASE WHEN Churn = 1 THEN Age END), 2)      AS avg_age_churned,
    ROUND(AVG(CASE WHEN Churn = 0 THEN Age END), 2)      AS avg_age_retained,
    ROUND(AVG(CASE WHEN Churn = 1 THEN Balance END), 2)  AS avg_balance_churned,
    ROUND(AVG(CASE WHEN Churn = 0 THEN Balance END), 2)  AS avg_balance_retained
FROM customers;
