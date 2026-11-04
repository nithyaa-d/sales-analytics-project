
from pathlib import Path
import pandas as pd

# ==========================================
# 1. PROJECT PATHS
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_FILE = PROJECT_ROOT / "data" / "raw" / "superstore.csv"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# ==========================================
# 2. LOAD RAW DATA
# ==========================================

print("Loading Superstore dataset...")

df = pd.read_csv(
    RAW_FILE,
    dtype={"Postal Code": "string"},
    encoding="cp1252"
)

initial_rows = len(df)

print(f"Original records: {initial_rows}")

# ==========================================
# 3. STANDARDISE COLUMN NAMES
# ==========================================

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace("/", "_", regex=False)
    .str.replace("-", "_", regex=False)
    .str.replace(" ", "_", regex=False)
)

# ==========================================
# 4. REMOVE EXACT DUPLICATES
# ==========================================

exact_duplicates = int(df.duplicated().sum())
df = df.drop_duplicates().copy()

# ==========================================
# 5. CONVERT DATE COLUMNS
# ==========================================

# Dataset uses DD-MM-YYYY dates.
for column in ["order_date", "ship_date"]:
    df[column] = pd.to_datetime(
        df[column],
        format="mixed",
        dayfirst=True,
        errors="coerce"
    )

# ==========================================
# 6. CONVERT NUMERIC COLUMNS
# ==========================================

numeric_columns = [
    "row_id",
    "sales",
    "quantity",
    "discount",
    "profit"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )

# ==========================================
# 7. DATA QUALITY CHECKS
# ==========================================

duplicate_row_ids = int(
    df["row_id"].duplicated().sum()
)

missing_values = int(df.isnull().sum().sum())

invalid_order_dates = int(
    df["order_date"].isna().sum()
)

invalid_ship_dates = int(
    df["ship_date"].isna().sum()
)

invalid_sales = int(
    (df["sales"] < 0).sum()
)

invalid_quantity = int(
    (df["quantity"] <= 0).sum()
)

invalid_discount = int(
    (
        (df["discount"] < 0) |
        (df["discount"] > 1)
    ).sum()
)

invalid_shipping_dates = int(
    (df["ship_date"] < df["order_date"]).sum()
)

# ==========================================
# 8. CLEAN ESSENTIAL RECORDS
# ==========================================

rows_before_cleaning = len(df)

df_cleaned = df.dropna(
    subset=[
        "row_id",
        "order_id",
        "product_id",
        "order_date"
    ]
).copy()

# Remove duplicate row IDs if any exist.
df_cleaned = df_cleaned.drop_duplicates(
    subset=["row_id"],
    keep="first"
).copy()

df_cleaned["row_id"] = df_cleaned["row_id"].astype(int)

# ==========================================
# 9. SAVE CLEANED DATA
# ==========================================

output_file = (
    PROCESSED_DIR / "superstore_cleaned.csv"
)

df_cleaned.to_csv(
    output_file,
    index=False
)

# ==========================================
# 10. GENERATE QUALITY REPORT
# ==========================================

quality_report = pd.DataFrame({
    "metric": [
        "Initial rows",
        "Exact duplicates removed",
        "Duplicate row IDs",
        "Missing values",
        "Invalid order dates",
        "Invalid shipping dates",
        "Negative sales records",
        "Invalid quantity records",
        "Invalid discount records",
        "Ship date before order date",
        "Final cleaned rows",
        "Rows removed during cleaning"
    ],
    "value": [
        initial_rows,
        exact_duplicates,
        duplicate_row_ids,
        missing_values,
        invalid_order_dates,
        invalid_ship_dates,
        invalid_sales,
        invalid_quantity,
        invalid_discount,
        invalid_shipping_dates,
        len(df_cleaned),
        rows_before_cleaning - len(df_cleaned)
    ]
})

report_file = (
    PROCESSED_DIR / "data_quality_report.csv"
)

quality_report.to_csv(
    report_file,
    index=False
)

# ==========================================
# 11. FINAL SUMMARY
# ==========================================

print("\n" + "=" * 45)
print("DATA CLEANING COMPLETED")
print("=" * 45)

print(f"Original records : {initial_rows}")
print(f"Cleaned records  : {len(df_cleaned)}")
print(f"Duplicates       : {exact_duplicates}")
print(f"Invalid dates    : {invalid_order_dates}")

print("\nGenerated files:")
print(output_file)
print(report_file)

print("=" * 45)
