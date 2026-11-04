
-- ============================================================
-- PROJECT: Sales Analytics & Business Intelligence
-- FILE: 04_advanced_analysis.sql
-- PURPOSE: Advanced business analysis using SQL window functions
-- DATABASE: PostgreSQL
-- ============================================================


-- 1. Year-over-Year Revenue Growth

WITH yearly_sales AS (
    SELECT
        EXTRACT(YEAR FROM order_date)::INTEGER AS sales_year,
        SUM(sales) AS total_revenue
    FROM raw_superstore
    GROUP BY EXTRACT(YEAR FROM order_date)
),
yearly_comparison AS (
    SELECT
        sales_year,
        total_revenue,
        LAG(total_revenue) OVER (
            ORDER BY sales_year
        ) AS previous_year_revenue
    FROM yearly_sales
)
SELECT
    sales_year,
    ROUND(total_revenue, 2) AS total_revenue,
    ROUND(previous_year_revenue, 2) AS previous_year_revenue,
    ROUND(
        (total_revenue - previous_year_revenue)
        / NULLIF(previous_year_revenue, 0) * 100,
        2
    ) AS yoy_growth_percentage
FROM yearly_comparison
ORDER BY sales_year;


-- 2. Monthly Revenue Ranking

WITH monthly_sales AS (
    SELECT
        DATE_TRUNC('month', order_date)::DATE AS sales_month,
        SUM(sales) AS total_revenue
    FROM raw_superstore
    GROUP BY DATE_TRUNC('month', order_date)
)
SELECT
    sales_month,
    ROUND(total_revenue, 2) AS total_revenue,
    RANK() OVER (
        ORDER BY total_revenue DESC
    ) AS revenue_rank
FROM monthly_sales
ORDER BY revenue_rank;


-- 3. Top 3 Products in Each Category

WITH product_performance AS (
    SELECT
        category,
        product_id,
        product_name,
        SUM(sales) AS total_revenue,
        SUM(profit) AS total_profit
    FROM raw_superstore
    GROUP BY
        category,
        product_id,
        product_name
),
ranked_products AS (
    SELECT
        *,
        DENSE_RANK() OVER (
            PARTITION BY category
            ORDER BY total_revenue DESC
        ) AS product_rank
    FROM product_performance
)
SELECT
    category,
    product_id,
    product_name,
    ROUND(total_revenue, 2) AS total_revenue,
    ROUND(total_profit, 2) AS total_profit,
    product_rank
FROM ranked_products
WHERE product_rank <= 3
ORDER BY category, product_rank;


-- 4. Repeat Customer Analysis

WITH customer_orders AS (
    SELECT
        customer_id,
        customer_name,
        COUNT(DISTINCT order_id) AS total_orders,
        SUM(sales) AS total_revenue
    FROM raw_superstore
    GROUP BY customer_id, customer_name
)
SELECT
    COUNT(*) AS total_customers,
    COUNT(*) FILTER (
        WHERE total_orders > 1
    ) AS repeat_customers,
    ROUND(
        COUNT(*) FILTER (
            WHERE total_orders > 1
        ) * 100.0 / NULLIF(COUNT(*), 0),
        2
    ) AS repeat_customer_percentage,
    ROUND(AVG(total_orders), 2) AS average_orders_per_customer
FROM customer_orders;


-- 5. Customer Revenue Ranking

WITH customer_revenue AS (
    SELECT
        customer_id,
        customer_name,
        SUM(sales) AS total_revenue
    FROM raw_superstore
    GROUP BY customer_id, customer_name
)
SELECT
    customer_id,
    customer_name,
    ROUND(total_revenue, 2) AS total_revenue,
    DENSE_RANK() OVER (
        ORDER BY total_revenue DESC
    ) AS customer_rank
FROM customer_revenue
ORDER BY customer_rank;


-- 6. Cumulative Monthly Revenue

WITH monthly_sales AS (
    SELECT
        DATE_TRUNC('month', order_date)::DATE AS sales_month,
        SUM(sales) AS monthly_revenue
    FROM raw_superstore
    GROUP BY DATE_TRUNC('month', order_date)
)
SELECT
    sales_month,
    ROUND(monthly_revenue, 2) AS monthly_revenue,
    ROUND(
        SUM(monthly_revenue) OVER (
            ORDER BY sales_month
            ROWS BETWEEN UNBOUNDED PRECEDING
            AND CURRENT ROW
        ),
        2
    ) AS cumulative_revenue
FROM monthly_sales
ORDER BY sales_month;


-- 7. Customer Purchase Intervals

WITH customer_order_dates AS (
    SELECT DISTINCT
        customer_id,
        order_id,
        order_date
    FROM raw_superstore
),
purchase_intervals AS (
    SELECT
        customer_id,
        order_id,
        order_date,
        LAG(order_date) OVER (
            PARTITION BY customer_id
            ORDER BY order_date, order_id
        ) AS previous_order_date
    FROM customer_order_dates
)
SELECT
    customer_id,
    order_id,
    order_date,
    previous_order_date,
    order_date - previous_order_date
        AS days_between_orders
FROM purchase_intervals
WHERE previous_order_date IS NOT NULL
ORDER BY customer_id, order_date;


-- 8. Shipping Performance Analysis

SELECT
    ship_mode,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(
        AVG(ship_date - order_date),
        2
    ) AS average_shipping_days,
    MIN(ship_date - order_date) AS fastest_shipping_days,
    MAX(ship_date - order_date) AS slowest_shipping_days
FROM raw_superstore
WHERE ship_date IS NOT NULL
GROUP BY ship_mode
ORDER BY average_shipping_days;


-- 9. Revenue Contribution by Category

WITH category_sales AS (
    SELECT
        category,
        SUM(sales) AS total_revenue
    FROM raw_superstore
    GROUP BY category
)
SELECT
    category,
    ROUND(total_revenue, 2) AS total_revenue,
    ROUND(
        total_revenue * 100.0
        / NULLIF(SUM(total_revenue) OVER (), 0),
        2
    ) AS revenue_contribution_percentage
FROM category_sales
ORDER BY total_revenue DESC;


-- 10. Profitability Ranking by Region

WITH regional_performance AS (
    SELECT
        region,
        SUM(sales) AS total_revenue,
        SUM(profit) AS total_profit
    FROM raw_superstore
    GROUP BY region
)
SELECT
    region,
    ROUND(total_revenue, 2) AS total_revenue,
    ROUND(total_profit, 2) AS total_profit,
    ROUND(
        total_profit * 100.0
        / NULLIF(total_revenue, 0),
        2
    ) AS profit_margin_percentage,
    DENSE_RANK() OVER (
        ORDER BY total_profit DESC
    ) AS profitability_rank
FROM regional_performance
ORDER BY profitability_rank;
