"""
Mobile Sales Data Analysis
Run:
    python src/analyze_mobile_sales.py dataset/mobile_sales.csv

Expected CSV columns:
Brands, Models, Mobile, Memory, Storage, Selling Price,
Original Price, Discount, Rating, R

The original PDF is included in dataset/. It is the source document, not a
machine-clean CSV. Export/clean the table to CSV using the column names above
before running this script. The script validates required fields and writes
summary CSV files to outputs/.
"""
from pathlib import Path
import sys
import pandas as pd
import numpy as np

REQUIRED = [
    "Brands", "Models", "Mobile", "Memory", "Storage",
    "Selling Price", "Original Price", "Discount", "Rating", "R"
]

def load_data(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    # Standardize common header variations.
    df.columns = [str(c).strip() for c in df.columns]
    missing = [c for c in REQUIRED if c not in df.columns]
    if missing:
        raise ValueError(
            "Missing columns: " + ", ".join(missing) +
            "\nPlease rename CSV headers to: " + ", ".join(REQUIRED)
        )
    for col in ["Memory", "Storage", "Selling Price", "Original Price", "Discount", "Rating", "R"]:
        df[col] = pd.to_numeric(
            df[col].astype(str).str.replace(",", "", regex=False).str.strip(),
            errors="coerce"
        )
    df["Brands"] = df["Brands"].astype(str).str.strip()
    df["Mobile"] = df["Mobile"].astype(str).str.strip()
    df = df.dropna(subset=["Brands", "Selling Price", "Original Price", "Discount", "Rating"])
    df["Discount %"] = np.where(
        df["Original Price"] > 0,
        df["Discount"] / df["Original Price"] * 100,
        0
    )
    return df

def main():
    if len(sys.argv) < 2:
        print("Usage: python src/analyze_mobile_sales.py dataset/mobile_sales.csv")
        sys.exit(1)

    csv_path = Path(sys.argv[1])
    df = load_data(csv_path)
    out = Path("outputs")
    out.mkdir(exist_ok=True)

    # Q1: brand with most records/models
    brand_count = df.groupby("Brands").size().sort_values(ascending=False)
    brand_count.rename("Model records").to_csv(out / "q1_brand_counts.csv")

    # Q2: top 10 by selling price
    df.nlargest(10, "Selling Price").to_csv(out / "q2_top10_selling_price.csv", index=False)

    # Q3-Q5: brand-level averages
    brand_avg = df.groupby("Brands").agg(
        Model_records=("Mobile", "count"),
        Average_selling_price=("Selling Price", "mean"),
        Average_discount=("Discount", "mean"),
        Average_rating=("Rating", "mean")
    ).sort_values("Average_selling_price", ascending=False)
    brand_avg.to_csv(out / "q3_q4_q5_brand_averages.csv")

    # Q6: storage comparison
    storage_avg = df.groupby("Storage").agg(
        Model_records=("Mobile", "count"),
        Average_selling_price=("Selling Price", "mean"),
        Average_rating=("Rating", "mean")
    ).sort_index()
    storage_avg.to_csv(out / "q6_storage_comparison.csv")

    # Q7: highest discount amount and discount percentage
    df.nlargest(10, "Discount").to_csv(out / "q7_top_discounts.csv", index=False)

    # Q8: memory-storage combinations (at least 3 records for stability)
    combo = df.groupby(["Memory", "Storage"]).agg(
        Model_records=("Mobile", "count"),
        Average_selling_price=("Selling Price", "mean"),
        Average_rating=("Rating", "mean")
    ).query("Model_records >= 3").sort_values(
        ["Average_rating", "Average_selling_price"],
        ascending=[False, True]
    )
    combo.to_csv(out / "q8_memory_storage_combinations.csv")

    # Q9: transparent value score based on percentile ranks
    scored = df.copy()
    scored["Value score"] = (
        0.40 * scored["Rating"].rank(pct=True) +
        0.20 * scored["Discount %"].rank(pct=True) +
        0.20 * scored["Storage"].rank(pct=True) +
        0.10 * scored["Memory"].rank(pct=True) +
        0.10 * (1 - scored["Selling Price"].rank(pct=True))
    ) * 100
    scored.nlargest(10, "Value score").to_csv(out / "q9_top10_value_for_money.csv", index=False)

    # Q10: R is treated as the provided class/label; its meaning must be
    # confirmed with the dataset owner.
    class_summary = df.groupby("R").agg(
        Records=("Mobile", "count"),
        Average_price=("Selling Price", "mean"),
        Average_discount=("Discount", "mean"),
        Average_rating=("Rating", "mean"),
        Average_memory=("Memory", "mean"),
        Average_storage=("Storage", "mean")
    )
    class_summary.to_csv(out / "q10_R_class_summary.csv")

    correlations = df[["Selling Price", "Discount", "Rating", "Memory", "Storage", "R"]].corr()["R"]
    correlations.drop("R").sort_values(key=abs, ascending=False).to_csv(
        out / "q10_correlations_with_R.csv", header=["Correlation"]
    )

    print(f"Analysis complete. {len(df)} valid records processed.")
    print(f"Results saved in: {out.resolve()}")

if __name__ == "__main__":
    main()
