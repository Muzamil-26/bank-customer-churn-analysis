-- q02: Churn rate by geography.
-- Finding: Germany churns at ~2x the rate of France/Spain.
SELECT
    Geography,
    COUNT(*)                                AS customers,
    SUM(Churn)                              AS churned,
    ROUND(100.0 * SUM(Churn) / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY Geography
ORDER BY churn_rate_pct DESC;
