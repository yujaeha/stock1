import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="미국 주식 TOP10",
    page_icon="📈",
    layout="wide"
)

st.title("📈 미국 주식 TOP 10 주가 변동")

stocks = {
    "Tesla": "TSLA",
    "NVIDIA": "NVDA",
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Amazon": "AMZN",
    "Meta": "META",
    "Google": "GOOGL",
    "AMD": "AMD",
    "Palantir": "PLTR",
    "Broadcom": "AVGO"
}

@st.cache_data(ttl=3600)
def get_stock_data():
    result = pd.DataFrame()

    for name, ticker in stocks.items():
        data = yf.download(
            ticker,
            period="1y",
            auto_adjust=True,
            progress=False
        )

        if not data.empty:
            result[name] = data["Close"]

    return result

df = get_stock_data()

st.subheader("🚀 최근 1년 주가 변동")

fig = go.Figure()

for stock in df.columns:
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=df[stock],
            mode="lines",
            name=stock,
            hovertemplate=
            f"<b>{stock}</b><br>" +
            "날짜: %{x}<br>" +
            "가격: $%{y:.2f}<extra></extra>"
        )
    )

fig.update_layout(
    template="plotly_dark",
    height=750,
    hovermode="x unified",
    title="미국 대표 주식 TOP10",
    xaxis_title="날짜",
    yaxis_title="주가($)",
    legend_title="종목"
)

st.plotly_chart(fig, use_container_width=True)
