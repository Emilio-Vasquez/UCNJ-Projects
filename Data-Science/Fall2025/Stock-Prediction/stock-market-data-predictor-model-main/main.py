# I would like to thank grok for doing the refactoring
# the prompt was to refactor from the previous yfinance data to FMP... it needed help but hey it did a 1 hour job in 10 minutes!!!!

import requests
import pandas as pd
import os
from datetime import datetime, timedelta
import time

from dotenv import load_dotenv

load_dotenv()
FMP_API_KEY = os.getenv("FMP_API_KEY")
BASE_URL = "https://financialmodelingprep.com"
api_call_count = 0
MAX_CALLS_PER_TICKER = 15

tickers = ["NVDA", "AAPL", "MSFT", "TSLA", "ORCL", "META", "GOOG", "JPM", "TSM", "XOM"]

# Free tier: ~5 years historical prices max, so adjust start_date
start_date = (datetime.today() - timedelta(days=5 * 365 + 1)).strftime("%Y-%m-%d")
end_date = datetime.today().strftime("%Y-%m-%d")
output_dir = "datasets_fmp_free"

os.makedirs(output_dir, exist_ok=True)


# ===== HELPER FUNCTIONS =====
def fetch_fmp(endpoint, params=None):
    """Fetch data from FMP API with error handling"""
    global api_call_count

    if params is None:
        params = {}
    params["apikey"] = FMP_API_KEY

    try:
        api_call_count += 1
        print(f"      [API Call #{api_call_count}]", end=" ")

        response = requests.get(f"{BASE_URL}/{endpoint}", params=params)
        response.raise_for_status()
        data = response.json()
        time.sleep(0.5)
        return data
    except Exception as e:
        print(f"Error: {e}")
        return None


def fetch_historical_prices(ticker, from_date, to_date):
    """Fetch historical daily EOD prices - Free tier (~5yr max)"""
    endpoint = "stable/historical-price-eod/full"
    params = {"symbol": ticker}
    data = fetch_fmp(endpoint, params)

    if data:
        df = pd.DataFrame(data)
        if not df.empty and "date" in df.columns:
            df = df.drop(columns=["symbol"], errors="ignore")
            df["date"] = pd.to_datetime(df["date"])
            df.set_index("date", inplace=True)
            df.sort_index(inplace=True)

            df = df[(df.index >= from_date) & (df.index <= to_date)]
            return df

    return pd.DataFrame()


def fetch_income_statements(ticker, period="annual", limit=5):
    """Fetch income statements (annual, 5yr max for free)"""
    endpoint = "stable/income-statement"
    params = {"symbol": ticker, "period": period, "limit": limit}
    data = fetch_fmp(endpoint, params)

    if data:
        df = pd.DataFrame(data)
        if not df.empty and "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])
            df["period_type"] = period
            return df
    return pd.DataFrame()


def fetch_balance_sheets(ticker, period="annual", limit=5):
    """Fetch balance sheet statements (annual, 5yr max)"""
    endpoint = "stable/balance-sheet-statement"
    params = {"symbol": ticker, "period": period, "limit": limit}
    data = fetch_fmp(endpoint, params)

    if data:
        df = pd.DataFrame(data)
        if not df.empty and "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])
            df["period_type"] = period
            return df
    return pd.DataFrame()


def fetch_cash_flow(ticker, period="annual", limit=5):
    """Fetch cash flow statements (annual, 5yr max)"""
    endpoint = "stable/cash-flow-statement"
    params = {"symbol": ticker, "period": period, "limit": limit}
    data = fetch_fmp(endpoint, params)

    if data:
        df = pd.DataFrame(data)
        if not df.empty and "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])
            df["period_type"] = period
            return df
    return pd.DataFrame()


def fetch_key_metrics(ticker, period="annual", limit=5):
    """Fetch key financial metrics (annual, 5yr max)"""
    endpoint = "stable/key-metrics"
    params = {"symbol": ticker, "period": period, "limit": limit}
    data = fetch_fmp(endpoint, params)

    if data:
        df = pd.DataFrame(data)
        if not df.empty and "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"])
            return df
    return pd.DataFrame()


def fetch_company_profile(ticker):
    """Fetch company profile (free for popular symbols)"""
    endpoint = "stable/profile"
    params = {"symbol": ticker}
    data = fetch_fmp(endpoint, params)

    if data and len(data) > 0:
        return data[0]
    return {}


