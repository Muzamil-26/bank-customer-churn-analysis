-- q04: Churn rate by age band (CASE bucketing).
-- Finding: the 50-60 band churns at 56%+; under-30s barely churn.
SELECT
    CASE
        WHEN Age < 30  THEN '<30'
        WHEN Age < 40  THEN '30-40'
        WHEN Age < 50  THEN '40-50'
        WHEN Age < 60  THEN '50-60'
        ELSE '60+'
    END                                 AS age_band,
    COUNT(*)                            AS customers,
    SUM(Churn)                          AS churned,
    ROUND(100.0 * SUM(Churn) / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY age_band
ORDER BY
    CASE age_band
        WHEN '<30' THEN 1 WHEN '30-40' THEN 2 WHEN '40-50' THEN 3
        WHEN '50-60' THEN 4 ELSE 5
    END;
