import pandas as pd
import yfinance as yf
from datetime import datetime
import os

os.makedirs("datasets", exist_ok=True)

print("Downloading S&P 500 (3 years)...")
sp500 = yf.download("^GSPC", period="3y", interval="1d")

sp500.to_csv("datasets/sp_data.csv")

sp500["Year"] = sp500.index.year

for year, df_year in sp500.groupby("Year"):
    df_year.drop(columns=["Year"], inplace=True)
    df_year.to_csv(f"datasets/sp_{year}.csv")

print("done!")