def merge_fundamental_data(daily_df, fundamental_dfs):
    """Merge fundamental data with daily price data using forward fill"""
    merged = daily_df.copy()

    for name, df in fundamental_dfs.items():
        if df.empty:
            continue

        if "date" in df.columns:
            df_indexed = df.set_index("date").sort_index()
            df_indexed.columns = [f"{name}_{col}" for col in df_indexed.columns]
            df_reindexed = df_indexed.reindex(merged.index, method="ffill")
            merged = pd.concat([merged, df_reindexed], axis=1)

    return merged


def calculate_weighted_shares_outstanding(df):
    """
    Blends reported shares with market-derived (marketCap / price) based on report proximity.
    Adapted for annual data (365-day scale).
    """
    shares_cols = [
        col
        for col in df.columns
        if "sharesOutstanding" in col.lower() or "commonstock" in col.lower()
    ]
    marketcap_cols = [col for col in df.columns if "marketcap" in col.lower()]

    if not shares_cols or not marketcap_cols:
        print("    ⚠ No shares/marketcap cols for weighting")
        return df

    shares_col = shares_cols[0]
    marketcap_col = marketcap_cols[0]

    price_col = "adjClose" if "adjClose" in df.columns else "close"
    if price_col not in df.columns:
        print("    ⚠ No price col for market-derived shares")
        return df

    df["market_derived_shares"] = df[marketcap_col] / df[price_col]
    df["reported_shares"] = df[shares_col]
    df["shares_changed"] = df["reported_shares"].ne(df["reported_shares"].shift())

    report_dates = df[df["shares_changed"]].index

    df["days_since_report"] = 0
    df["days_until_next_report"] = 0

    for date in df.index:
        recent = report_dates[report_dates <= date]
        upcoming = report_dates[report_dates > date]

        if len(recent) > 0:
            df.loc[date, "days_since_report"] = (date - recent[-1]).days
        if len(upcoming) > 0:
            df.loc[date, "days_until_next_report"] = (upcoming[0] - date).days

    df["report_progress"] = df["days_since_report"] / (
        df["days_since_report"] + df["days_until_next_report"] + 1
    )
    df["report_progress"] = df["report_progress"].fillna(0.5)
    df["market_weight"] = df["report_progress"] ** 2
    df["reported_weight"] = 1 - df["market_weight"]

    df["weighted_shares_outstanding"] = (
        df["reported_weight"] * df["reported_shares"]
        + df["market_weight"] * df["market_derived_shares"]
    )

    mask_nan = df["reported_shares"].isna()
    df.loc[mask_nan, "weighted_shares_outstanding"] = df.loc[
        mask_nan, "market_derived_shares"
    ]

    print(
        f"    ✓ Weighted shares calc'd (reported weight avg: {df['reported_weight'].mean():.2%})"
    )

    # Cleanup
    drop_cols = [
        "shares_changed",
        "days_since_report",
        "days_until_next_report",
        "report_progress",
        "market_weight",
        "reported_weight",
    ]
    df.drop(columns=drop_cols, errors="ignore", inplace=True)

    return df


def fetch_stock_splits(ticker):
    """Fetch historical stock splits (free, limited symbols)"""
    endpoint = "stable/splits"
    params = {"symbol": ticker}
    data = fetch_fmp(endpoint, params)

    if data:
        df = pd.DataFrame(data)
        if not df.empty and "date" in df.columns:
            df = df.drop(columns=["symbol"], errors="ignore")  # Fix overlap
            df["date"] = pd.to_datetime(df["date"])
            df.set_index("date", inplace=True)
            # Assume cols: numerator, denominator
            return df
    return pd.DataFrame()


def fetch_dividends(ticker):
    """Fetch historical dividends (free, limited symbols)"""
    endpoint = "stable/dividends"
    params = {"symbol": ticker}
    data = fetch_fmp(endpoint, params)

    if data:
        df = pd.DataFrame(data)
        if not df.empty and "date" in df.columns:
            df = df.drop(columns=["symbol"], errors="ignore")  # Fix overlap
            df["date"] = pd.to_datetime(df["date"])
            df.set_index("date", inplace=True)
            # Handle amount col (dividend or label)
            if "label" in df.columns:
                df = df.rename(columns={"label": "dividend_amount"})
            elif "dividend" in df.columns:
                df = df.rename(columns={"dividend": "dividend_amount"})
            return df[["dividend_amount"]] if "dividend_amount" in df.columns else df
    return pd.DataFrame()


