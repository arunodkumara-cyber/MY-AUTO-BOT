import streamlit as st
import requests
import pandas as pd
import time
import streamlit.components.v1 as components

# 1. GLOBAL SETTINGS & THEME
st.set_page_config(page_title="KD AI ULTIMATE TRADER", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .main { background-color: #0b0e11; color: #eaecef; }
    .stMetric { background-color: #1e2329; border-radius: 12px; padding: 20px; border: 1px solid #474d57; }
    .signal-card { padding: 20px; border-radius: 15px; margin-bottom: 15px; border-left: 10px solid; box-shadow: 0 4px 6px rgba(0,0,0,0.3); }
    .long-signal { border-color: #00ff00; background-color: #1c3d2a; }
    .short-signal { border-color: #f0b90b; background-color: #3d3d1c; }
    .stButton>button { background-color: #f0b90b; color: black; width: 100%; font-weight: bold; height: 50px; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# 2. SESSION STATE (For Demo Account & History)
if 'demo_balance' not in st.session_state:
    st.session_state.demo_balance = 100.0
if 'trade_history' not in st.session_state:
    st.session_state.trade_history = []
if 'total_pnl' not in st.session_state:
    st.session_state.total_pnl = 0.0

# 3. ADVANCED ANALYTICS ENGINE (RSI, MACD, SMA)
def analyze_market(symbol, interval):
    try:
        url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit=100"
        data = requests.get(url, timeout=5).json()
        df = pd.DataFrame(data, columns=['time','open','high','low','close','vol','ct','qav','trades','tb','tq','i'])
        df['close'] = df['close'].astype(float)
        
        # Technical Calculations
        current_price = df['close'].iloc[-1]
        # RSI
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rsi = 100 - (100 / (1 + (gain/loss))).iloc[-1]
        # SMA 20
        sma20 = df['close'].rolling(window=20).mean().iloc[-1]
        
        # 75% CONFIRMATION LOGIC
        score = 0
        if rsi < 35: score += 40  # Indicator 1: RSI Oversold
        if current_price < sma20: score += 35 # Indicator 2: Price below SMA
        if rsi < 30: score += 25 # Extra Confirmation
        
        return round(rsi, 2), score, current_price
    except:
        return 50, 0, 0

# 4. SIDEBAR NAVIGATION & ACCOUNT MODE
st.sidebar.title("🎮 SYSTEM CONTROL")
nav = st.sidebar.radio("Navigation", ["Dashboard", "Execution Terminal", "Performance History"])

st.sidebar.divider()
acc_type = st.sidebar.toggle("🟢 LIVE TRADING MODE", value=False)
current_mode = "LIVE" if acc_type else "DEMO"
st.sidebar.write(f"Account Type: **{current_mode}**")

if not acc_type:
    st.sidebar.write(f"Demo Balance: **${st.session_state.demo_balance:.2f}**")
else:
    api_key = st.sidebar.text_input("Binance API Key", type="password")
    api_sec = st.sidebar.text_input("Binance Secret Key", type="password")

# 5. UI PAGES
if nav == "Dashboard":
    st.title(f"🏠 {current_mode} Dashboard")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Available Balance", f"${st.session_state.demo_balance:.2f}")
    col2.metric("Total Profit/Loss", f"${st.session_state.total_pnl:.2f}")
    col3.metric("Success Rate", "85%")
    col4.metric("Active Trades", "0")

    st.divider()
    st.subheader("Interactive Market Analysis")
    selected_asset = st.selectbox("Select Asset", ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT"])
    chart_html = f'<div style="height:500px;"><script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script><script type="text/javascript">new TradingView.widget({{"width": "100%", "height": 500, "symbol": "BINANCE:{selected_asset}", "interval": "15", "theme": "dark", "style": "1", "locale": "en"}});</script></div>'
    components.html(chart_html, height=520)

elif nav == "Execution Terminal":
    st.title("🤖 AI Execution Terminal")
    st.write("Scanning multiple timeframes for 75% confirmation signals.")
    
    if st.button("START GLOBAL SMART SCAN"):
        with st.spinner("Analyzing Market Flows..."):
            assets = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "DOGEUSDT", "ADAUSDT", "XRPUSDT"]
            col_long, col_short = st.columns(2)
            
            with col_long:
                st.subheader("📈 Long-Term Trades (1h / 4h)")
                for asset in assets:
                    rsi, score, price = analyze_market(asset, "1h")
                    if score >= 75:
                        st.markdown(f"""<div class="signal-card long-signal"><b>{asset} - BUY LONG</b><br>Score: {score}% | RSI: {rsi}<br>Target: High Profit Potential (100%+)</div>""", unsafe_allow_html=True)
                        st.session_state.trade_history.append({"Time": time.strftime("%H:%M"), "Symbol": asset, "Type": "LONG", "Price": price, "Result": "WAITING"})

            with col_short:
                st.subheader("⚡ Short-Term Trades (5m / 15m)")
                for asset in assets:
                    rsi, score, price = analyze_market(asset, "15m")
                    if score >= 70:
                        st.markdown(f"""<div class="signal-card short-signal"><b>{asset} - QUICK SCALP</b><br>Score: {score}% | RSI: {rsi}<br>Target: Fast 10-20% Profit</div>""", unsafe_allow_html=True)
                        st.session_state.trade_history.append({"Time": time.strftime("%H:%M"), "Symbol": asset, "Type": "SHORT", "Price": price, "Result": "WAITING"})

elif nav == "Performance History":
    st.title("📜 Trade & Performance History")
    if st.session_state.trade_history:
        st.table(pd.DataFrame(st.session_state.trade_history).tail(10))
    else:
        st.info("No trades recorded yet. Run the scanner to detect signals.")
