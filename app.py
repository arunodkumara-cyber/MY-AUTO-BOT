import streamlit as st
import requests
import pandas as pd
import time
import streamlit.components.v1 as components

# 1. Page Configuration
st.set_page_config(page_title="KD AI AUTO TRADER PRO", layout="wide")

# API Configuration (You will enter these in the UI)
# Note: In a real app, use st.secrets for safety
BINANCE_API_KEY = st.sidebar.text_input("Binance API Key", type="password")
BINANCE_API_SECRET = st.sidebar.text_input("Binance Secret Key", type="password")
TRADE_AMOUNT = st.sidebar.number_input("Trade Amount (USDT)", min_value=10.0, value=15.0)

# Custom Dark Theme CSS
st.markdown("""
    <style>
    .main { background-color: #0b0e11; color: #eaecef; }
    .stMetric { background-color: #1e2329; border-radius: 10px; padding: 15px; border: 1px solid #474d57; }
    .trade-log { background-color: #1c1c1c; padding: 10px; border-radius: 5px; font-family: monospace; color: #00ff00; }
    .stButton>button { background-color: #f0b90b; color: black; width: 100%; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 2. RSI Calculation Function
def get_rsi(symbol):
    try:
        url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1h&limit=50"
        res = requests.get(url, timeout=5).json()
        if not isinstance(res, list) or len(res) < 20: return 50
        closes = [float(c[4]) for c in res]
        gains = [max(0, closes[i] - closes[i-1]) for i in range(1, len(closes))]
        losses = [max(0, closes[i-1] - closes[i]) for i in range(1, len(closes))]
        avg_gain = sum(gains[-14:]) / 14
        avg_loss = sum(losses[-14:]) / 14
        rs = avg_gain / (avg_loss if avg_loss != 0 else 1)
        return round(100 - (100 / (1 + rs)), 2)
    except: return 50

# 3. Market Scan Function
def get_market_data():
    try:
        url = "https://api.binance.com/api/v3/ticker/24hr"
        res = requests.get(url, timeout=5).json()
        df = pd.DataFrame(res)
        df = df[df['symbol'].str.endswith('USDT')]
        exclude = ['USDCUSDT', 'FDUSDUSDT', 'TUSDUSDT', 'DAIUSDT']
        df = df[~df['symbol'].isin(exclude)]
        df['lastPrice'] = df['lastPrice'].astype(float)
        df['priceChangePercent'] = df['priceChangePercent'].astype(float)
        return df
    except: return pd.DataFrame()

# 4. Auto Trading Logic (Mock Function for Safety)
def execute_auto_trade(symbol, price, rsi):
    st.write(f"🚀 [AUTO-TRADE] Attempting to Buy {symbol} at ${price} (RSI: {rsi})")
    # Here we would integrate the real Binance python-binance library
    # For now, it logs the virtual trade
    st.success(f"Successfully placed Virtual Order for {symbol}")

# UI Layout
st.title("🤖 KD AI AUTO TRADER PRO")
st.write("Full Automated Scanning & Execution System")

# Fixed Run Button Logic
if st.button('START FULL AUTO SCAN & TRADE'):
    status_box = st.empty()
    status_box.info("System Initialized. Scanning Market...")
    
    all_coins = get_market_data()
    if not all_coins.empty:
        top_coins = all_coins.sort_values(by='priceChangePercent').head(10).copy()
        top_coins['RSI'] = top_coins['symbol'].apply(get_rsi)
        
        st.subheader("📊 Current Market Analysis")
        st.dataframe(top_coins[['symbol', 'lastPrice', 'priceChangePercent', 'RSI']], use_container_width=True)
        
        # Check for Auto-Trade signals
        st.subheader("📡 Real-time Trading Logs")
        found_signal = False
        for _, row in top_coins.iterrows():
            if row['RSI'] < 35:  # Auto-Trade Condition
                execute_auto_trade(row['symbol'], row['lastPrice'], row['RSI'])
                found_signal = True
        
        if not found_signal:
            st.warning("No high-probability signals found in this cycle.")
            
    else:
        st.error("Market data unreachable. Check connection.")

else:
    st.info("System is IDLE. Click the gold button to start the bot.")

st.divider()
st.subheader("🔍 Manual Chart View")
selected_coin = st.selectbox("Select Asset", ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT"])
chart_html = f"""
    <div style="height:450px;">
        <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
        <script type="text/javascript">
        new TradingView.widget({{"width": "100%", "height": 450, "symbol": "BINANCE:{selected_coin}", "interval": "H", "theme": "dark", "style": "1", "locale": "en"}});
        </script>
    </div>
"""
components.html(chart_html, height=470)





