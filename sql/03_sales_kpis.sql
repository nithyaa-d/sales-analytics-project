
-- ============================================================
-- PROJECT: Sales Analytics & Business Intelligence
-- FILE: 03_sales_kpis.sql
-- PURPOSE: Analyse sales performance and business KPIs
-- DATABASE: PostgreSQL
-- ============================================================


-- 1. Overall Business Performance
SELECT
    COUNT(DISTINCT order_id) AS total_orders,
    COUNT(DISTINCT customer_id) AS total_customers,
    COUNT(*) AS total_order_lines,
    ROUND(SUM(sales), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(
        SUM(profit) / NULLIF(SUM(sales), 0) * 100,
        2
    ) AS profit_margin_percentage
FROM raw_superstore;


-- 2. Average Order Value (AOV)
WITH order_revenue AS (
    SELECT
        order_id,
        SUM(sales) AS order_total
    FROM raw_superstore
    GROUP BY order_id
)
SELECT
    ROUND(AVG(order_total), 2) AS average_order_value
FROM order_revenue;


-- 3. Revenue and Profit by Product Category
SELECT
    category,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(sales), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(
        SUM(profit) / NULLIF(SUM(sales), 0) * 100,
        2
    ) AS profit_margin_percentage
FROM raw_superstore
GROUP BY category
ORDER BY total_revenue DESC;


-- 4. Sales Performance by Region
SELECT
    region,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(sales), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit
FROM raw_superstore
GROUP BY region
ORDER BY total_revenue DESC;


-- 5. Top 10 Products by Revenue
SELECT
    product_id,
    product_name,
    category,
    sub_category,
    ROUND(SUM(sales), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit
FROM raw_superstore
GROUP BY
    product_id,
    product_name,
    category,
    sub_category
ORDER BY total_revenue DESC
LIMIT 10;


-- 6. Top 10 Customers by Revenue
SELECT
    customer_id,
    customer_name,
    segment,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(sales), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit
FROM raw_superstore
GROUP BY
    customer_id,
    customer_name,
    segment
ORDER BY total_revenue DESC
LIMIT 10;


-- 7. Customer Segment Performance
SELECT
    segment,
    COUNT(DISTINCT customer_id) AS total_customers,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(sales), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit
FROM raw_superstore
GROUP BY segment
ORDER BY total_revenue DESC;


-- 8. Monthly Revenue and Profit Trends
SELECT
    DATE_TRUNC('month', order_date)::DATE AS sales_month,
    ROUND(SUM(sales), 2) AS monthly_revenue,
    ROUND(SUM(profit), 2) AS monthly_profit,
    COUNT(DISTINCT order_id) AS total_orders
FROM raw_superstore
GROUP BY DATE_TRUNC('month', order_date)
ORDER BY sales_month;


-- 9. Most Profitable Sub-Categories
SELECT
    category,
    sub_category,
    ROUND(SUM(sales), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND(
        SUM(profit) / NULLIF(SUM(sales), 0) * 100,
        2
    ) AS profit_margin_percentage
FROM raw_superstore
GROUP BY category, sub_category
ORDER BY total_profit DESC;


-- 10. Loss-Making Products
SELECT
    product_id,
    product_name,
    category,
    sub_category,
    ROUND(SUM(sales), 2) AS total_revenue,
    ROUND(SUM(profit), 2) AS total_profit
FROM raw_superstore
GROUP BY
    product_id,
    product_name,
    category,
    sub_category
HAVING SUM(profit) < 0
ORDER BY total_profit ASC
LIMIT 20;
