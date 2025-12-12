from flask import render_template, request, flash
import pandas as pd
import yfinance as yf
import os
from .algorith import StockPredictor

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
MODEL_PATH = os.path.join(ROOT_DIR, "alg/model.pkl")
SCALER_PATH = os.path.join(ROOT_DIR, "alg/scaler.pkl")
COLS_PATH = os.path.join(ROOT_DIR, "alg/columns.pkl")

predictor = StockPredictor(MODEL_PATH, SCALER_PATH, COLS_PATH)


def dashboard():
    prediction = None
    ticker = None
    graph1 = None
    graph2 = None
    graph3 = None
    error_message = None

    if request.method == "POST":
        ticker = request.form.get(
            "ticker",
        ).upper()

        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            financials = stock.financials
            balance_sheet = stock.balance_sheet
            cashflow = stock.cashflow

            data = {
                "marketPrice": info.get("currentPrice", 0),
                "sharesOutstanding": info.get("sharesOutstanding", 0),
                "freeCashFlow": info.get("freeCashflow", 0),
                "operatingCashFlow": info.get("operatingCashflow", 0),
                "totalDebt": info.get("totalDebt", 0),
                "dividendsPaid": (
                    cashflow.loc["Cash Dividends Paid"].iloc[0]
                    if "Cash Dividends Paid" in cashflow.index
                    else 0
                ),
                "netIncome": info.get("netIncomeToCommon", 0),
                "employees": info.get("fullTimeEmployees", 0),
                "stockIssued": (
                    cashflow.loc["Issuance Of Capital Stock"].iloc[0]
                    if "Issuance Of Capital Stock" in cashflow.index
                    else 0
                ),
                "stockRepurchased": (
                    cashflow.loc["Repurchase Of Capital Stock"].iloc[0]
                    if "Repurchase Of Capital Stock" in cashflow.index
                    else 0
                ),
            }

            df_input = pd.DataFrame([data])

            result = predictor.predict(df_input)

            prediction = result[0]
            hist = stock.history(period="1mo")

            if not hist.empty:
                hist_reset = hist.reset_index()
                fig1 = px.line(
                    hist_reset,
                    x="Date",
                    y="Close",
                    title=f"{ticker} Stock Price - Last 30 Days",
                    labels={"Close": "Price ($)", "Date": "Date"},
                )
                fig1.update_traces(line_color="#1f77b4", line_width=2)
                fig1.update_layout(
                    hovermode="x unified",
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                )
                graph1 = fig1.to_html(full_html=False)

                volume_data = hist["Volume"].tail(30)
                avg_volume = volume_data.mean()

                fig2 = go.Figure()
                fig2.add_trace(
                    go.Bar(
                        x=hist_reset["Date"].tail(30),
                        y=volume_data,
                        name="Daily Volume",
                    )
                )
                fig2.add_trace(
                    go.Scatter(
                        x=hist_reset["Date"].tail(30),
                        y=[avg_volume] * len(volume_data),
                        name="Average Volume",
                        line=dict(color="red", dash="dash", width=2),
                    )
                )
                fig2.update_layout(
                    title=f"{ticker} Trading Volume - Last 30 Days",
                    xaxis_title="Date",
                    yaxis_title="Volume",
                    hovermode="x unified",
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                )
                graph2 = fig2.to_html(full_html=False)

            metrics = {
                "Market Cap": (
                    info.get("marketCap", 0) / 1e9 if info.get("marketCap") else 0
                ),  # Convert to billions
                "Total Debt": data["totalDebt"] / 1e9 if data["totalDebt"] else 0,
                "Free Cash Flow": (
                    data["freeCashFlow"] / 1e9 if data["freeCashFlow"] else 0
                ),
                "Net Income": data["netIncome"] / 1e9 if data["netIncome"] else 0,
            }

            metrics = {k: v for k, v in metrics.items() if v != 0}

            if metrics:
                fig3 = px.bar(
                    x=list(metrics.keys()),
                    y=list(metrics.values()),
                    title=f"{ticker} Key Financial Metrics (Billions $)",
                    labels={"x": "Metric", "y": "Value (Billions $)"},
                    color=list(metrics.values()),
                    color_continuous_scale="Blues",
                )
                fig3.update_layout(
                    showlegend=False,
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                )
                graph3 = fig3.to_html(full_html=False)
            else:
                fig3 = px.pie(
                    names=["Data Unavailable"],
                    values=[100],
                    title=f"{ticker} Financial Metrics",
                )
                graph3 = fig3.to_html(full_html=False)

        except Exception as e:
            flash(f"Error analyzing {ticker}: {str(e)}")
            print(f"DEBUG ERROR: {e}")
    return render_template(
        "dashboard.html",
        prediction=prediction,
        ticker=ticker,
        graph1=graph1,
        graph2=graph2,
        graph3=graph3,
    )
