
-- ============================================================
-- PROJECT: Sales Analytics & Business Intelligence
-- FILE: 02_data_quality.sql
-- PURPOSE: Identify data quality issues in raw sales data
-- DATABASE: PostgreSQL
-- ============================================================


-- 1. Total number of records
SELECT
    COUNT(*) AS total_records
FROM raw_superstore;


-- 2. Check duplicate row IDs
SELECT
    row_id,
    COUNT(*) AS duplicate_count
FROM raw_superstore
GROUP BY row_id
HAVING COUNT(*) > 1;


-- 3. Check duplicate order-product combinations
SELECT
    order_id,
    product_id,
    COUNT(*) AS duplicate_count
FROM raw_superstore
GROUP BY order_id, product_id
HAVING COUNT(*) > 1;


-- 4. Check missing values
SELECT
    COUNT(*) FILTER (WHERE order_id IS NULL) AS missing_order_id,
    COUNT(*) FILTER (WHERE order_date IS NULL) AS missing_order_date,
    COUNT(*) FILTER (WHERE customer_id IS NULL) AS missing_customer_id,
    COUNT(*) FILTER (WHERE product_id IS NULL) AS missing_product_id,
    COUNT(*) FILTER (WHERE category IS NULL) AS missing_category,
    COUNT(*) FILTER (WHERE sales IS NULL) AS missing_sales,
    COUNT(*) FILTER (WHERE quantity IS NULL) AS missing_quantity,
    COUNT(*) FILTER (WHERE profit IS NULL) AS missing_profit
FROM raw_superstore;


-- 5. Check invalid sales values
SELECT *
FROM raw_superstore
WHERE sales IS NULL
   OR sales <= 0;


-- 6. Check invalid quantities
SELECT *
FROM raw_superstore
WHERE quantity IS NULL
   OR quantity <= 0;


-- 7. Check unusual discount values
SELECT *
FROM raw_superstore
WHERE discount IS NULL
   OR discount < 0
   OR discount > 1;


-- 8. Check invalid date sequences
SELECT
    order_id,
    order_date,
    ship_date
FROM raw_superstore
WHERE ship_date < order_date;


-- 9. Check negative profit
SELECT
    order_id,
    product_name,
    sales,
    profit
FROM raw_superstore
WHERE profit < 0
ORDER BY profit ASC;


-- 10. Check missing customer and product details
SELECT *
FROM raw_superstore
WHERE customer_name IS NULL
   OR product_name IS NULL;


-- 11. Summary by category
SELECT
    category,
    COUNT(*) AS total_records,
    SUM(sales) AS total_sales,
    SUM(profit) AS total_profit
FROM raw_superstore
GROUP BY category
ORDER BY total_sales DESC;


-- 12. Overall data quality summary
SELECT
    COUNT(*) AS total_records,
    COUNT(DISTINCT row_id) AS unique_row_ids,
    COUNT(DISTINCT order_id) AS unique_orders,
    COUNT(DISTINCT customer_id) AS unique_customers,
    COUNT(DISTINCT product_id) AS unique_products,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit
FROM raw_superstore;
