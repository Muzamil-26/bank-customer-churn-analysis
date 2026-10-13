-- q07: Balance deciles vs churn (window function NTILE).
-- Finding: churn climbs with balance — the bank loses its highest-balance customers.
WITH ranked AS (
    SELECT
        Churn,
        NTILE(10) OVER (ORDER BY Balance) AS balance_decile
    FROM customers
)
SELECT
    balance_decile,
    COUNT(*)                                AS customers,
    SUM(Churn)                              AS churned,
    ROUND(100.0 * SUM(Churn) / COUNT(*), 2) AS churn_rate_pct
FROM ranked
GROUP BY balance_decile
ORDER BY balance_decile;
