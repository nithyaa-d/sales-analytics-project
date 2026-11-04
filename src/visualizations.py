
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "processed"
FIGURE_DIR = BASE_DIR / "reports" / "figures"

FIGURE_DIR.mkdir(parents=True, exist_ok=True)

# Load data
df = pd.read_csv(DATA_DIR / "superstore_cleaned.csv", parse_dates=["order_date"])
df["order_month"] = df["order_date"].dt.to_period("M").astype(str)

# Consistent chart styling
plt.rcParams.update({
    "figure.figsize": (12, 6),
    "axes.titlesize": 16,
    "axes.labelsize": 11,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "figure.dpi": 120
})

# 1. Monthly sales and profit trend
monthly = df.groupby("order_month")[["sales", "profit"]].sum()

fig, ax = plt.subplots()
ax.plot(monthly.index, monthly["sales"], label="Sales", marker="o")
ax.plot(monthly.index, monthly["profit"], label="Profit", marker="o")
ax.set_title("Monthly Sales and Profit Trend")
ax.set_xlabel("Month")
ax.set_ylabel("Amount (USD)")
ax.tick_params(axis="x", rotation=60)
ax.legend()
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig(FIGURE_DIR / "monthly_sales_profit.png")
plt.close(fig)

# 2. Sales by category
category = df.groupby("category")["sales"].sum().sort_values()

fig, ax = plt.subplots()
category.plot(kind="barh", ax=ax)
ax.set_title("Sales by Product Category")
ax.set_xlabel("Sales (USD)")
ax.set_ylabel("Category")
ax.grid(axis="x", alpha=0.3)
fig.tight_layout()
fig.savefig(FIGURE_DIR / "sales_by_category.png")
plt.close(fig)

# 3. Profit by region
region = df.groupby("region")["profit"].sum().sort_values()

fig, ax = plt.subplots()
region.plot(kind="bar", ax=ax)
ax.set_title("Profit by Region")
ax.set_xlabel("Region")
ax.set_ylabel("Profit (USD)")
ax.grid(axis="y", alpha=0.3)
fig.tight_layout()
fig.savefig(FIGURE_DIR / "profit_by_region.png")
plt.close(fig)

# 4. Discount versus profit
discount = df.groupby("discount")["profit"].sum()

fig, ax = plt.subplots()
discount.plot(kind="bar", ax=ax)
ax.axhline(0, linewidth=1)
ax.set_title("Discount Level vs Total Profit")
ax.set_xlabel("Discount")
ax.set_ylabel("Profit (USD)")
ax.grid(axis="y", alpha=0.3)
fig.tight_layout()
fig.savefig(FIGURE_DIR / "discount_vs_profit.png")
plt.close(fig)

# 5. Top 10 products by sales
top_products = (
    df.groupby("product_name")["sales"]
    .sum()
    .nlargest(10)
    .sort_values()
)

fig, ax = plt.subplots(figsize=(12, 7))
top_products.plot(kind="barh", ax=ax)
ax.set_title("Top 10 Products by Sales")
ax.set_xlabel("Sales (USD)")
ax.set_ylabel("Product")
ax.grid(axis="x", alpha=0.3)
fig.tight_layout()
fig.savefig(FIGURE_DIR / "top_10_products.png")
plt.close(fig)

# 6. Top 10 loss-making products
loss_products = (
    df.groupby("product_name")["profit"]
    .sum()
    .nsmallest(10)
    .sort_values()
)

fig, ax = plt.subplots(figsize=(12, 7))
loss_products.plot(kind="barh", ax=ax)
ax.set_title("Top 10 Loss-Making Products")
ax.set_xlabel("Profit (USD)")
ax.set_ylabel("Product")
ax.axvline(0, linewidth=1)
ax.grid(axis="x", alpha=0.3)
fig.tight_layout()
fig.savefig(FIGURE_DIR / "top_10_loss_products.png")
plt.close(fig)

print("All visualizations generated successfully!")
print(f"Charts saved in: {FIGURE_DIR}")
