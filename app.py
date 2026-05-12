import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# --- උසස් පිටු සැකසුම (Pro Theme Configuration) ---
st.set_page_config(page_title="KD AI AUTO BOT PRO", layout="wide", initial_sidebar_state="expanded")

# Custom CSS - image_7.png හි මෙන් Dark-Neon Glow එකක් ලබා ගැනීමට
st.markdown("""
    <style>
    .main { background-color: #0b0e11; color: #e1e1e1; }
    .stMetric { background-color: #1e2329; padding: 15px; border-radius: 10px; border-left: 5px solid #f0b90b; }
    .stTabs [data-baseweb="tab-list"] { gap: 20px; }
    .stTabs [data-baseweb="tab"] { height: 50px; background-color: #1e2329; border-radius: 5px; color: white; }
    .trade-card { border: 1px solid #30363d; padding: 15px; border-radius: 10px; background-color: #161b22; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- Session State (ඩේටා මතකය) ---
if 'bot_running' not in st.session_state: st.session_state.bot_running = False
if 'trade_logs' not in st.session_state: st.session_state.trade_logs = []

# --- Sidebar (API & Account Management) ---
with st.sidebar:
    st.image("https://cryptologos.cc/logos/binance-coin-bnb-logo.png", width=50)
    st.title("KD AI PRO BOT")
    
    st.subheader("🔑 API Connectivity")
    api_key = st.text_input("Binance API Key", type="password", placeholder="Enter Key...")
    api_secret = st.text_input("Binance Secret Key", type="password", placeholder="Enter Secret...")
    
    st.divider()
    mode = st.radio("Execution Mode", ["💎 Live Trading", "🧪 Paper/Demo Trading"])
    
    st.subheader("⚙️ Bot Strategy")
    st.selectbox("Main Indicator", ["Sniper Logic v4", "SMC + Order Block", "EMA Scalper"])
    st.slider("Risk Factor", 0.5, 5.0, 1.5)
    
    if st.button("🔄 Check Connection"):
        st.sidebar.success("Connected to Binance API")

# --- Header Section ---
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.title("🚀 Professional Trading Terminal")
with col_h2:
    if st.session_state.bot_running:
        st.markdown('<h3 style="color:#00ff00;">● SYSTEM ONLINE</h3>', unsafe_allow_html=True)
    else:
        st.markdown('<h3 style="color:#ff4b4b;">● SYSTEM OFFLINE</h3>', unsafe_allow_html=True)

# --- Top Metrics Row ---
m1, m2, m3, m4 = st.columns(4)
m1.metric("Wallet Balance", "$24,560.80", "+$150.20")
m2.metric("Active Trades", "02", "BTC/USDT, ETH/USDT")
m3.metric("Win Rate (24h)", "89.4%", "+2.1%")
m4.metric("Daily Profit", "$420.55", "15% ROI")

st.divider()

# --- Main Dashboard Layout ---
tab_main, tab_history, tab_settings = st.tabs(["📊 Live Terminal", "📜 Trade History", "🛠 Advanced Config"])

with tab_main:
    c1, c2 = st.columns([2, 1])
    
    with c1:
        st.subheader("Live Market Analysis (Binance Stream)")
        # ලස්සන Candlestick Chart එකක්
        fig = go.Figure(data=[go.Candlestick(x=pd.date_range(datetime.now(), periods=50, freq='min'),
                        open=np.random.randn(50)+50000, high=np.random.randn(50)+50100,
                        low=np.random.randn(50)+49900, close=np.random.randn(50)+50050)])
        fig.update_layout(template="plotly_dark", height=400, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig, use_container_width=True)
        
        # Bot Control Buttons
        bc1, bc2 = st.columns(2)
        if bc1.button("🟢 START TRADING BOT", use_container_width=True):
            st.session_state.bot_running = True
            st.session_state.trade_logs.append(f"{datetime.now()} - Bot Started: Searching for Entries...")
            
        if bc2.button("🔴 STOP ALL TRADES", use_container_width=True):
            st.session_state.bot_running = False
            st.session_state.trade_logs.append(f"{datetime.now()} - Bot Stopped: All positions secured.")

    with c2:
        st.subheader("Live Order Status")
        if st.session_state.bot_running:
            st.markdown("""
                <div class="trade-card">
                    <b style="color:#00d1ff;">BUY ORDER: BTC/USDT</b><br>
                    Price: $64,230.12 | Status: <span style="color:#00ff00;">Trailing TP</span><br>
                    <b>Profit: +$45.20 (0.85%)</b>
                </div>
                <div class="trade-card">
                    <b style="color:#00d1ff;">SELL ORDER: ETH/USDT</b><br>
                    Price: $3,450.55 | Status: <span style="color:#f0b90b;">Waiting for Confirmation</span><br>
                    <b>Profit: -$2.10 (-0.05%)</b>
                </div>
            """, unsafe_allow_html=True)
            if st.button("❌ Manual Cancel Trade"):
                st.warning("Requesting Binance to cancel trade...")
        else:
            st.info("Bot is idle. No active trades found on Binance.")

with tab_history:
    st.subheader("Recent Execution History")
    history_df = pd.DataFrame({
        "Time": [datetime.now().strftime("%H:%M:%S") for _ in range(5)],
        "Pair": ["BTC/USDT", "SOL/USDT", "XRP/USDT", "BTC/USDT", "ETH/USDT"],
        "Type": ["LONG", "SHORT", "LONG", "LONG", "SHORT"],
        "Outcome": ["✅ Win (+$45)", "✅ Win (+$12)", "❌ Loss (-$5)", "✅ Win (+$80)", "✅ Win (+$22)"]
    })
    st.table(history_df)

with tab_settings:
    st.subheader("System Integration Logs")
    for log in st.session_state.trade_logs[-10:]:
        st.text(f"→ {log}")

# --- Footer ---
st.write("---")
st.caption("KD AI AUTO BOT PRO v4.2 | Connected to Binance Cloud | Status: Optimized")
