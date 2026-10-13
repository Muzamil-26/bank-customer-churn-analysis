-- q09: At-risk segments — inactive + Germany + age 40-60 (CTE stack).
-- This is the cohort the retention team should call first: large AND high churn.
WITH segments AS (
    SELECT
        Geography,
        "Is Active Member"                                              AS is_active,
        CASE WHEN Age BETWEEN 40 AND 60 THEN '40-60' ELSE 'Other' END   AS age_band,
        COUNT(*)                                AS customers,
        SUM(Churn)                              AS churned,
        ROUND(100.0 * SUM(Churn) / COUNT(*), 2) AS churn_rate_pct
    FROM customers
    GROUP BY Geography, is_active, age_band
)
SELECT
    Geography,
    CASE is_active WHEN 1 THEN 'Active' ELSE 'Inactive' END AS membership,
    age_band,
    customers,
    churned,
    churn_rate_pct
FROM segments
WHERE churn_rate_pct >= 30          -- material risk threshold
  AND customers >= 100             -- large enough to matter
ORDER BY churn_rate_pct DESC;
