-- q03: Churn rate by gender (with geography cross-tab).
-- Finding: female customers churn at a materially higher rate than male.
SELECT
    Gender,
    COUNT(*)                                AS customers,
    SUM(Churn)                              AS churned,
    ROUND(100.0 * SUM(Churn) / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY Gender
ORDER BY churn_rate_pct DESC;
