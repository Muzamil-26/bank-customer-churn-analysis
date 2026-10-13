-- q10: Tenure vs churn — does loyalty (years with bank) reduce churn?
-- Finding: mostly flat; slight dip around tenure 7-8, no strong loyalty effect.
SELECT
    Tenure,
    COUNT(*)                                AS customers,
    SUM(Churn)                              AS churned,
    ROUND(100.0 * SUM(Churn) / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY Tenure
ORDER BY Tenure;
