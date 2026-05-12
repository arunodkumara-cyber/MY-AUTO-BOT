import streamlit as st
import requests
import pandas as pd
import streamlit.components.v1 as components

# 1. Page Setup
st.set_page_config(page_title="KD AI AUTO BOT", layout="wide", initial_sidebar_state="expanded")

# Custom Dark Theme CSS
st.markdown("""
    <style>
    .main { background-color: #0b0e11; color: #eaecef; }
    .stMetric { background-color: #1e2329; border-radius: 10px; padding: 15px; border: 1px solid #474d57; }
    .signal-card { background-color: #2b3139; padding: 20px; border-radius: 15px; border-left: 5px solid #00ff00; }
    </style>
    """, unsafe_allow_html=True)

# 2. RSI Calculation Function (With safety checks)
def get_rsi(symbol):
    try:
        url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1h&limit=50"
        data = requests.get(url).json()
        if not isinstance(data, list) or len(data) < 14: return 50
        
        closes = [float(c[4]) for c in data]
        gains = [max(0, closes[i] - closes[i-1]) for i in range(1, len(closes))]
        losses = [max(0, closes[i-1] - closes[i]) for i in range(1, len(closes))]
        avg_gain = sum(gains[-14:]) / 14
        avg_loss = sum(losses[-14:]) / 14
        rs = avg_gain / (avg_loss if avg_loss != 0 else 1)
        return round(100 - (100 / (1 + rs)), 2)
    except: return 50

# 3. Fixed Market Data Function (Fixes the ValueError)
def get_market_data():
    try:
        url = "https://api.binance.com/api/v3/ticker/24hr"
        res = requests.get(url).json()
        # Check if the response is a list as expected
        if isinstance(res, list):
            df = pd.DataFrame(res)
            # Filter for USDT pairs
            df = df[df['symbol'].str.endswith('USDT')]
            return df
        else:
            return pd.DataFrame()
    except Exception as e:
        return pd.DataFrame()

# Header Area
st.title("🤖 KD AI AUTO BOT - Pro Dashboard")
st.write("Real-time Technical Analysis & Virtual Portfolio")

# Sidebar
st.sidebar.title("💳 Virtual Wallet")
st.sidebar.metric("Available Balance", "$30.00", "+0.00%")
st.sidebar.divider()
selected_coin = st.sidebar.selectbox("Select Coin for Chart", ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "DOGEUSDT"])
=


