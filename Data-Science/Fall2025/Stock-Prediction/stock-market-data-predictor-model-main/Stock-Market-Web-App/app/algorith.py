import joblib
import pandas as pd
import numpy as np
import ast
import os


# ======================================================
# What does algorith.py do? (yeah I'm to lazy to rename the file)
# ======================================================


"""

Import StockPredictor(df); this is the function that will return two numbers in an array

the return array is [float]

float -> -1: strong buy back tendency
float -> 1: strong issue tendency

The expected param df is a data frame containing the following columns:

        "marketPrice"
        "sharesOutstanding"
        "freeCashFlow"
        "operatingCashFlow"
        "totalDebt"
        "dividendsPaid"
        "netIncome"
        "employees"
        "stockIssued"
        "stockRepurchased"

"""


# ======================================================
# 1) Utility numeric parsing
# ======================================================
def safe_num(x):
    """Converts messy input into a clean float."""
    if isinstance(x, (int, float, np.number)):
        return float(x)

    if isinstance(x, (list, tuple, np.ndarray)):
        return safe_num(x[0])

    if isinstance(x, str):
        txt = x.strip()

        if txt.startswith("[") and txt.endswith("]"):
            try:
                arr = ast.literal_eval(txt)
                return safe_num(arr[0])
            except:
                pass

        txt = txt.replace(",", "").replace("$", "").replace("%", "")
        try:
            return float(txt)
        except:
            return np.nan

    return np.nan


def clean_df_numeric(df: pd.DataFrame) -> pd.DataFrame:
    """Converts all values in the dataframe to numeric floats wherever possible."""
    return df.applymap(safe_num)


# ======================================================
# 2) Feature Engineering
# ======================================================
def add_engineered_features(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates all derived model features from raw primitives."""

    df = clean_df_numeric(df).copy()

    # Base derived intermediate metrics
    df["market_derived_shares"] = df["marketPrice"] * df["sharesOutstanding"]
    df["metrics_annual_earningsYield"] = df["netIncome"] / df["market_derived_shares"]

    # Standard feature names
    df["cashflow_annual_netStockIssuance"] = df["stockIssued"]
    df["balance_annual_totalDebt"] = df["totalDebt"]
    df["cashflow_annual_commonStockRepurchased"] = df["stockRepurchased"]
    df["profile_lastDividend"] = df["dividendsPaid"]
    df["profile_fullTimeEmployees"] = df["employees"]
    df["metrics_annual_peRatio"] = 1 / (df["metrics_annual_earningsYield"] + 1e-9)

    # Model input features
    df["feature_debt_per_share"] = df["totalDebt"] / (df["sharesOutstanding"] + 1e-9)
    df["feature_dilution_ratio"] = df["stockIssued"] / (df["sharesOutstanding"] + 1e-9)
    df["feature_price_to_earnings_inverse"] = df["metrics_annual_earningsYield"]

    return df


# ======================================================
# 3) Column alignment
# ======================================================
def align_to_model_columns(
    df: pd.DataFrame, col_path="alg/columns.pkl"
) -> pd.DataFrame:
    """Ensures df has exactly the columns used at training."""
    col_order = joblib.load(col_path)

    # add missing columns
    missing = [c for c in col_order if c not in df.columns]
    for col in missing:
        df[col] = 0

    # reorder properly
    return df[col_order]


# ======================================================
# 4) Model manager for efficient use
# ======================================================
class StockPredictor:
    """Wrapper class to manage model, scaling, and prediction pipeline."""

    def __init__(
        self,
        model_path="alg/model.pkl",
        scaler_path="alg/scaler.pkl",
        col_path="alg/columns.pkl",
    ):

        self.model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)
        self.col_order = joblib.load(col_path)
        self.col_path = col_path

    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        df = add_engineered_features(df)
        df = align_to_model_columns(df, self.col_path)
        return df

    def predict(self, df: pd.DataFrame):
        df = self.preprocess(df)
        X = self.scaler.transform(df)
        return self.model.predict(X)


# ======================================================
# 5) Example usage
# ======================================================


def main():
    test_data = {
        "marketPrice": [150.25, 82.10],
        "sharesOutstanding": [4_500_000_000, 1_200_000_000],
        "freeCashFlow": [92_000_000_000, 8_500_000_000],
        "operatingCashFlow": [120_000_000_000, 10_000_000_000],
        "totalDebt": [70_000_000_000, 3_200_000_000],
        "dividendsPaid": [-14_000_000_000, -650_000_000],
        "netIncome": [33_000_000_000, 2_900_000_000],
        "employees": [163_000, 22_500],
        "stockIssued": [3_000_000_000, 200_000_000],
        "stockRepurchased": [4_500_000_000, 150_000_000],
    }

    df_test = pd.DataFrame(test_data)
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(BASE_DIR, "../alg/model.pkl")
    model_path = os.path.abspath(model_path)
    scaler_path = os.path.abspath(os.path.join(BASE_DIR, "../alg/scaler.pkl"))
    cols_path = os.path.abspath(os.path.join(BASE_DIR, "../alg/columns.pkl"))

    model = StockPredictor(model_path, scaler_path, cols_path)
    preds = model.predict(df_test)

    print("\n=== ENGINEERED DF SAMPLE ===")
    print(model.preprocess(df_test).head())

    print("\n=== MODEL PREDICTIONS ===")
    print(preds)


if __name__ == "__main__":
    main()
