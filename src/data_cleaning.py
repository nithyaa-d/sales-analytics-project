
from pathlib import Path
import pandas as pd

# Project directories
PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = PROJECT_ROOT / "data" / "raw" / "superstore.csv"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

# Load raw data
df = pd.read_csv(
    RAW_FILE,
    dtype={"Postal Code": "string"}
)

initial_rows = len(df)

# Standardise column names
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace("/", "_", regex=False)
    .str.replace("-", "_", regex=False)
    .str.replace(" ", "_", regex=False)
)

# Remove exact duplicate records
exact_duplicates = int(df.duplicated().sum())
df = df.drop_duplicates()

# Convert date columns
for column in ["order_date", "ship_date"]:
    df[column] = pd.to_datetime(
        df[column],
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

# Data quality checks
duplicate_row_ids = int(df["row_id"].duplicated().sum())

missing_values = df.isnull().sum()

invalid_sales = int((df["sales"] < 0).sum())
invalid_quantity = int((df["quantity"] <= 0).sum())
invalid_discount = int(
    ((df["discount"] < 0) | (df["discount"] > 1)).sum()
)

invalid_dates = int(
    (df["ship_date"] < df["order_date"]).sum()
)

# Keep rows with essential identifiers and valid order dates
df_cleaned = df.dropna(
    subset=["row_id", "order_id", "product_id", "order_date"]
).copy()

# Save cleaned dataset
output_file = PROCESSED_DIR / "superstore_cleaned.csv"
df_cleaned.to_csv(output_file, index=False)

# Generate data quality report
quality_report = pd.DataFrame({
    "metric": [
        "Initial rows",
        "Rows after removing exact duplicates",
        "Exact duplicate rows removed",
        "Duplicate row IDs",
        "Rows in cleaned dataset",
        "Rows with negative sales",
        "Rows with invalid quantity",
        "Rows with invalid discount",
        "Rows with ship date before order date"
    ],
    "value": [
        initial_rows,
        len(df),
        exact_duplicates,
        duplicate_row_ids,
        len(df_cleaned),
        invalid_sales,
        invalid_quantity,
        invalid_discount,
        invalid_dates
    ]
})

quality_report.to_csv(
    PROCESSED_DIR / "data_quality_report.csv",
    index=False
)

print("Data cleaning completed!")
print(f"Initial rows: {initial_rows}")
print(f"Cleaned rows: {len(df_cleaned)}")
print(f"Exact duplicates removed: {exact_duplicates}")
print(f"Output saved to: {output_file}")
