import json
from pathlib import Path
from typing import Dict, List

import numpy as np
import pandas as pd

DATA_FILES = [
    "bronx_2021.xlsx",
    "brooklyn_2021.xlsx",
    "manhat_2021.xlsx",
    "queens_2021.xlsx",
    "staten_2021.xlsx",
]

DISTRICT_MAP = {
    1: "Manhattan",
    2: "Bronx",
    3: "Brooklyn",
    4: "Queens",
    5: "Staten Island",
}

HIST_BINS = 100
SCATTER_SAMPLE = 5000
BASE_DIR = Path(__file__).resolve().parent / "datasets"
OUTPUT_JSON = Path("eda_chart_data.json")


def load_all_data(base_dir: Path) -> pd.DataFrame:
    frames: List[pd.DataFrame] = []
    for file_name in DATA_FILES:
        df = pd.read_excel(base_dir / file_name, skiprows=4)
        frames.append(df)
    return pd.concat(frames, ignore_index=True)


def clean_total_df(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["BOROUGH"] = df["BOROUGH"].map(DISTRICT_MAP)
    df["YEAR"] = pd.DatetimeIndex(df["SALE DATE"]).year

    filters = [
        df["SALE PRICE"] > 100,
        df["SALE PRICE"] < 10_000_000,
        df["GROSS SQUARE FEET"] > 10,
        df["GROSS SQUARE FEET"] < 100_000,
        df["LAND SQUARE FEET"] > 5,
        df["LAND SQUARE FEET"] < 25_000,
        df["TOTAL UNITS"] > 0,
        df["YEAR BUILT"] != 0,
        df["COMMERCIAL UNITS"] < 40,
        df["RESIDENTIAL UNITS"] < 500,
        df["YEAR BUILT"] > 1875,
    ]
    for f in filters:
        df = df[f]
    return df


def build_histogram(series: pd.Series, bins: int = HIST_BINS, cap_q: float = 0.99) -> Dict[str, List[float]]:
    series = series.dropna()
    cap = series.quantile(cap_q)
    clipped = series[series <= cap]
    counts, bin_edges = np.histogram(clipped, bins=bins)
    return {"counts": counts.tolist(), "bin_edges": bin_edges.tolist()}


def sample_scatter(x: pd.Series, y: pd.Series, cap_q: float = 0.99) -> List[Dict[str, float]]:
    df = pd.DataFrame({"x": x, "y": y}).dropna()
    x_cap = df["x"].quantile(cap_q)
    y_cap = df["y"].quantile(cap_q)
    df = df[(df["x"] <= x_cap) & (df["y"] <= y_cap)]
    if len(df) > SCATTER_SAMPLE:
        df = df.sample(SCATTER_SAMPLE, random_state=42)
    return df.to_dict(orient="records")


def main():
    total_df = load_all_data(BASE_DIR)
    total_df = clean_total_df(total_df)

    total_df["SALE PRICE LOG"] = np.log1p(total_df["SALE PRICE"])
    total_df["GROSS SQUARE FEET LOG"] = np.log1p(total_df["GROSS SQUARE FEET"])
    total_df["LAND SQUARE FEET LOG"] = np.log1p(total_df["LAND SQUARE FEET"])

    log_df = total_df[
        [
            "SALE PRICE LOG",
            "GROSS SQUARE FEET LOG",
            "LAND SQUARE FEET LOG",
            "RESIDENTIAL UNITS",
            "COMMERCIAL UNITS",
            "YEAR BUILT",
            "ZIP CODE",
            "YEAR",
        ]
    ].copy()
    log_filters = [
        log_df["SALE PRICE LOG"] != 0,
        log_df["GROSS SQUARE FEET LOG"] != 0,
        log_df["GROSS SQUARE FEET LOG"] > 4,
        log_df["LAND SQUARE FEET LOG"] != 0,
    ]
    for f in log_filters:
        log_df = log_df[f]

    output = {
        "houses_per_borough": [
            {"borough": borough, "count": int(count)}
            for borough, count in total_df["BOROUGH"].value_counts().items()
        ],
        "histograms": {
            "sale_price": build_histogram(total_df["SALE PRICE"]),
            "land_square_feet": build_histogram(total_df["LAND SQUARE FEET"]),
            "gross_square_feet": build_histogram(total_df["GROSS SQUARE FEET"]),
        },
        "scatterplots": {
            "gross_sqft_vs_sale_price": sample_scatter(
                total_df["GROSS SQUARE FEET"], total_df["SALE PRICE"]
            ),
            "log_gross_sqft_vs_log_sale_price": sample_scatter(
                log_df["GROSS SQUARE FEET LOG"], log_df["SALE PRICE LOG"]
            ),
            "log_sale_price_vs_log_gross_sqft": sample_scatter(
                log_df["SALE PRICE LOG"], log_df["GROSS SQUARE FEET LOG"]
            ),
        },
        "correlations": {
            "spearman_total": total_df[
                [
                    "RESIDENTIAL UNITS",
                    "COMMERCIAL UNITS",
                    "LAND SQUARE FEET",
                    "GROSS SQUARE FEET",
                    "YEAR BUILT",
                    "SALE PRICE",
                    "YEAR",
                ]
            ]
            .corr(method="spearman")
            .round(6)
            .to_dict(),
            "pearson_log": log_df.corr().round(6).to_dict(),
        },
    }

    OUTPUT_JSON.write_text(
        json.dumps(output, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"Saved chart data to {OUTPUT_JSON.resolve()}")


if __name__ == "__main__":
    main()