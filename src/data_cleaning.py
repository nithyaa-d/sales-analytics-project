
"""
Project: Sales Analytics & Business Intelligence
File: src/data_cleaning.py

Purpose:
    Load, clean, validate and prepare retail sales data
    for SQL analysis and business intelligence.
"""

from pathlib import Path
import pandas as pd


# ------------------------------------------------------------
# 1. PROJECT PATHS
# ------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "superstore.csv"

PROCESSED_DATA_PATH = (
    PROJECT_ROOT / "data" / "processed" / "superstore_cleaned.csv"
)

REPORT_PATH = (
    PROJECT_ROOT / "outputs" / "data_quality_report.txt"
)


# ------------------------------------------------------------
# 2. LOAD DATA
# ------------------------------------------------------------

def load_data(file_path: Path) -> pd.DataFrame:
    """Load the raw Superstore dataset."""

    if not file_path.exists():
        raise FileNotFoundError(
            f"Dataset not found: {file_path}"
        )

    df = pd.read_csv(file_path)

    print(f"Dataset loaded successfully: {df.shape}")
    return df


# ------------------------------------------------------------
# 3. STANDARDISE COLUMN NAMES
# ------------------------------------------------------------

def standardise_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Convert column names into lowercase snake_case."""

    df = df.copy()

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(r"[^a-z0-9]+", "_", regex=True)
        .str.strip("_")
    )

    return df


# ------------------------------------------------------------
# 4. CONVERT DATA TYPES
# ------------------------------------------------------------

def convert_data_types(df: pd.DataFrame) -> pd.DataFrame:
    """Convert dates, numeric fields and identifiers."""

    df = df.copy()

    date_columns = ["order_date", "ship_date"]

    numeric_columns = [
        "sales",
        "quantity",
        "discount",
        "profit"
    ]

    for column in date_columns:
        if column in df.columns:
            df[column] = pd.to_datetime(
                df[column],
                errors="coerce"
            )

    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    # Identifiers and postal codes should remain strings.
    identifier_columns = [
        "row_id",
        "order_id",
        "customer_id",
        "product_id",
        "postal_code"
    ]

    for column in identifier_columns:
        if column in df.columns:
            df[column] = df[column].astype("string")

    return df


# ------------------------------------------------------------
# 5. REMOVE EXACT DUPLICATE ROWS
# ------------------------------------------------------------

def remove_exact_duplicates(
    df: pd.DataFrame
) -> tuple[pd.DataFrame, int]:
    """Remove only completely identical records."""

    initial_count = len(df)

    df = df.drop_duplicates().copy()

    removed_count = initial_count - len(df)

    print(f"Exact duplicate rows removed: {removed_count}")

    return df, removed_count


# ------------------------------------------------------------
# 6. VALIDATE BUSINESS RULES
# ------------------------------------------------------------

def validate_data(
    df: pd.DataFrame
) -> dict:
    """Identify potential data quality issues."""

    report = {}

    report["total_records"] = len(df)
    report["duplicate_row_ids"] = int(
        df["row_id"].duplicated().sum()
    )

    report["missing_values"] = (
        df.isnull().sum().to_dict()
    )

    report["invalid_sales"] = int(
        (df["sales"] <= 0).sum()
        + df["sales"].isna().sum()
    )

    report["invalid_quantity"] = int(
        (df["quantity"] <= 0).sum()
        + df["quantity"].isna().sum()
    )

    report["invalid_discount"] = int(
        (
            (df["discount"] < 0)
            | (df["discount"] > 1)
        ).sum()
        + df["discount"].isna().sum()
    )

    report["invalid_date_sequence"] = int(
        (
            df["ship_date"] < df["order_date"]
        ).sum()
    )

    report["negative_profit_records"] = int(
        (df["profit"] < 0).sum()
    )

    return report


# ------------------------------------------------------------
# 7. GENERATE DATA QUALITY REPORT
# ------------------------------------------------------------

def save_quality_report(
    report: dict,
    file_path: Path
) -> None:
    """Save data quality findings to a text file."""

    file_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(file_path, "w", encoding="utf-8") as file:

        file.write("SALES ANALYTICS - DATA QUALITY REPORT\n")
        file.write("=" * 45 + "\n\n")

        file.write(
            f"Total records: {report['total_records']}\n"
        )

        file.write(
            f"Duplicate row IDs: "
            f"{report['duplicate_row_ids']}\n"
        )

        file.write(
            f"Invalid sales records: "
            f"{report['invalid_sales']}\n"
        )

        file.write(
            f"Invalid quantity records: "
            f"{report['invalid_quantity']}\n"
        )

        file.write(
            f"Invalid discount records: "
            f"{report['invalid_discount']}\n"
        )

        file.write(
            f"Invalid date sequences: "
            f"{report['invalid_date_sequence']}\n"
        )

        file.write(
            f"Negative profit records: "
            f"{report['negative_profit_records']}\n"
        )

        file.write("\nMISSING VALUES BY COLUMN\n")
        file.write("-" * 30 + "\n")

        for column, count in report["missing_values"].items():
            file.write(f"{column}: {count}\n")

    print(f"Quality report saved: {file_path}")


# ------------------------------------------------------------
# 8. SAVE PROCESSED DATA
# ------------------------------------------------------------

def save_processed_data(
    df: pd.DataFrame,
    file_path: Path
) -> None:
    """Export the cleaned dataset as CSV."""

    file_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        file_path,
        index=False
    )

    print(f"Processed dataset saved: {file_path}")


# ------------------------------------------------------------
# 9. MAIN PIPELINE
# ------------------------------------------------------------

def main():

    print("\nStarting sales data preparation...\n")

    df = load_data(RAW_DATA_PATH)

    df = standardise_columns(df)

    df = convert_data_types(df)

    df, removed_duplicates = remove_exact_duplicates(df)

    report = validate_data(df)

    report["exact_duplicate_rows_removed"] = (
        removed_duplicates
    )

    save_quality_report(report, REPORT_PATH)

    save_processed_data(df, PROCESSED_DATA_PATH)

    print("\nData preparation completed!")
    print(f"Final dataset shape: {df.shape}")


if __name__ == "__main__":
    main()
