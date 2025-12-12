import os
import ast
import numpy as np
import pandas as pd
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib


class DilutionModel:
    DESIRED_COLS = [
        "market_derived_shares",
        "cashflow_annual_netStockIssuance",
        "balance_annual_totalDebt",
        "cashflow_annual_commonStockRepurchased",
        "profile_lastDividend",
        "metrics_annual_earningsYield",
        "profile_fullTimeEmployees",
        "metrics_annual_peRatio",
    ]

    def __init__(self, data_path="./datasets_fmp_free/", alg_path="alg"):
        self.data_path = data_path
        self.alg_path = alg_path
        self.model = None
        self.scaler = None
        self.columns = None
        os.makedirs(self.alg_path, exist_ok=True)

    # ==================================================
    # VALUE CLEANING
    # ==================================================
    @staticmethod
    def clean_numeric(x):
        """Safely convert a messy cell to float."""
        if isinstance(x, (int, float, np.int64, np.float64)):
            return float(x)

        if isinstance(x, (list, tuple, np.ndarray)):
            return DilutionModel.clean_numeric(x[0])

        if isinstance(x, str):
            txt = x.strip()

            # Possible stringified list "[123, 14]"
            if txt.startswith("[") and txt.endswith("]"):
                try:
                    arr = ast.literal_eval(txt)
                    return DilutionModel.clean_numeric(arr[0])
                except:
                    pass

            for ch in [",", "$", "%"]:
                txt = txt.replace(ch, "")

            try:
                return float(txt)
            except:
                return np.nan

        return np.nan

    # ==================================================
    # FEATURE ENGINEERING
    # ==================================================
    def engineer_features(self, df):
        """Generate meaningful predictive features."""

        df["feature_debt_per_share"] = (
            df["balance_annual_totalDebt"] / df["market_derived_shares"]
        )

        df["feature_dilution_ratio"] = df["cashflow_annual_netStockIssuance"] / (
            abs(df["cashflow_annual_commonStockRepurchased"]) + 1
        )

        df["feature_price_to_earnings_inverse"] = 1 / (
            df["metrics_annual_earningsYield"] + 1e-9
        )

        df["feature_log_totalDebt"] = np.log(df["balance_annual_totalDebt"] + 1)
        df["feature_log_shares"] = np.log(df["market_derived_shares"] + 1)

        # time-series change features
        for col in self.DESIRED_COLS:
            if col in df.columns:
                df[f"{col}_change"] = df[col].pct_change()
                df[f"{col}_prev1"] = df[col].shift(1)
                df[f"{col}_prev2"] = df[col].shift(2)

        df["feature_dividend_change"] = df["profile_lastDividend"].pct_change()
        df["feature_earningsYield_change"] = df[
            "metrics_annual_earningsYield"
        ].pct_change()

        return df

    # ==================================================
    # LOAD FINANCIAL DATA
    # ==================================================
    def load_financial_data(self):
        dfs = []

        for filename in os.listdir(self.data_path):
            if not filename.endswith(".csv"):
                continue

            print(f"Loading: {filename}")

            try:
                df = pd.read_csv(
                    os.path.join(self.data_path, filename), low_memory=False
                )

                available = [c for c in self.DESIRED_COLS if c in df.columns]
                reduced_df = df[available].copy()
                reduced_df = reduced_df.map(self.clean_numeric)

                dfs.append(reduced_df)
            except Exception as e:
                print(f"Failed reading {filename}: {e}")

        if not dfs:
            raise RuntimeError("❗ No usable financial data found.")

        df = pd.concat(dfs, ignore_index=True)
        df = df.apply(pd.to_numeric, errors="coerce")
        df = self.engineer_features(df)

        return df

    # ==================================================
    # TARGET LABEL
    # ==================================================
    def compute_target(self, df):
        df["netIssuance"] = (
            df["cashflow_annual_netStockIssuance"]
            - df["cashflow_annual_commonStockRepurchased"]
        )

        max_abs = df["netIssuance"].abs().max()
        df["dilution_signal"] = (df["netIssuance"] / max_abs).clip(-1, 1)

        return df

    # ==================================================
    # TRAINING
    # ==================================================
    def train(self, df):
        df = df.dropna(subset=["dilution_signal"])
        df = df.select_dtypes(include=[np.number])

        X = df.drop(columns=["dilution_signal"])
        y = df["dilution_signal"]

        X = X.replace([np.inf, -np.inf], np.nan).dropna()
        y = y.loc[X.index]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)

        self.model = LinearRegression()
        self.model.fit(X_train_scaled, y_train)

        preds = self.model.predict(X_test_scaled)
        score = r2_score(y_test, preds)

        print("=====================================")
        print(f"MODEL TRAINED – R²: {score:.4f}")
        print("=====================================")

        self.columns = list(X.columns)
        self.save_model()

        return score

    # ==================================================
    # SAVE MODEL
    # ==================================================
    def save_model(self):
        joblib.dump(self.model, f"{self.alg_path}/model.pkl")
        joblib.dump(self.scaler, f"{self.alg_path}/scaler.pkl")
        joblib.dump(self.columns, f"{self.alg_path}/columns.pkl")
        print("✔ Model saved successfully.")

    # ==================================================
    # FULL TRAINING PIPELINE
    # ==================================================
    def run_full_training(self):
        df = self.load_financial_data()
        df = self.compute_target(df)
        return self.train(df)


# ======================================================
# MAIN SCRIPT
# ======================================================
def main():
    dm = DilutionModel()
    dm.run_full_training()


if __name__ == "__main__":
    main()
