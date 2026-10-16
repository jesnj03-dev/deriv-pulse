
import streamlit as st
import pandas as pd
import random

st.set_page_config(
    page_title="Deriv Pulse",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Lightweight styling
st.markdown("""
<style>
.stApp {
    background: #0b1020;
    color: #f1f5f9;
}
.block-container {
    max-width: 1150px;
    padding-top: 2rem;
}
.pulse-logo {
    display: flex;
    align-items: center;
    gap: 13px;
    margin-bottom: 8px;
}
.logo-icon {
    width: 54px;
    height: 54px;
    border-radius: 15px;
    background: linear-gradient(135deg, #00e5a0, #00a8ff);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 29px;
}
.pulse-title {
    font-size: 34px;
    font-weight: 800;
    letter-spacing: -1px;
}
.pulse-title span {
    color: #00e5a0;
}
.subtitle {
    color: #94a3b8;
    margin-bottom: 25px;
}
div[data-testid="stMetric"] {
    background: #131c30;
    border: 1px solid #26334d;
    padding: 17px;
    border-radius: 14px;
}
div[data-testid="stMetricValue"] {
    color: #00e5a0;
}
.stSelectbox div[data-baseweb="select"] {
    background: #131c30;
}
</style>
""", unsafe_allow_html=True)

# Creative graph logo and heading
st.markdown("""
<div class="pulse-logo">
    <div class="logo-icon">📈</div>
    <div class="pulse-title">DERIV <span>PULSE</span></div>
</div>
<div class="subtitle">
    SYNTHETIC INDICES · MARKET INSIGHTS · MANUAL TRADING
</div>
""", unsafe_allow_html=True)

st.caption("A lightweight market dashboard built for clarity and speed.")

# Market selector
market = st.selectbox(
    "Choose a market",
    [
        "Volatility 10 Index",
        "Volatility 25 Index",
        "Volatility 50 Index",
        "Volatility 75 Index",
        "Volatility 100 Index"
    ]
)

timeframe = st.selectbox(
    "Chart timeframe",
    ["1 minute", "5 minutes", "15 minutes"]
)

# Demo price data only — not live Deriv data
@st.cache_data
def make_demo_data(selected_market):
    random.seed(selected_market)
    price = 1000.0
    values = []

    for i in range(60):
        price += random.uniform(-5, 5)
        values.append(round(price, 2))

    return pd.DataFrame({"Price": values})

data = make_demo_data(market)

data["Fast Average"] = data["Price"].rolling(5).mean()
data["Slow Average"] = data["Price"].rolling(15).mean()

latest = data["Price"].iloc[-1]
fast = data["Fast Average"].iloc[-1]
slow = data["Slow Average"].iloc[-1]

if fast > slow:
    signal = "BUY BIAS"
    explanation = "The short-term average is above the long-term average."
elif fast < slow:
    signal = "SELL BIAS"
    explanation = "The short-term average is below the long-term average."
else:
    signal = "WAIT"
    explanation = "No clear direction from these averages."

# Dashboard metrics
a, b, c = st.columns(3)

a.metric("Selected Market", market)
b.metric("Latest Demo Price", f"{latest:,.2f}")
c.metric("Demo Signal", signal)

st.divider()

st.subheader("📊 Price Movement")
st.line_chart(data[["Price", "Fast Average", "Slow Average"]])

st.subheader("⚡ Signal Overview")

if signal == "BUY BIAS":
    st.success("BUY BIAS — " + explanation)
elif signal == "SELL BIAS":
    st.error("SELL BIAS — " + explanation)
else:
    st.info("WAIT — " + explanation)

st.caption(f"Selected timeframe: {timeframe}")

st.warning(
    "DEMO MODE: Prices are randomly generated sample data, "
    "not live Deriv prices. These indicators are not real trading signals. "
    "Connect the official Deriv API before using live market data."
)

st.markdown("---")
st.caption("DERIV PULSE • Simple charts. Clear thinking. Trade responsibly.")
