-- q11: Credit-score bands vs churn (FICO-style cut points).
-- Finding: almost no relationship — credit score is not a churn driver here.
SELECT
    CASE
        WHEN CreditScore < 580  THEN 'Poor (<580)'
        WHEN CreditScore < 670  THEN 'Fair (580-669)'
        WHEN CreditScore < 740  THEN 'Good (670-739)'
        ELSE 'Very Good (740+)'
    END                                     AS credit_band,
    COUNT(*)                                AS customers,
    SUM(Churn)                              AS churned,
    ROUND(100.0 * SUM(Churn) / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY credit_band
ORDER BY
    CASE credit_band
        WHEN 'Poor (<580)' THEN 1 WHEN 'Fair (580-669)' THEN 2
        WHEN 'Good (670-739)' THEN 3 ELSE 4
    END;