# ===== MAIN EXECUTION =====
print(
    f"🔥 Free-tier FMP fetch v2: {len(tickers)} tickers (stable endpoints, EOD prices, annual funds)"
)
print(f"Range: {start_date} to {end_date}\n")

for ticker in tickers:
    print(f"\n{'=' * 60}")
    print(f"Processing {ticker}...")
    print(f"{'=' * 60}")

    # Prices first
    print(f"  → Fetching EOD historical prices...")
    daily_data = fetch_historical_prices(
        ticker, pd.to_datetime(start_date), pd.to_datetime(end_date)
    )

    if daily_data.empty:
        print(f"  ✗ No price data for {ticker}, skipping.")
        continue

    print(f"  ✓ {len(daily_data)} days of EOD data")

    # Fundamentals (annual, stable)
    fundamental_data = {}

    print(f"  → Income statements (annual, 5yr)...")
    fundamental_data["income_annual"] = fetch_income_statements(ticker, "annual", 5)
    print(f"  ✓ {len(fundamental_data['income_annual'])} records")

    print(f"  → Balance sheets (annual, 5yr)...")
    fundamental_data["balance_annual"] = fetch_balance_sheets(ticker, "annual", 5)
    print(f"  ✓ {len(fundamental_data['balance_annual'])} records")

    print(f"  → Cash flows (annual, 5yr)...")
    fundamental_data["cashflow_annual"] = fetch_cash_flow(ticker, "annual", 5)
    print(f"  ✓ {len(fundamental_data['cashflow_annual'])} records")

    print(f"  → Key metrics (annual, 5yr)...")
    fundamental_data["metrics_annual"] = fetch_key_metrics(ticker, "annual", 5)
    print(f"  ✓ {len(fundamental_data['metrics_annual'])} records")

    # Profile (stable)
    print(f"  → Company profile...")
    profile = fetch_company_profile(ticker)
    if profile:
        for key, value in profile.items():
            if isinstance(value, (int, float, str)) and not isinstance(value, bool):
                if isinstance(value, str) and len(value) < 200:
                    daily_data[f"profile_{key}"] = value
                elif isinstance(value, (int, float)):
                    daily_data[f"profile_{key}"] = value
        print(f"  ✓ Profile added")
    else:
        print(f"  ⚠ No profile data")

    # Splits & Divs (stable, fixed overlap)
    print(f"  → Stock splits...")
    splits = fetch_stock_splits(ticker)
    if not splits.empty:
        daily_data = daily_data.join(
            splits.rename(
                columns={
                    "numerator": "split_numerator",
                    "denominator": "split_denominator",
                }
            ).fillna(0)
        )  # Ffill 0 for no-split days
    print(f"  ✓ {len(splits)} splits")

    print(f"  → Dividends...")
    dividends = fetch_dividends(ticker)
    if not dividends.empty:
        daily_data = daily_data.join(dividends)
    print(f"  ✓ {len(dividends)} div records")

    # Merge & calc
    print(f"  → Merging fundamentals...")
    merged_data = merge_fundamental_data(daily_data, fundamental_data)

    print(f"  → Weighted shares calc...")
    merged_data = calculate_weighted_shares_outstanding(merged_data)

    merged_data["Year"] = merged_data.index.year

    print(f"  ✓ Dataset: {len(merged_data)} rows × {len(merged_data.columns)} cols")

    # Save yearly CSVs
    print(f"  → Saving by year...")
    for year, df_year in merged_data.groupby("Year"):
        df_year = df_year.drop(columns=["Year"], errors="ignore")
        file_path = f"{output_dir}/{ticker}_{year}.csv"
        df_year.to_csv(file_path, index=True)
        print(f"    ✓ {file_path} ({len(df_year)} rows)")

    print(f"\n  📊 Calls for {ticker}: {api_call_count}")

print("\n" + "=" * 60)
print("=" * 60)
print(
    f"Total calls: {api_call_count}/250 | Data in '{output_dir}' – FCF, shares, ROE primed for buyback magic."
)
