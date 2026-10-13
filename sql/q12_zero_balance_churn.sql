-- q12: Zero-balance customers vs churn — do dormant (zero-balance) accounts churn more?
-- Finding: counterintuitive — zero-balance customers churn LESS (13.8%) than
-- customers holding a balance (24.1%). Churned customers are on average
-- WEALTHIER (avg balance ~91k vs ~73k for retained).
SELECT
    CASE WHEN Balance = 0 THEN 'Zero balance' ELSE 'Has balance' END AS balance_status,
    COUNT(*)                                                        AS customers,
    SUM(Churn)                                                      AS churned,
    ROUND(100.0 * SUM(Churn) / COUNT(*), 2)                         AS churn_rate_pct,
    ROUND(AVG(Balance), 2)                                          AS avg_balance
FROM customers
GROUP BY balance_status
ORDER BY churn_rate_pct DESC;
