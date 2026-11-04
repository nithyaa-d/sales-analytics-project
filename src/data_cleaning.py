
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

print("Loading raw Superstore dataset...")

df = pd.read_csv(
    RAW_FILE,
    dtype={"Postal Code": "string"},
    encoding="cp1252"
)

initial_rows = len(df)

print(f"Dataset loaded successfully: {initial_rows} rows")

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

print("Column names standardised.")

# ==========================================
# 4. REMOVE EXACT DUPLICATES
# ==========================================

exact_duplicates = int(df.duplicated().sum())

df = df.drop_duplicates().copy()

print(f"Exact duplicate rows removed: {exact_duplicates}")

# ==========================================
# 5. CONVERT DATA TYPES
# ==========================================

# Convert date columns
for column in ["order_date", "ship_date"]:
    df[column] = pd.to_datetime(
    df[column],
    format="mixed",
    dayfirst=True,
    errors="coerce"
)

# Convert numeric columns
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

print("Data types converted successfully.")

# ==========================================
# 6. DATA QUALITY CHECKS
# ==========================================

duplicate_row_ids = int(
    df["row_id"].duplicated().sum()
)

missing_values_total = int(
    df.isnull().sum().sum()
)

missing_order_ids = int(
    df["order_id"].isnull().sum()
)

missing_product_ids = int(
    df["product_id"].isnull().sum()
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

invalid_dates = int(
    (df["ship_date"] < df["order_date"]).sum()
)

print("Data quality checks completed.")

# ==========================================
# 7. CLEAN ESSENTIAL RECORDS
# ==========================================

# Remove records missing essential identifiers
# or order dates.

df_cleaned = df.dropna(
    subset=[
        "row_id",
        "order_id",
        "product_id",
        "order_date"
    ]
).copy()

# Keep only the first occurrence of duplicate row IDs.
df_cleaned = df_cleaned.drop_duplicates(
    subset=["row_id"],
    keep="first"
).copy()

# Convert row_id to integer after removing missing values.
df_cleaned["row_id"] = df_cleaned["row_id"].astype(int)

# ==========================================
# 8. SAVE CLEANED DATASET
# ==========================================

output_file = (
    PROCESSED_DIR / "superstore_cleaned.csv"
)

df_cleaned.to_csv(
    output_file,
    index=False
)

# ==========================================
# 9. GENERATE DATA QUALITY REPORT
# ==========================================

quality_report = pd.DataFrame({
    "metric": [
        "Initial rows",
        "Rows after exact duplicate removal",
        "Exact duplicate rows removed",
        "Duplicate row IDs before cleaning",
        "Total missing values before cleaning",
        "Missing order IDs",
        "Missing product IDs",
        "Rows with negative sales",
        "Rows with invalid quantity",
        "Rows with invalid discount",
        "Rows with ship date before order date",
        "Final cleaned rows",
        "Rows removed during essential-field cleaning"
    ],

    "value": [
        initial_rows,
        len(df),
        exact_duplicates,
        duplicate_row_ids,
        missing_values_total,
        missing_order_ids,
        missing_product_ids,
        invalid_sales,
        invalid_quantity,
        invalid_discount,
        invalid_dates,
        len(df_cleaned),
        len(df) - len(df_cleaned)
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
# 10. FINAL SUMMARY
# ==========================================

print("\n" + "=" * 45)
print("DATA CLEANING COMPLETED SUCCESSFULLY")
print("=" * 45)

print(f"Initial rows       : {initial_rows}")
print(f"Cleaned rows       : {len(df_cleaned)}")
print(f"Duplicates removed : {exact_duplicates}")

print(f"\nCleaned dataset saved to:")
print(output_file)

print(f"\nQuality report saved to:")
print(report_file)

print("=" * 45)
