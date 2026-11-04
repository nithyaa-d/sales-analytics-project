
import pandas as pd
import numpy as np
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_FILE = BASE_DIR / "data" / "processed" / "superstore_cleaned.csv"
OUTPUT_DIR = BASE_DIR / "data" / "processed"

# Load cleaned dataset
print("Loading cleaned Superstore dataset...")
df = pd.read_csv(DATA_FILE, parse_dates=["order_date", "ship_date"])

print(f"Dataset loaded: {len(df):,} rows and {len(df.columns)} columns")

# Overall business KPIs
total_sales = df["sales"].sum()
total_profit = df["profit"].sum()
total_orders = df["order_id"].nunique()
total_customers = df["customer_id"].nunique()
total_products = df["product_id"].nunique()
total_quantity = df["quantity"].sum()

profit_margin = (total_profit / total_sales) * 100
average_order_value = total_sales / total_orders

kpis = pd.DataFrame({
    "metric": [
        "Total Sales",
        "Total Profit",
        "Total Orders",
        "Total Customers",
        "Unique Products",
        "Units Sold",
        "Profit Margin (%)",
        "Average Order Value"
    ],
    "value": [
        total_sales,
        total_profit,
        total_orders,
        total_customers,
        total_products,
        total_quantity,
        profit_margin,
        average_order_value
    ]
})

# Monthly sales and profit
df["order_month"] = df["order_date"].dt.to_period("M").astype(str)

monthly_trends = (
    df.groupby("order_month", as_index=False)
    .agg(
        sales=("sales", "sum"),
        profit=("profit", "sum"),
        orders=("order_id", "nunique")
    )
)

# Category performance
category_performance = (
    df.groupby("category", as_index=False)
    .agg(
        sales=("sales", "sum"),
        profit=("profit", "sum"),
        quantity=("quantity", "sum")
    )
)

category_performance["profit_margin_pct"] = (
    category_performance["profit"] /
    category_performance["sales"] * 100
)

# Regional performance
regional_performance = (
    df.groupby("region", as_index=False)
    .agg(
        sales=("sales", "sum"),
        profit=("profit", "sum"),
        orders=("order_id", "nunique")
    )
)

# Top 10 products by sales
top_products = (
    df.groupby("product_name", as_index=False)
    .agg(
        sales=("sales", "sum"),
        profit=("profit", "sum")
    )
    .sort_values("sales", ascending=False)
    .head(10)
)

# Bottom 10 products by profit
loss_products = (
    df.groupby("product_name", as_index=False)
    .agg(
        sales=("sales", "sum"),
        profit=("profit", "sum")
    )
    .sort_values("profit")
    .head(10)
)

# Discount and profitability analysis
discount_analysis = (
    df.groupby("discount", as_index=False)
    .agg(
        sales=("sales", "sum"),
        profit=("profit", "sum"),
        quantity=("quantity", "sum")
    )
)

# Save outputs
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

kpis.to_csv(OUTPUT_DIR / "business_kpis.csv", index=False)
monthly_trends.to_csv(OUTPUT_DIR / "monthly_trends.csv", index=False)
category_performance.to_csv(OUTPUT_DIR / "category_performance.csv", index=False)
regional_performance.to_csv(OUTPUT_DIR / "regional_performance.csv", index=False)
top_products.to_csv(OUTPUT_DIR / "top_products.csv", index=False)
loss_products.to_csv(OUTPUT_DIR / "loss_making_products.csv", index=False)
discount_analysis.to_csv(OUTPUT_DIR / "discount_analysis.csv", index=False)

# Display summary
print("\n" + "=" * 50)
print("SUPERSTORE BUSINESS ANALYSIS")
print("=" * 50)

print("\nKEY BUSINESS KPIs")
print(kpis.to_string(index=False))

print("\nCATEGORY PERFORMANCE")
print(category_performance.round(2).to_string(index=False))

print("\nREGIONAL PERFORMANCE")
print(regional_performance.round(2).to_string(index=False))

print("\nTOP 10 PRODUCTS BY SALES")
print(top_products.round(2).to_string(index=False))

print("\nTOP 10 LOSS-MAKING PRODUCTS")
print(loss_products.round(2).to_string(index=False))

print("\nEDA completed successfully!")
print(f"Results saved in: {OUTPUT_DIR}")
