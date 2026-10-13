-- q05: Churn rate by number of products held.
-- Finding: 2 products = the loyalty sweet spot (7.6% churn).
-- 1 product churns 3.6x more; 3-4 products are tiny but extreme cohorts.
SELECT
    "Num Of Products"                       AS num_products,
    COUNT(*)                                AS customers,
    SUM(Churn)                              AS churned,
    ROUND(100.0 * SUM(Churn) / COUNT(*), 2) AS churn_rate_pct
FROM customers
GROUP BY "Num Of Products"
ORDER BY num_products;
