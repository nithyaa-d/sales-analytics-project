
-- ============================================================
-- PROJECT: Sales Analytics & Business Intelligence
-- FILE: 01_schema.sql
-- PURPOSE: Create the raw Superstore sales table
-- DATABASE: PostgreSQL
-- ============================================================

CREATE TABLE IF NOT EXISTS raw_superstore (

    row_id          INTEGER PRIMARY KEY,
    order_id        VARCHAR(30) NOT NULL,
    order_date      DATE NOT NULL,
    ship_date       DATE,
    ship_mode       VARCHAR(50),

    customer_id     VARCHAR(30) NOT NULL,
    customer_name   VARCHAR(150),
    segment         VARCHAR(50),

    country_region  VARCHAR(100),
    city            VARCHAR(100),
    state           VARCHAR(100),
    postal_code     VARCHAR(20),
    region          VARCHAR(50),

    product_id      VARCHAR(50) NOT NULL,
    category        VARCHAR(50),
    sub_category    VARCHAR(50),
    product_name    VARCHAR(255),

    sales           NUMERIC(12, 2),
    quantity        INTEGER,
    discount        NUMERIC(5, 2),
    profit          NUMERIC(12, 2)

);

-- Verify table creation
SELECT *
FROM raw_superstore
LIMIT 10;

-- Check the total number of records
SELECT COUNT(*) AS total_records
FROM raw_superstore;

-- Check the number of unique orders
SELECT COUNT(DISTINCT order_id) AS unique_orders
FROM raw_superstore;

-- Check the number of unique customers
SELECT COUNT(DISTINCT customer_id) AS unique_customers
FROM raw_superstore;
