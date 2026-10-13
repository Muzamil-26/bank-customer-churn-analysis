-- q06: Active-member effect on churn.
-- Finding: inactive members churn at nearly 2x the rate of active ones.
SELECT
    CASE "Is Active Member" WHEN 1 THEN 'Active' ELSE 'Inactive' END AS membership,
    COUNT(*)                                                        AS customers,
    SUM(Churn)                                                      AS churned,
    ROUND(100.0 * SUM(Churn) / COUNT(*), 2)                         AS churn_rate_pct
FROM customers
GROUP BY membership
ORDER BY churn_rate_pct DESC;
