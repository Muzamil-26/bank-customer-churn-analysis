-- q08: Geography x Gender segment ranking (CTE + RANK window function).
-- Answers: "which demographic segments should retention target first?"
WITH segments AS (
    SELECT
        Geography,
        Gender,
        COUNT(*)                                AS customers,
        SUM(Churn)                              AS churned,
        ROUND(100.0 * SUM(Churn) / COUNT(*), 2) AS churn_rate_pct
    FROM customers
    GROUP BY Geography, Gender
)
SELECT
    Geography,
    Gender,
    customers,
    churned,
    churn_rate_pct,
    RANK() OVER (ORDER BY churn_rate_pct DESC) AS churn_rank
FROM segments
ORDER BY churn_rank;
